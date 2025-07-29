from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sce-minigame-publisher",
    version="0.1.7",
    author="SCE Team",
    author_email="jl@xd.com",
    description="TapTap SCE小游戏自动发布工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    py_modules=["sce_minigame_publisher"],
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "sce-minigame-publisher=sce_minigame_publisher:cli_main",
        ],
    },
) 