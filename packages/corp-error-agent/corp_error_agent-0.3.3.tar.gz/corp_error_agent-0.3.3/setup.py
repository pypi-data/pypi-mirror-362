# setup.py
from setuptools import setup, find_packages
import sysconfig

site_packages = sysconfig.get_paths()["purelib"]

setup(
    name="corp_error_agent",
    version="0.3.3",
    description="Runtime agent that captures uncaught errors + env snapshot and prints data‑driven CLI hints.",
    author="Fayol Ateufack",
    author_email="arielfayol1@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.31",
        "platformdirs>=3.10",
    ],
    data_files=[(site_packages, ["corp_error_agent.pth"])],
    python_requires=">=3.8",
    license="MIT",
    url="https://github.com/arielfayol37/corp_error_agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
) 