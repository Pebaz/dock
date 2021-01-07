from setuptools import setup

setup(
	name='dock-python',
	version='0.1.0',
	author='https://github.com/Pebaz',
	py_modules=['dock'],
	entry_points={
		'console_scripts' : [
			'dock=dock:cli'
		]
	}
)
