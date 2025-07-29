from setuptools import setup, find_packages

setup(
    name="logservice",
    version="0.1.1",
    description="Reusable CloudWatch log sender",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Naveenkumar Koppala",
    author_email="naveenkumar.k@tnsservices.com",
    # url="https://github.com/your-org/logservice",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'aioboto3>=10.0.0',
        'pydantic>=1.10.0,<2.11.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.11",
)
