from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gentune_flan",
    version="0.1.6",
    author="Manish Agrawal",
    author_email="manishagrawal.datascience@gmail.com",
    description="Genetic Algorithm: Optimize the finetuning of FLAN-T5 models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manishagrawal-datascience/gentune_flan.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "transformers>=2.53.1",
        "evaluate>=0.4.5",
        "numpy>=2.0.2",
        "pandas>=2.2.2",
        "rouge_score>=0.1.2"
    ],
)
