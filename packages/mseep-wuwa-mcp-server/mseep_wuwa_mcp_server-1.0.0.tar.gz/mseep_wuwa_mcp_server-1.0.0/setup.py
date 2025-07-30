from setuptools import setup, find_packages

setup(
    name='mseep-wuwa-mcp-server',
    version='1.0.0',
    description='Add your description here',
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
    install_requires=['asyncio>=3.4.3', 'beautifulsoup4>=4.13.4', 'httpx>=0.28.1', 'mcp[cli]>=1.7.0'],
    keywords=['mseep'],
)
