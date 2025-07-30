from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

extensions = [
    Extension("runner.cy_loader", ["runner/cy_loader.pyx"])
]

setup(
    name="shadowseal",
    version="1.0.2",
    description="Secure Python encryptor and loader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Monarch of Shadows",
    author_email="farhanbd637@gmail.com",
    url="https://github.com/AFTeam-Owner/shadowseal",
    packages=find_packages(),
    install_requires=read_requirements(),
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    entry_points={
        "console_scripts": ["shadowseal=shadowseal.cli:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
)
