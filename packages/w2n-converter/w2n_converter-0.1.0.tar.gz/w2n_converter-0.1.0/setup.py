from setuptools import setup, find_packages

setup(
    name='w2n_converter',
    version='0.1.0',
    description='Converts an English word to a list of numbers corresponding to the positions of the letters in the English alphabet (a=1, ..., z=26)',
    author='Diyorbekw',
    author_email='diyorbek0143@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
