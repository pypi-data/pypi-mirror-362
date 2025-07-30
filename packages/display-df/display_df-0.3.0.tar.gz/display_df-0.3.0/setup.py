from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="display_df",
    version="0.3.0",
    description="An interactive Pandas DataFrame viewer that enables better-than-notepad viewing abilities in normal Python files 👀",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=["pandas", "PyQt5"],
    python_requires=">=3.7",
    url="https://github.com/yourusername/display_df",  # Update this if you publish to GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
