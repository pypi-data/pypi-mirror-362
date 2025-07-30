from setuptools import setup

setup(
    name='mimicx',
    version='0.1.6',    
    description='MimicX AI',
    url='https://github.com/Mimicx-AI/pip-package',
    author='Hamadi Camara',
    author_email='hamadi.camara@mimicx.ai',
    license='MIT',
    packages=['mimicx'],
    install_requires=['mpi4py>=2.0',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)