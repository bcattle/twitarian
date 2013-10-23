from distutils.core import setup
import py2exe

setup(
    name='Twitarian',
    version='0.2.1',
    description='Twitarian calculates twitter statistics',
    author='Bryan Cattle',
    url='http://github.com/bcattle/twitarian/',
    console=['twitarian.py']
)
