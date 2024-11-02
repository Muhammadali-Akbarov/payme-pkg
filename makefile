upload:
	rm -rf ./dist/*
	python setup.py sdist
	twine upload dist/*

upload_retry:
	twine upload dist/*