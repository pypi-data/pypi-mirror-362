from setuptools import setup, find_packages

setup(
    name='neuralinit',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'neuralinit=neuralinit.builder:main'
        ]
    },
    install_requires=[],
    author='Charles Jeyaseelan',
    author_email='charlesjeyaseelan03.research@gmail.com',
    description='Automation tool to scaffold deep learning project directory structure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/charlesjeyaseelan/neuralinit',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    python_requires='>=3.6',
)
