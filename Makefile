# Based on code from https://gitlab.com/keatontaylor/alexapy/blob/master/Makefile
coverage:
	Not implemented yet
	#pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=tvchannellist tests
bump:
	pipenv run semantic-release release
	pipenv run semantic-release changelog
bump_and_publish:
	pipenv run semantic-release publish
check_vulns:
	pipenv check
clean:
	rm -rf dist/ build/ .egg tvchannellist.egg-info/
init:
	pip3 install pip pipenv
	pipenv lock
	pipenv install --three --dev
lint: flake8 docstyle pylint typing isort black
flake8:
	pipenv run flake8 tvchannellist channellist
docstyle:
	pipenv run pydocstyle tvchannellist channellist
pylint:
	pipenv run pylint tvchannellist channellist
isort:
	pipenv run isort tvchannellist/*py channellist
black:
	pipenv run black tvchannellist/*py channellist
typing:
	pipenv run mypy --ignore-missing-imports tvchannellist channellist
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg tvchannellist.egg-info/
test:
	#Not implemented yet
	#pipenv run py.test

