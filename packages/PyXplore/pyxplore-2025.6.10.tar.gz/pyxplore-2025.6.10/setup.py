import os
from setuptools import setup, find_packages

# 读取 README 内容
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PyXplore',
    version='2025.06.10',
    description='Toolkit for refining crystal structures using WPEM',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bin CAO',
    author_email='bincao4-c@my.cityu.edu.hk',
    maintainer='Bin CAO',
    maintainer_email='bincao4-c@my.cityu.edu.hk',
    license='MIT License',
    url='https://github.com/Bin-Cao/PyWPEM',
    packages=find_packages(include=['PyXplore', 'PyXplore.*']),
    include_package_data=True,
    package_data={
        # 包含所有 .pdf、.cif、.ipynb 文件作为数据资源
        'PyXplore': [
            'refs/*.pdf',
            '**/*.ipynb',
            '**/*.cif'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=[

        'numpy',
        'matplotlib',
        'scipy',
        'pymatgen',
    ],
)
