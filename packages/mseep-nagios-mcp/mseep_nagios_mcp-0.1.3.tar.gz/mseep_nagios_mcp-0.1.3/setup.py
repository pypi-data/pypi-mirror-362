from setuptools import setup, find_packages

setup(
    name='mseep-nagios-mcp',
    version='0.1.3',
    description='MCP Server for Nagios Core',
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
    install_requires=['flask>=3.1.1', 'mcp[cli]>=1.8.0', 'pyyaml>=6.0.2', 'requests>=2.32.3'],
    keywords=['mseep'],
)
