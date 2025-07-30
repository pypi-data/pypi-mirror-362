from setuptools import setup, find_packages

setup(
    name="euriai",
    version="0.4",
    description="Python client for Euri API (euron.one) with CLI, LangChain, and LlamaIndex integration",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Euri",
    author_email="tech@euron.one",
    packages=find_packages(include=["euriai", "euriai.*", "euri"]),
    install_requires=[
        "requests",
        "numpy",
        "pyyaml",
    ],
    extras_require={
        "langchain-core": ["langchain-core"],
        "langchain": ["langchain"],
        "llama-index": ["llama-index>=0.10.0"],
        "langgraph": ["langgraph"],
        "smolagents": ["smolagents"],
        "n8n": ["requests"],
        "crewai": ["crewai"],
        "autogen": ["pyautogen"],
        "test": ["pytest"],
    },
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "euriai=euriai.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
    license="MIT",
)
