from setuptools import setup, find_packages


setup(
    name='payme-pkg',
    version='1.4',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    url='https://github.com/Muhammadali-Akbarov/payme_pkg',
    keywords='paymeuz paycomuz',
    install_requires=[
          'requests',
      ],
)
