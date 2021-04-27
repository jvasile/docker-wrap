import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="docker-wrap",
    version="0.0.1",
    author="James Vasile",
    author_email="james@opentechstrategies.com",
    description="A drop-in wrapper for docker-compose that runs pre/post scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jvasile/docker-wrap",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    scripts=['scripts/docker-wrap'],
)
