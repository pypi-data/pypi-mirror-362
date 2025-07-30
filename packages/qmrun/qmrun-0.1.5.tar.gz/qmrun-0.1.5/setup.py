from setuptools import setup
with open("README.md","r",encoding="utf-8") as f:
    readme = f.read()

setup(
    name='qmrun',
    version='0.1.5',
    description='Orca6 input file generator from SDF files',
    url='https://github.com/NMRDev/qmrun',
    author='Armando Navarro-Vázquez',
    author_email='armando.navarro@ufpe.br',
    license='MIT',
    packages=['qmrun'],
    install_requires=['rdkit',
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'qmrun = qmrun:run',
        ]
    },

scripts=['bin/qmrun-orca6.ps1',
         'bin/qmrun-orca6',
         'bin/qmrun-orca6-stdout'],
long_description=readme, # A detailed description of the package
long_description_content_type="text/markdown", # The format of the long description
)
