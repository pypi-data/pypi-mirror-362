from setuptools import setup, find_packages

def read_requirements():
    with open("/home/vishnu/Data2/visualizerlib/visualizerlib/requirements.txt") as f:
        return f.read().splitlines()

setup(
    name="visulaizerlib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),  # dynamically read from requirements.txt
    author="vishnu",
    author_email="vishnurrajeev@gmail.com",
    description="A simple example package",
    license="MIT",
)