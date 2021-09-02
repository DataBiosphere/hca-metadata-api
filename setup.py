from setuptools import setup, find_namespace_packages

setup(
    name="hca-metadata-api",
    version="1.0b32",
    license='MIT',
    install_requires=[
        "dataclasses >= 0.6;python_version<'3.7'"
    ],
    # Not using tests_require because that installs the test requirements into .eggs, not the virtualenv
    extras_require={
        "dss": [
            'hca == 7.0.0',
            'urllib3 >= 1.23',
            'requests >= 2.19.1'
        ],
        "staging_area": [
            'attrs == 20.3.0',
            'furl == 2.1.2',
            'jsonschema == 3.2.0',
            'PyGithub == 1.54.1'
        ],
        "examples": [
            'jupyter >= 1.0.0'
        ],
        "coverage": [
            'coverage',
            'coveralls'
        ],
        "test": [
            'checksumming_io == 0.0.1',
            'atomicwrites == 1.3.0',
            'more_itertools == 7.0.0'
        ]
    },
    package_dir={'': 'src'},
    packages=find_namespace_packages('src'),
    project_urls={
        "Source Code": "https://github.com/DataBiosphere/hca-metadata-api",
    }
)
