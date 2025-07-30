from setuptools import setup, find_packages

setup(
    name='mseep-nautex',
    version='0.1.10',
    description='Nautex AI MCP server that works as Product and Project manager for coding agents',
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
    install_requires=['pydantic>=2.0.0,<3.0.0', 'pydantic-settings>=2.0.0,<3.0.0', 'aiohttp>=3.9.0,<4.0.0', 'textual>=3.0.0,<5.0.0', 'fastmcp>=2.8.1', 'python-dotenv>=1.0.0,<2.0.0', 'aiofiles>=20.0.0'],
    keywords=['mseep'],
)
