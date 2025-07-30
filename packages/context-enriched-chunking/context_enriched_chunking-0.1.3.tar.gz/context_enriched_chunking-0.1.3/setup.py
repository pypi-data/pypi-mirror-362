from setuptools import setup, find_packages

setup(
    name="context_enriched_chunking",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["langchain-text-splitters==0.3.6"],  # Add dependencies if needed
    author="Elvis A. de Souza",
    author_email="elvis.desouza99@gmail.com",
    description="A text chunking strategy that keeps document title and section as headers for each chunk.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alvelvis/context-enriched-chunking",  # Update with your repo link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
