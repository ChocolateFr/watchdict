from setuptools import setup, find_packages

setup(
    name='watchdict',
    version='0.1.4',
    packages=find_packages(),
    description='A dictionary class with change detection and state persistence',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Chocolate',
    author_email='theerilia@gmail.com',
    url='https://github.com/chocolatefr/watchdict',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
    test_suite='tests',
)
