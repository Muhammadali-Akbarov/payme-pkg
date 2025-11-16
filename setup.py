import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='payme-pkg',
    version='3.0.30',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages(),
    url='https://github.com/Muhammadali-Akbarov/payme-pkg',
    keywords='paymeuz paycomuz payme-merchant merchant-api subscribe-api payme-pkg payme-api',
    install_requires=[
        'requests==2.*',
        "dataclasses==0.*;python_version<'3.7'",
        'djangorestframework==3.*',
        'pyarmor>=9.0.0',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        '': ['*.so', '*.pyd', '*.dll'],
        'pyarmor_runtime_000000': ['*.so', '*.pyd', '*.dll', '__init__.py'],
    },
)
