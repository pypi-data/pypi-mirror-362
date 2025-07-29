from setuptools import setup, find_packages

setup(
    name="minimind",
    version="0.2.5",
    author="신유찬",
    author_email="shinnara.yuchan@gmail.com",
    description="MiniMind: Lightweight and flexible AI generation library",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/INSECT5386/MiniMind",  # 깃허브 주소 넣어줘
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21",
        "scikit-learn>=1.0",
        "autograd>=1.3",
        "joblib>=1.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    include_package_data=True,
    package_data={
        'minimind' : ['datasets/MLdata.csv'],
    },
    zip_safe=False,
)
