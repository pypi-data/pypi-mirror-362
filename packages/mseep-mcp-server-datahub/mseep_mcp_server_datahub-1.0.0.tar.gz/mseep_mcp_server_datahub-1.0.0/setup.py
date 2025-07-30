from setuptools import setup, find_packages

setup(
    name='mseep-mcp-server-datahub',
    version='1.0.0',
    description='A Model Context Protocol (MCP) server for DataHub',
    long_description="Package managed by MseeP.ai",
    long_description_content_type="text/plain",
    author='mseep',
    author_email='support@skydeck.ai',
    maintainer='mseep',
    maintainer_email='support@skydeck.ai',
    url='https://github.com/mseep',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['acryl-datahub==1.1.0.5rc11', 'fastmcp==2.10.4', 'jmespath~=1.0.1'],
    keywords=['mseep'],
)
