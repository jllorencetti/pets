lint:
	pre-commit run -a -v

test:
	cd pets/ && pipenv run ./manage.py test
