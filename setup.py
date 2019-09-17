import setuptools

with open('README.md') as f:
    description = f.read()

setuptools.setup(
    name="pydatapack",
    version="0.1",
    description=description,
    author="Tom Gringauz",
    author_email="tomgrin10@gmail.com",
    url="https://github.com/tomgrin10/free-smiley-dealer-discord",
    packages=setuptools.find_packages(),
    install_requires=['mcpack', 'typeguard']
)
