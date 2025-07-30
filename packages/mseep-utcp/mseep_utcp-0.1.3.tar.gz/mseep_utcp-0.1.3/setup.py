from setuptools import setup, find_packages

setup(
    name='mseep-utcp',
    version='0.1.3',
    description='Universal Tool Calling Protocol (UTCP) client library for Python',
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
    install_requires=['pydantic>=2.0', 'authlib>=1.0', 'python-dotenv>=1.0', 'tomli>=2.0', 'aiohttp>=3.8', 'mcp>=1.0', 'pyyaml>=6.0'],
    keywords=['mseep'],
)
