from setuptools import setup

setup(
	name='balikAvla',
	version='1.0',
	url='https://github.com/mulosbron/balikAvla',
	author='mulosbron',
	author_email='mulosbron@gmail.com',
	description='balık yakalama oyunu',
	install_requires=[
		'pygame',
		'random',
		'mysql.connector',
		'datetime',
	],
	py_modules=['balikAvlamaOyunu', 'dbSkorlar'],
)
