from setuptools import setup, find_packages

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="aniwatch-tr",
    version="1.0.0",
    author="https://github.com/DeoDorqnt387/aniwatch-tr",
    description="Türkçe anime izleme ve indirme aracı",
    long_description="Aniwatch-TR CLI ile anime izleyip indirebilirsiniz",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aniwatch-tr=aniwatch_tr.__main__:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)