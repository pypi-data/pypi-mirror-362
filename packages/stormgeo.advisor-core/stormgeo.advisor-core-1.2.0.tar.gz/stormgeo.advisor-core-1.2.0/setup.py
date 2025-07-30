from setuptools import setup, find_packages

setup(
    name = 'stormgeo.advisor-core',
    version = '1.2.0',
    author = 'climatempo',
    packages = find_packages(include=['advisor_core']),
    license = 'MIT',
    description = 'SDK to access the advisor core API.',
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url = 'https://github.com/StormGeo/advisor-sdk',
    project_urls = {
        'Código fonte': 'https://github.com/StormGeo/advisor-sdk/tree/main/python-advisor-core'
    }
)
