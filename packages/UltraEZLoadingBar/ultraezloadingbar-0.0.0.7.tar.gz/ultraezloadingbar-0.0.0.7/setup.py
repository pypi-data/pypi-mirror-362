from setuptools import setup, find_packages

setup(
    name="UltraEZLoadingBar",  # Unique name for your package
    version="0.0.0.7",  # Increment the version number
    description="A simple console-based loading bar for Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ItsAlexander91",
    author_email="alexander.bagwell9@gmail.com",
    packages=find_packages(),  # This will automatically include Ez_Loading_Bar
    classifiers=[  # Classifiers help users find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["cryptography"],  # Added dependency on cryptography
    python_requires='>=3.6',  # Optional: specify Python version compatibility
)
