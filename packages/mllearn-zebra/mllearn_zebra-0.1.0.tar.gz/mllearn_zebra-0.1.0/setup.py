from setuptools import setup, find_packages

setup(
    name='mllearn-zebra',  
    version='0.1.0',
    author='Balayya',
    author_email='',
    description='View machine learning algorithms as code',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mahi044/mllearn-zebra',  
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.7',
)
