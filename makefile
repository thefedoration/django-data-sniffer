release:
	python setup.py sdist bdist_wheel

upload_test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	twine upload dist/*
