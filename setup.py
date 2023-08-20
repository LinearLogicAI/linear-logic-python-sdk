import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='linearlogic',
    version='0.4.0',
    author="Linear Logic Inc.",
    author_email="support@linearlogic.ai",
    description="Linear Logic Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://linearlogic.ai",
    packages=setuptools.find_packages(),
    install_requires=[
        "awesome_progress_bar>=1.7.2",
        "requests>=2.28.1",
        "colored==1.4.3",
        "rich==13.5.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['linlog=linlog.cli:main'],
    }
)
