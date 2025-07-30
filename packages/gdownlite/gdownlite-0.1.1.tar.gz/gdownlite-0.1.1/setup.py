from setuptools import setup, find_packages

setup(
    name="gdownlite",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "gdownlite = gdownlite.__main__:main",
        ],
    },
    author="Christian Balais",
    author_email="christianbalais06@gmail.com",
    description="Simple Google Drive downloader with original filename",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ceejay06s/gdownlite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
