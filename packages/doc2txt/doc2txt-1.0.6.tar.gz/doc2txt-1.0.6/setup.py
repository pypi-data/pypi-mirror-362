from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="doc2txt",
    version="1.0.6",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "doc2txt": [
            "bin/darwin-arm64/*",
            "bin/linux-amd64/*", 
            "bin/win-amd64/*",
            "antiword_share/*",
        ],
    },
    install_requires=[
        "langdetect",
    ],
    python_requires=">=3.6",
    author="Quant",
    author_email="pengzhia@mail.com",  # 需要填写
    description="Python wrapper for antiword with bundled binary and data files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/quantatirsk/doc2txt-pypi",  # 需要填写项目URL
    project_urls={
        "Bug Reports": "https://github.com/quantatirsk/doc2txt-pypi/issues",  # 需要填写
        "Source": "https://github.com/quantatirsk/doc2txt-pypi",       # 需要填写
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Office/Business :: Office Suites",
    ],
    keywords="word doc text extraction antiword document",
    license="MIT",
)
