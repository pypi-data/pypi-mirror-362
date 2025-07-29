#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version = 1.2.13
European Space Agency (ESA)
European Space Research and Technology Centre (ESTEC)
Keplerlaan 1, 2201 AZ Noordwijk, The Netherlands
Email: maximilian.guenther@esa.int
GitHub: mnguenther
Twitter: m_n_guenther
Web: www.mnguenther.com
"""

from setuptools import setup, find_packages





setup(
    name = 'alexfitter',
    packages = find_packages(),
version = "1.2.19",
    description = 'A global inference framework for photometry and RV',
    author = 'Maximilian N. Günther & Tansu Daylan',
    author_email = 'maximilian.guenther@esa.int',
    url = 'https://github.com/MNGuenther/allesfitter',
    download_url = 'https://github.com/MNGuenther/allesfitter',
    license='MIT',
    classifiers=['Development Status :: 5 - Production/Stable', #3 - Alpha / 4 - Beta / 5 - Production/Stable
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python'],
    #install_requires=['numpy>=1.10'],
    include_package_data = True
    )



