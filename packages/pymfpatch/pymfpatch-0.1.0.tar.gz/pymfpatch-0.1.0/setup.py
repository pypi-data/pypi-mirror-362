from setuptools import setup, find_packages

setup(
    name='pymfpatch',
    version='0.1.0',
    description='Fill missing weather measurements using user-provided ERA5 data and a TensorFlow encoder-decoder model',
    author='Alexis SAUVAGEON',
    author_email='alexis.sauvageon@arep.fr',
    url="https://gitlab.com/arep-dev/pymfpatch.git",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy==2.3.1",
        "pandas==2.3.1",
        "scikit-learn==1.7.0",
        "torch==2.7.1",
        "tqdm==4.67.1",
        "xgboost==3.0.2",
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "pymfpatch=pymfpatch.cli:main",
        ],
    },
)

