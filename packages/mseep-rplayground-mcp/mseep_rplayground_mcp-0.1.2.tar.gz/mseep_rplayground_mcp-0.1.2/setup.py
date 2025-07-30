from setuptools import setup, find_packages

setup(
    name='mseep-rplayground-mcp',
    version='0.1.2',
    description='An MCP that lets the model transiently execute R code.',
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
    install_requires=['anyio>=4.9.0', 'mcp[cli]>=1.6.0', 'pillow>=10.0', 'pytest-asyncio>=0.26.0', 'pytest>=8.3.5', 'rpy2>=3.5.17', 'packaging>=24.2', 'pydantic-settings>=2.8.1'],
    keywords=['mseep'],
)
