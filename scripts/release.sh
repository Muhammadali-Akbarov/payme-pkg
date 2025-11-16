#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting release process..."

if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
elif [ -d "env" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

if ! command -v pyarmor &> /dev/null; then
    echo "❌ PyArmor not found. Installing..."
    pip install pyarmor>=9.0.0
fi

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info payme_pkg.egg-info

mkdir -p build/temp

echo "🔒 Obfuscating code with PyArmor..."
pyarmor gen -O build/temp -r payme/

echo "📁 Organizing package structure..."
mv build/temp/payme build/payme
mv build/temp/pyarmor_runtime_* build/

rm -rf build/temp

echo "📦 Copying necessary files..."
cp README.md build/
cp LICENSE.txt build/
cp MANIFEST.in build/

echo "⚙️  Creating setup configuration..."
cat > build/setup.py << 'EOF'
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
EOF

echo "🔨 Building package..."
cd build
python setup.py sdist bdist_wheel

echo "📤 Uploading to PyPI..."
twine upload dist/*

cd ..
echo "✅ Release completed successfully!"
echo "🎉 Package uploaded to PyPI with obfuscated code!"
