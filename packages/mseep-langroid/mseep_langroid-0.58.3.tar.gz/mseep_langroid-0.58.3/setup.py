from setuptools import setup, find_packages

setup(
    name='mseep-langroid',
    version='0.58.3',
    description='Harness LLMs with Multi-Agent Programming',
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
    install_requires=['adb-cloud-connector<2.0.0,>=1.0.2', 'aiohttp<4.0.0,>=3.9.1', 'async-generator<2.0,>=1.10', 'bs4<1.0.0,>=0.0.1', 'cerebras-cloud-sdk<2.0.0,>=1.1.0', 'colorlog<7.0.0,>=6.7.0', 'docstring-parser<1.0,>=0.16', 'duckduckgo-search<7.0.0,>=6.0.0', 'exa-py>=1.8.7', 'faker<19.0.0,>=18.9.0', 'fakeredis<3.0.0,>=2.12.1', 'fastmcp>=2.2.5', 'fire<1.0.0,>=0.5.0', 'gitpython<4.0.0,>=3.1.43', 'google-api-python-client<3.0.0,>=2.95.0', 'google-genai>=1.0.0', 'groq<1.0.0,>=0.13.0', 'grpcio<2.0.0,>=1.62.1', 'halo<1.0.0,>=0.0.31', 'jinja2<4.0.0,>=3.1.2', 'json-repair<1.0.0,>=0.29.9', 'lxml<6.0.0,>=5.4.0', 'markdownify>=0.13.1', 'nest-asyncio<2.0.0,>=1.6.0', 'nltk<4.0.0,>=3.8.2', 'onnxruntime<2.0.0,>=1.16.1', 'openai<2.0.0,>=1.61.1', 'pandas<3.0.0,>=2.0.3', 'prettytable<4.0.0,>=3.8.0', 'pydantic<3.0.0,>=1', 'pygithub<2.0.0,>=1.58.1', 'pygments<3.0.0,>=2.15.1', 'pymupdf4llm<0.1.0,>=0.0.17', 'pyparsing<4.0.0,>=3.0.9', 'pytest-rerunfailures<16.0,>=15.0', 'python-dotenv>=1.0.0,<2.0.0', 'python-magic<1.0.0,>=0.4.27', 'pyyaml<7.0.0,>=6.0.1', 'qdrant-client<2.0.0,>=1.8.0', 'rank-bm25<1.0.0,>=0.2.2', 'redis<6.0.0,>=5.0.1', 'requests<3.0.0,>=2.31.0', 'requests-oauthlib<2.0.0,>=1.3.1', 'rich<14.0.0,>=13.3.4', 'thefuzz<1.0.0,>=0.20.0', 'tiktoken<1.0.0,>=0.7.0', 'trafilatura<2.0.0,>=1.5.0', 'typer<1.0.0,>=0.9.0', 'wget<4.0,>=3.2'],
    keywords=['mseep'],
)
