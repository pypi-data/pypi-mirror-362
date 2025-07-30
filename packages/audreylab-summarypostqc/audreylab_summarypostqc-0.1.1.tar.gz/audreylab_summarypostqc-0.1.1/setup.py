from setuptools import setup, find_packages

setup(
    name='audreylab-summarypostqc',
    version='0.1.1',
    description='GWAS summary QC plotting tool (QQ & Manhattan plots)',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author='Etienne Kabongo',
    author_email='etienne@example.com',
    url='https://github.com/audreygrantlab/audreylab-summarypostqc',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'audreylab-summarypostqc = audreylab_summarypostqc.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)

