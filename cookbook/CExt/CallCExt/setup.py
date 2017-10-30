# coding = utf-8
from distutils.core import setup, Extension

setup \
(
	name = "callcext",
	ext_modules = \
	[
		Extension \
		(
			"callcext",
			["callcext.c"],
			include_dirs = [r"..\CExt", r"C:\intel\Python35\include"],
			library_dirs = [r"..\x64\Release", r"C:\intel\Python35\libs"],
			libraries = ["cext", "python35"], # 引用的库名
			define_macros = [("CALL_C_EXT", "1")],
			undef_macros = None
		)
	]
)
