from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='pynnacle_genesis',
    version='1.0.6', 
    packages=find_packages(),
    description='A Python module for the Pinnacle Genesis board, offering hands-on robotics coding with a familiar structure inspired by popular development board environments.',
    url='https://github.com/Red-Pula/pynnacle-genesis',
    author='Rafael Red Angelo M. Hizon, Jenel M. Justo, Serena Mae C.S. Lee',
    author_email='redhizon@gmail.com, jenel.just88@gmail.com, nmae.lee@gmail.com',
    license='GNU Affero General Public License',
    install_requires=[
        'pymata4>=1.15',
        'pyserial>=3.5'
    ],
    long_description=description,
    long_description_content_type="text/markdown",

    classifiers=[
        'Intended Audience :: Education',
        'Topic :: Education',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
)
