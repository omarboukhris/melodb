import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='melodb',
    version='0.0',
    author_email='omarboukhris@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/omarboukhris',
    project_urls = {
        "Bug Tracker": "https://github.com/omarboukhris"
    },
    packages=['melodb'],
    install_requires=['requests'],
)