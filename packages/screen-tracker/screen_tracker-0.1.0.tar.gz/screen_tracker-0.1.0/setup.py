
from setuptools import setup, find_packages

setup(
    name="screen_tracker",
    version="0.1.0",
    author="Kamran Ahmed",
    author_email="kamranahmed.6388@gmail.com",
    description="Track screen usage and take automatic screenshots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screen_tracker",
    packages=find_packages(),
    install_requires=[
        "pygetwindow",
        "pyautogui",
        "pandas",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
