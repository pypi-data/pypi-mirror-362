from setuptools import setup

setup(
    name='vislotan',
    version='0.0.4',
    description='Nir Lotan\'s visualization package',
    url='https://github.com/nlotan/vislotan',
    author='Nir Lotan',
    author_email='Nir.Lotan@intel.com',
    license='MIT License',
    packages=['vislotan'],
    install_requires=['plotly',
                      'pandas', 
                      'matplotlib',                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)