from setuptools import setup, find_packages

setup(
    name="verifyid-sdk-python",
    version="1.0.2",
    description="Official Python SDK for VerifyID.io KYC, AML, Biometric and Document Verification APIs.",
    author="Philip Csaplar",
    author_email="your@email.com",
    url="https://github.com/ositid/verifyid-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0"
    ],
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
