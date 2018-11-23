PIPENV := pipenv run

publish:
	@rm -rf dist
	@$(PIPENV) python setup.py bdist_wheel --universal
	@$(PIPENV) twine upload dist/*
