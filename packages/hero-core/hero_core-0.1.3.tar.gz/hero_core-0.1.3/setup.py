from setuptools import setup, find_packages

setup(
    name='hero-core',
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.16",
        "beautifulsoup4>=4.13.4",  # 主要是 search web_crawler 中使用, 后续看看怎么分离
        "chardet>=5.2.0",
        "colorama>=0.4.6",
        "librosa>=0.11.0",
        "mypy>=1.15.0",
        "numpy>=2.2.6",
        "openai>=1.70.0",
        "pandas>=2.2.3",
        "playwright>=1.52.0",
        "pypdf2>=3.0.1",
        "python-docx>=1.1.2",
        "python-pptx>=1.0.2",
        "python-ulid[pydantic]>=3.0.0",
        "tqdm>=4.67.1",
    ],
    author='Baidu',
    author_email='lanyu@baidu.com',
    description='A brief description of your library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/baidu/hero-core',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License 2.0",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    python_requires='>=3.12',
    package_data={
        'hero': ['prompt/*.md', 'util/*.txt'],
    },
)
