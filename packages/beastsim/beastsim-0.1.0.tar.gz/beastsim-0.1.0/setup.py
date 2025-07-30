from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="BEASTsim",
    version="0.1.0",
    description="A benchmarking tool for Spatial Transcriptomics Simulations.",
    author="Tomás Bordoy García-Carpintero, Lucas Alexander Damberg Torp Dyssel",
    author_email="tobor@imada.sdu.dk, ludys@imada.sdu.dk",
    maintainer="Tomás Bordoy García-Carpintero",
    maintainer_email="tobor@imada.sdu.dk",
    packages=find_packages(include=["BEASTsim", "BEASTsim.*"]),
    install_requires=requirements,
    python_requires='>=3.9',
    include_package_data=True,
)
