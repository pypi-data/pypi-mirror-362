from setuptools import setup, find_packages

setup(
	name='localgraph',
	version='0.1.1',
	author='Omar Melikechi',
	author_email='omar.melikechi@gmail.com',
	description='Local graph estimation with pathwise feature selection',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	packages=find_packages(include=["localgraph", "localgraph.*"]),
	install_requires=[
	'ipss>=1.1.1',
	'matplotlib>=3.0.0',
	'networkx>=2.0',
	'numpy>=1.16.0',
	],
	python_requires='>=3.6',
	include_package_data=True,
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
)
