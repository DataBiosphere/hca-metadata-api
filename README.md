[![Build Status](https://travis-ci.com/DataBiosphere/hca-metadata-api.svg?branch=develop)](https://travis-ci.com/DataBiosphere/hca-metadata-api)
[![Coverage Status](https://coveralls.io/repos/github/DataBiosphere/hca-metadata-api/badge.svg?branch=develop)](https://coveralls.io/github/DataBiosphere/hca-metadata-api?branch=develop)

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
pip install "git+git://github.com/DataBiosphere/hca-metadata-api@master#egg=hca-metadata-api[dss]"
```

You can omit `[dss]` at the end of the `pip` invocation if you don't need
the download helper this library provides and don't want to pull in the HCA CLI
distribution the helper depends on.

## Github credentials

Github credentials in the form of a personal access token are required to run
test cases that pull files from the canned staging area in the
[schema-test-data](https://github.com/HumanCellAtlas/schema-test-data)
repository.

Use the
[Creating a personal access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token)
guide to create your token. No additional scopes or permissions should be
granted to this token as it will only be used to read from the canned staging
area repository.

Copy the token and use it as the value of an environment variable named
`GITHUB_TOKEN`.

## Release guide

This guide will walk you through the steps necessary to promote the `develop`
branch to `main`, tag the release, and prepare `develop` for the next release.

Note: For purpose of example, this guide will pretend we are upgrading `main`
from release 29 to 30.

1. Merge `develop` into `main`.

   - Resolve conflicts in `setup.py`, promote to the higher version.

       ```
       <     version="1.0b29",       # value from `main`
       <     version="1.0b30.dev1",  # value from `develop`
       >     version="1.0b30",       # new value for `main`
       ```

   - Title the merge commit: "Release beta 30".

   - Push `main` to GitHub.

2. Create a new release.

   - On the GitHub repository home page click *Releases* — *Draft a new release*

       - Tag: (create new) `release/1.0b30`

       - Target: `main`

       - Title: `Release 1.0 beta 30`

       - description: (list all tickets & PRs included since the previous release)

       - This is a pre-release: (leave unchecked)

       - Click *Publish release*.

3. Prepare `develop` for the next release.

   - Add a commit to increment the version in `setup.py` .

       ```
       <    version="1.0b30.dev1",
       >    version="1.0b31.dev1",
       ```

   - Title the commit "Prepare beta 31".

   - Push `develop` to GitHub.
