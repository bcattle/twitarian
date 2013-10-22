from distutils.core import setup
import py2exe

setup(
    name='Twitarian',
    version='0.2.0',
    description='Twitarian calculates twitter statistics',
    author='Bryan Cattle',
    url='http://github.com/bcattle/twitarian/',
    install_requires=[
        'twitter',
        'pytz',
        'openpyxl',
    ],
    console=['twitarian.py']
)
