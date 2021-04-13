import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="musicDownloader",
    version="1.01",

    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A video downloader, with integrated mp3 conversion and metadata addition",

    author="dadope",
    url="https://github.com/dadope/musicDownloader",

    python_requires='>=3',
    include_package_data=True,
    packages=setuptools.find_packages(),

    entry_points={
        "console_scripts": ["musicDownloader = musicDownloader.main:main"]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)

