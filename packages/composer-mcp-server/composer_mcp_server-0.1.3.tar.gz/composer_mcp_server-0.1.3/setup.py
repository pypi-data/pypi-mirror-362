from setuptools import setup
import os

VERSION = "0.1.3"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="composer-mcp-server",
    description="composer-mcp-server is now composer-trade-mcp",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    install_requires=["composer-trade-mcp"],
    classifiers=["Development Status :: 7 - Inactive"],
)
