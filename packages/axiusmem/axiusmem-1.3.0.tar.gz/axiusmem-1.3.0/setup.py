from setuptools import setup, find_packages

setup(
    name="axiusmem",
    version="1.3.0",
    description="A W3C-compliant temporal knowledge graph library for AI agents.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Timothy W. Cook",
    url="https://github.com/yourusername/axiusmem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "rdflib>=6.0.0",
        "requests>=2.25.0",
        "pandas>=1.3.0",
        "python-dotenv>=0.19.0",
        "langchain>=0.1.0",
        "langgraph>=0.0.30",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "anthropic>=0.21.0",
        "cohere>=4.0.0",
        "transformers>=4.40.0",
        "huggingface_hub>=0.23.0",
        "mistralai>=0.1.0",
        # Add more as needed
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="Apache-2.0",
) 