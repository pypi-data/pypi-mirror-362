from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="alfinx_utils",
    version="0.3.6",
    description="HTTP headers auto detection tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Maharram",
    author_email="maharram@alfinx.com",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "httpx",
    ],
    python_requires='>=3.8',
    zip_safe=False
)
