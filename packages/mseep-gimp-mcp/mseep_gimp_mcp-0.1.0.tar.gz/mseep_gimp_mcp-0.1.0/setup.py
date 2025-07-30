from setuptools import setup, find_packages

setup(
    name='mseep-gimp-mcp',
    version='0.1.0',
    description='GIMP MCP integration for external control of GIMP 3.0',
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
    install_requires=['mcp', 'fastmcp'],
    keywords=['mseep'],
)
