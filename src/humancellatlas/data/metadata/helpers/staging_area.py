from collections import (
    defaultdict,
)
import json
import logging
import os
from typing import (
    Mapping,
    MutableMapping,
    Optional,
    Set,
    Tuple,
    Union,
)

from github import (
    Github,
)

from humancellatlas.data.metadata.api import (
    Bundle,
    JSON,
)

logger = logging.getLogger(__name__)


class File:
    """
    A JSON file in the staging area.
    """

    def __init__(self, uuid: str, version: str, name: str, content: JSON):
        self.uuid = uuid
        self.name = name
        self.version = version
        self.content = content


class LinksFile(File):
    """
    A file describing the links between entities in a subgraph.
    """

    def __init__(self, file_name: str, content: JSON):
        assert file_name.endswith('.json')
        file_id, version, project_id = file_name[:-5].split('_')
        super().__init__(file_id, version, file_name, content)
        self.project_id = project_id


class MetadataFile(File):
    """
    A file describing one entity (e.g. biomaterial, protocol) in an subgraph.
    """

    def __init__(self, file_name: str, content: JSON):
        assert file_name.endswith('.json')
        file_id, version = file_name[:-5].split('_')
        super().__init__(file_id, version, file_name, content)


class DescriptorFile(File):
    """
    A file containing the checksums and other information for asserting the
    integrity of a data file.
    """

    def __init__(self, file_name: str, content: JSON):
        assert file_name.endswith('.json')
        file_id, version = file_name[:-5].split('_')
        super().__init__(file_id, version, file_name, content)

    @property
    def translated_content(self):
        """
        The content of a descriptor transformed into a format ready to create a
        ManifestEntry object.
        """
        content = dict(self.content)
        content['name'] = content.pop('file_name')
        content['uuid'] = content.pop('file_id')
        content['version'] = content.pop('file_version')
        content['content-type'] = content.pop('content_type')
        content['indexed'] = True
        return content


class StagingArea:

    def __init__(self,
                 repo_owner: str,
                 repo_name: str,
                 repo_branch: str,
                 repo_path: Optional[str]
                 ):
        token = os.environ['GH_API_TOKEN']  # A GitHub personal access token
        logger.debug('Requesting GitHub repo %s/%s', repo_owner, repo_name)
        self.github_api = Github(token)
        self.log_rate_limit()
        self.repo = self.github_api.get_repo(f'{repo_owner}/{repo_name}')
        branch = self.repo.get_branch(repo_branch)
        self.branch_sha = branch.commit.sha
        self.path = () if not repo_path else tuple(repo_path.split('/'))
        # Fetch all the links, metadata, and descriptor files from the staging
        # area and store the files in a mapping by their file ID.
        self.links: Mapping[str, LinksFile]
        self.metadata: Mapping[str, MetadataFile]
        self.descriptors = Mapping[str, DescriptorFile]
        self.links = self.get_files(self.path + ('links',))
        self.metadata = self.get_files(self.path + ('metadata',))
        self.descriptors = self.get_files(self.path + ('descriptors',))
        self.log_rate_limit()

    def log_rate_limit(self):
        """
        Log the current GitHub rate limit values
        """
        rate_limit = self.github_api.get_rate_limit()
        logger.debug('GitHub API rate limit limit=%i, remaining=%i, reset=%s',
                     rate_limit.core.limit, rate_limit.core.remaining, rate_limit.core.reset)

    def get_files(self,
                  path: Tuple[str, ...]
                  ) -> MutableMapping[str, Union[LinksFile, MetadataFile, DescriptorFile]]:
        """
        Returns a mapping of file ID to JSON content for files in the given path
        """
        files = {}
        path_str = '/'.join(path)
        logger.debug('Requesting contents of %s', path_str)
        for content in self.repo.get_contents(path_str, ref=self.branch_sha):
            if content.type == 'dir':
                dir_name: str = content.name
                files.update(self.get_files(path + (dir_name,)))
            else:
                file_name = content.name
                file_json = json.loads(content.decoded_content)
                schema_type = file_json['schema_type']
                if schema_type == 'links':
                    assert 'links' in path, content.path
                    file = LinksFile(file_name, file_json)
                elif schema_type == 'file_descriptor':
                    assert 'descriptors' in path, content.path
                    file = DescriptorFile(file_name, file_json)
                else:
                    assert 'metadata' in path, content.path
                    file = MetadataFile(file_name, file_json)
                try:
                    existing_version = files[file.uuid].version
                except KeyError:
                    files[file.uuid] = file
                else:
                    # If multiple metadata files with the same ID were found
                    # keep the one with the largest version
                    if file.version > existing_version:
                        files[file.uuid] = file
                    else:
                        pass
        return files

    def file_type_ids(self,
                      subgraph_id: str
                      ) -> MutableMapping[str, Set[str]]:
        """
        Parse the links in a subgraph and return a mapping of the metadata file
        types (e.g. 'analysis_file', 'cell_suspension') to a set of file IDs
        """
        link_obj: LinksFile = self.links[subgraph_id]
        links_json = link_obj.content
        file_ids = defaultdict(set)
        # Project ID is only mentioned in the links JSON if there is a
        # supplementary_file_link so add it here to make sure it gets included.
        file_ids['project'].add(link_obj.project_id)
        link: JSON
        for link in links_json['links']:
            if link['link_type'] == 'process_link':
                file_type = link['process_type']
                file_ids[file_type].add(link['process_id'])
                for link_type in ('input', 'output', 'protocol'):
                    for file in link[f'{link_type}s']:
                        file_type = file[f'{link_type}_type']
                        file_ids[file_type].add(file[f'{link_type}_id'])
            elif link['link_type'] == 'supplementary_file_link':
                for file in link['files']:
                    file_type = file['file_type']
                    file_ids[file_type].add(file['file_id'])
        return dict(file_ids)

    def get_bundle(self, subgraph_id: str) -> Bundle:
        """
        Return a hca-metadata-api Bundle object for the given subgraph ID.
        """
        logger.debug('Composing bundle %s', subgraph_id)
        links_file: LinksFile = self.links[subgraph_id]
        file_type_ids = self.file_type_ids(subgraph_id)

        manifest = []
        metadata = {
            'links.json': links_file.content
        }

        for file_type, file_ids in file_type_ids.items():
            for i, file_id in enumerate(file_ids):
                key = f'{file_type}_{i}.json'
                metadata[key] = self.metadata[file_id].content
                if file_type.endswith('_file'):
                    file_manifest = self.descriptors[file_id].translated_content
                    file_name = file_manifest['name']
                    if file_name.startswith(f'{subgraph_id}/'):
                        file_manifest['name'] = file_name.partition('/')[-1]
                    manifest.append(file_manifest)

        logger.debug('Bundle contents: %s', list(metadata.keys()))
        return Bundle(links_file.uuid, links_file.version, manifest, metadata)
