from setuptools import setup, find_packages

setup(
    name="trelia",
    version=" 0.3.0",
    description="A Python package to rate and review student code using different llm's",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Aegletek",
    author_email="coe@aegletek.com",
    url="https://www.aegletek.com/",
    license="MIT",
    packages=find_packages(),  # auto-detects trelia
    install_requires=[
        "google-generativeai",
        "kynex"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",

    ],
    python_requires='>=3.7',
)
