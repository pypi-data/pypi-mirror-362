from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from pathlib import Path
import os

class build_with_pth(build_py):
    def run(self):
        super().run()
        self.copy_file(
            str(Path(__file__).parent / "corp_error_agent.pth"),
            os.path.join(self.build_lib, "corp_error_agent.pth")
        )

setup(
    name="corp_error_agent",
    version="0.4.1",
    description="Runtime agent that captures uncaught errors + env snapshot and prints data‑driven CLI hints.",
    author="Fayol Ateufack",
    author_email="arielfayol1@gmail.com",
    url="https://github.com/arielfayol37/corp_error_agent",
    packages=find_packages(),
    install_requires=["requests>=2.31", "platformdirs>=3.10"],
    python_requires=">=3.8",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    cmdclass={"build_py": build_with_pth},
)
