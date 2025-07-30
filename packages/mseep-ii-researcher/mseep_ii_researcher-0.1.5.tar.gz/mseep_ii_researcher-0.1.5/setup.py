from setuptools import setup, find_packages

setup(
    name='mseep-ii-researcher',
    version='0.1.5',
    description='II Researcher Package',
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
    install_requires=['requests', 'baml-py==0.77.0', 'pydantic>=2.0.0', 'fastapi>=0.100.0', 'requests>=2.32.3', 'bs4>=0.0.2', 'markdownify>=1.0.0', 'readability-lxml>=0.8.1', 'lxml[html-clean]>=5.3.1', 'tavily-python>=0.5.1', 'colorama>=0.4.6', 'langchain-community>=0.3.18', 'yt-dlp>=2025.2.19', 'click>=8.1.8', 'langchain-openai>=0.3.7', 'pymupdf>=1.25.3', 'markdown>=3.7', 'clean-text[gpl]>=0.6.0', 'litellm[proxy]>=1.63.6', 'uvicorn>=0.29.0', 'baml-cli>=0.1.0'],
    keywords=['mseep'],
)
