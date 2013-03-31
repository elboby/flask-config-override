#!/usr/bin/env python

from distutils.core import setup


with open('README.md') as file:
    long_description = file.read()

setup(
    name='Flask-Config-Override',
    version='0.0.2',
    url='https://github.com/elboby/flask-config-override',
    author='Arnaud Seilles',
    author_email='arnaud.seilles@gmail.com',
    packages=['flask_config_override', 'flask_config_override.test'],
    license='BSD',
    description='Override Flask configuration via Cookie at runtime.',
    long_description=long_description,
    install_requires=open('requirements.pip').readlines(),
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=[
        'nose>=1.0',
    ],
    test_suite='nose.collector',
)
