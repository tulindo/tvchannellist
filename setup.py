import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

VERSION = {}
with open("tvchannellist/__version__.py") as fh:
    exec(fh.read(), VERSION)

setuptools.setup(
    name="tvchannellist",
    version=VERSION["__version__"],
    author="Paolo Tuninetto",
    author_email="paolo.tuninetto@gmail.com",
    description="Python Package for programmatically retrieving LCN of television channels.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/tulindo/tvchannellist",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">=3.7",
    install_requires=["requests"],
    scripts=["channellist"],
)
