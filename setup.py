from setuptools import setup, find_packages


setup(
    name='paymentsuz',
    version='0.3',
    license='MIT',
    author="Muhammadali Akbarov",
    author_email='muhammadali17abc@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Muhammadali-Akbarov/payme_uz',
    keywords='paymeuz paycomuz',
    install_requires=[
          'requests',
      ],
)
