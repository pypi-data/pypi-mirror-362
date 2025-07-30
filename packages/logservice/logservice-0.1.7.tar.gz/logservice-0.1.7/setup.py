from setuptools import setup, find_packages

setup(
    name="logservice",
    version="0.1.7",
    description="Reusable CloudWatch log sender",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Naveenkumar Koppala",
    author_email="naveenkumar.k@tnsservices.com",
    # url="https://github.com/your-org/logservice",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'aioboto3>=15.0.0',
        "pydantic>=2.2.7,<3.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.9",
)
