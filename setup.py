from setuptools import setup, find_packages

setup(
        name='probablyhow',
        version='0.0.1',
        py_modules='howto.py',
        packages=find_packages(),
        install_requires=[
            'markovify',
            'BeautifulSoup'
            ],
        entry_points={
            'console_scripts': [
                'howto = probablyhow:howto'
                ]
            },
        )
