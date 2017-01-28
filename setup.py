from setuptools import setup, find_packages
from codecs import open
from os import path

thisDir = paths.abspath(path.dirname(__file__))
with open(path.join(thisDir, 'README.rst'), encoding='utf-8') as f:
    long_desc = f.read()

setup(
        name='rpi-camserver',
        version='0.0.1',
        description='A streaming server for the Raspberry camera',
        long_description=long_desc,
        url='https://github.com/stelzch/HolMOS',
        author='Christoph Stelz',
        author_email='mail@ch-st.de',
        license='MIT',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console :: Curses',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Multimedia :: Video :: Capture'
        ]
        keywords='raspberry video streaming camera',
        packages=find_packages(exclude=['contrib','docs','tests']),
        install_requires=[], # Runtime dependencies
)
