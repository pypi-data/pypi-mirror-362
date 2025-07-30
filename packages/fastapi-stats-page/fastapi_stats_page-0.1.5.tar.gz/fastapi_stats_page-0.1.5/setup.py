from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    docs = readme.read()

setup(
    name="fastapi-stats-page",
    version="0.1.5",
    description="FastAPI visitor statistics with middleware and stats page",
    author="Jackson Rodger",
    long_description=docs,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "fastapi_stats_page": ["templates/*.html"],
    },
    include_package_data=True,
    install_requires=[
        "fastapi",
        "jinja2",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
