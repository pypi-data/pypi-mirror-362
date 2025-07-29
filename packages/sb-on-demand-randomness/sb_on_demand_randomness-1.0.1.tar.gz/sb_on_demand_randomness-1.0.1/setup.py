from setuptools import setup, find_packages

setup(
    name="sb-on-demand-randomness",
    version="1.0.1",
    description="Switchboard On Demand Randomness Python SDK",
    author="kingsznhone",
    packages=find_packages(),
    install_requires=[
        "solders",
        "pydantic",
        "solana"
    ],
    python_requires='>=3.8',
    include_package_data=True,
    url="https://github.com/kingsznhone/sb-on-demand-randomness-py",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
