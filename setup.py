import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='linlog',
    version='0.1',
    author="Linear Logic Inc.",
    author_email="support@linearlogic.ai",
    description="Linear Logic Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://linearlogic.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
