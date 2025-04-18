from setuptools import setup, find_packages

setup(
    name='callisto',
    version='0.1.0',
    author='Maharava',
    description='Memory management system for the Jupiter AI home companion.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/callisto',
    packages=['src'],  # Direct reference to src directory
    install_requires=[
        # Only include what's actually needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)