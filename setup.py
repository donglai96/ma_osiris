from setuptools import setup, find_packages

setup(
    name='ma_osiris',  # Package name
    version='0.1.0',  # Initial release version
    author='Donglai Ma',  # Your name
    author_email='donglaima96@gmail.com',  # Your email
    description='A useful code for osiris diag',  # A short description
    long_description=open('README.md').read(),  # Long description read from the readme file
    long_description_content_type='text/markdown',  # Type of the long description, usually markdown or plain text
    url='http://github.com/donglai96/ma_osiris',  # Link to your project repository
    packages=find_packages(),  # Automatically find all packages and subpackages
    install_requires=[
        'numpy',  # Required packages for your project
        'pandas',  # Add other dependencies as needed
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Development status
        'Intended Audience :: Developers',  # Target audience
        'Natural Language :: English',  # Language
        'Programming Language :: Python :: 3',  # Supported Python versions
        'Programming Language :: Python :: 3.10',  # Specify additional versions
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
)
