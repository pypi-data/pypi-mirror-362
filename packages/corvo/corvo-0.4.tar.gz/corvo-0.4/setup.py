from setuptools import find_packages, setup

def readme():
    with open('README.md', 'r') as f:
        README = f.read()
    return README

setup(
    name="corvo",
    version="0.4",
    author="Camila Santiago",
    description="A credential harvester, powered by the IntelX API.",
    url="https://github.com/santiag02/Corvo",
    packages=find_packages(exclude="media"),
    include_package_data=True,    
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=["python-dateutil", "requests"],
    keywords= ['leaks', 'credentials', 'intelx', 'data-leak', 'infostealer'],
    entry_points={
        "console_scripts": [ "corvo = corvo.main:main"],
    }
)

