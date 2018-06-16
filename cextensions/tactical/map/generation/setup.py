from distutils.core import setup, Extension

module1 = Extension('TacticalMapGeneration',
                    sources = ['TacticalMapGeneration.c'])

setup (name = 'TacticalMapGeneration',
       ext_modules = [module1])