from setuptools import setup, find_packages

setup(
    name='nanourls',  # Must be unique on PyPI
    version='0.1.0',
    author='Yug Bhuva',
    author_email='ybhuva817@gmail.com',
    description='A tiny Python URL shortener',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Yugbhuva/nanourls',  # Optional but good
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)