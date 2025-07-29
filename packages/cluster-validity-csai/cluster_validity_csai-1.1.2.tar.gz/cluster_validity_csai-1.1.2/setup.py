from setuptools import setup, find_packages

setup(
    name='cluster-validity-csai',
    description='CSAIEvaluator: A Cluster Stability Assesment Index for clustering validation',
    author='Adane Nega Tarekegn',
    author_email='nega2002@email.com',
    url='https://github.com/adaneNT/cluster-validity-csai',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        'umap-learn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
