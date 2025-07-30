from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="insightaid",
    version="0.0.1",
    author="Tomek Porozynski",
    author_email="tomasz.porozynski@gmail.com",
    description="Private, on-device AI accessibility assistant powered by Gemma",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ontaptom/insightaid",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)