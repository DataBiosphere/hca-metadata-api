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
