from setuptools import setup, find_packages
import os

def get_version():
    """Read version from version.py without importing the module."""
    version_file = os.path.join(os.path.dirname(__file__), "vsi", "version.py")
    with open(version_file) as f:
        for line in f:
            if line.startswith("VERSION"):
                return line.split("=")[1].strip().replace('"', '').replace("'", "")
    raise RuntimeError("Version not found in version.py")

setup(
    name="vbsoundinference",
    version=get_version(),
    install_requires=["numpy", "sounddevice", "torch"],
    packages=find_packages(),
    author="Samarth Javagal",
    author_email="samarthjavagal@gmail.com",
    description="A python library for wake-word detection on low end devices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",    # or whichever you pick
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)


