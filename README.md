[![Build Status](https://travis-ci.org/HumanCellAtlas/metadata-api.svg?branch=develop)](https://travis-ci.org/HumanCellAtlas/metadata-api)
[![Coverage Status](https://coveralls.io/repos/github/HumanCellAtlas/metadata-api/badge.svg?branch=develop)](https://coveralls.io/github/HumanCellAtlas/metadata-api?branch=develop)

## The HumanCellAtlas metadata API

A light-weight wrapper library around the JSON metadata in HCA data bundles.
The library serves two purposes: providing convenient programmatic access to a
subset of metadata attributes as well as decoupling clients from schema changes
that would break direct access to the metadata.


## Installation

Version 1.0 will be on PyPI but until then we need to install from GitHub: 

```
virtualenv -p python3 foo
source foo/bin/activate
pip install "git+git://github.com/HumanCellAtlas/metadata-api@master#egg=hca-metadata-api[dss]"
```

You can omit `[dss]` at the end of the `pip` invocation if you don't need
the download helper this library provides and don't want to pull in the HCA CLI
distribution the helper depends on.

## Github credentials

Github credentials in the form of a personal access token is required to run test
cases that pull files from the canned staging area in the 
[schema-test-data](https://github.com/HumanCellAtlas/schema-test-data) repository.

Use the
[Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
guide to create your token. Give your token a descriptive name such as "For 
running hca-metadata-api test cases". No additional scopes or  permissions need 
to be granted to this token as this token will only be used for read access 
from the canned staging area repository.

After your token has been generated, copy the token value and use it to create
an environment variable named `GH_API_TOKEN` either by adding it to your shell
(e.g. ~/.bash_profile) or Pycharm's run configurations menu for the project.
