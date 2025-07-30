from setuptools import setup, find_packages

with open("readme.md", "r") as f:
    description = f.read()

setup(
    name="EYPA",
    version="0.0.0.0.0.0.1.5",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "eypa.info.version = console:Get_İNFO_Version"
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown"
)
