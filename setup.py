from setuptools import setup, find_packages


setup(
    name='payme-pkg',
    version='2.6.7',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    url='https://github.com/Muhammadali-Akbarov/payme-pkg',
    keywords='paymeuz paycomuz payme-merchant merchant-api subscribe-api payme-pkg payme-api',
    install_requires=[
        'requests==2.*',
        "dataclasses==0.*;python_version<'3.7'",  # will only install on py3.6
        'djangorestframework==3.*'
      ],
)
