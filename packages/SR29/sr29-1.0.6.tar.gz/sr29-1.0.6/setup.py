import os.path

from Cython.Build import cythonize
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext


class Build(build_ext):
    def build_extension(self, ext):
        if not self.build_lib.endswith('sr29'):
            self.build_lib = os.path.join(self.build_lib, 'sr29')
        super().build_extension(ext)


with open('README.md', 'r') as fl:
    long_des = fl.read()

libs = cythonize(["src/*"])

setup(
    name='SR29',
    version='1.0.6',
    author='Evan243',
    install_requires="progress",
    description='The SR29 encode and decode',
    long_description=long_des,
    long_description_content_type="text/markdown",
    ext_modules=libs,
    zip_safe=False,
    packages=find_packages(),
    package_data={
        '': ['LICENSE', 'NOTICE'],
        'sr29': ['*.pyi']
    },
    cmdclass=dict(build_ext=Build),
    include_package_data=True,
    license="Apache License 2.0",
    entry_points={
        'console_scripts': [
            'SR29 = sr29:main'
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        ],
)
