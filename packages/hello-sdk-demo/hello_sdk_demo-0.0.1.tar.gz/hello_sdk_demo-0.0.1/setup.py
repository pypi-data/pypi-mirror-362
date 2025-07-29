from setuptools import setup, find_packages

setup(
    name="hello-sdk-demo",       # ⚠️ PyPI 名唯一！
    version="0.0.1",
    author="Your Name",
    author_email="you@example.com",
    description="A minimal example Python SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.6",
)

