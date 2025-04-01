# coding = utf-8
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

extModules = [Extension("cclip", ["cclip.pyx"])]

setup(name="CClipExample", cmdclass={"build_ext": build_ext}, ext_modules=extModules)
