import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="showdown-anal-bot",
    version="0.0.2",  # PyPi shenanigans
    author="yoursred",
    author_email="yoursred@yoursred.com",
    description="Pokemon Showdown analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoursred/showdown-anal-bot",
    project_urls={
        "Bug Tracker": "https://github.com/yoursred/showdown-anal-bot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        'showdownpy',
        'requests',
    ],
)
