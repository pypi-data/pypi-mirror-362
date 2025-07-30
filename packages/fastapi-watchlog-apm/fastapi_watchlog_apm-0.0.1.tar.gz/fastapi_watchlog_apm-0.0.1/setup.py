from setuptools import setup, find_packages

setup(
    name="fastapi_watchlog_apm",
    version="0.0.1",
    description="Lightweight APM for FastAPI that sends metrics to Watchlog Agent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mohammadreza",
    author_email="mohammadnajm75@gmail.com",
    url="https://github.com/Watchlog-monitoring/fastapi_watchlog_apm",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "starlette",
        "psutil",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
