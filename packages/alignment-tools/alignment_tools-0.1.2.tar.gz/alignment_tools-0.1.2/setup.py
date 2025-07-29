from setuptools import setup, find_packages
install_requires=[
          "pandas",
          "numpy",
          "matplotlib",
          "seaborn",
          "scipy",
          "biopython",
          "freesasa"
            ]


setup(
    name="alignment_tools",
    version="0.1.2",
    packages=find_packages(),
    install_requires=install_requires,
    author="Amirhossein Sakhteman",
    author_email="amirhossein.sakhteman@tume.de",
    description="Tools for AlphaFold PDB processing, SASA, Clustal, and InterPro annotation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
)
