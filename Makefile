# Based on code from https://gitlab.com/keatontaylor/alexapy/blob/master/Makefile
coverage:
	Not implemented yet
	#py.test -s --verbose --cov-report term-missing --cov-report xml --cov=tvchannellist tests
bump:
	semantic-release release
	semantic-release changelog
bump_and_publish:
	semantic-release publish
check_vulns:
	pipenv check
clean:
	rm -rf dist/ build/ .egg tvchannellist.egg-info/
lint: flake8 docstyle pylint typing isort black
flake8:
	flake8 tvchannellist channellist
docstyle:
	pydocstyle tvchannellist channellist
pylint:
	pylint tvchannellist channellist
isort:
	isort tvchannellist/*py channellist
black:
	black tvchannellist/*py channellist
typing:
	mypy --ignore-missing-imports tvchannellist channellist
publish:
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist/ build/ .egg tvchannellist.egg-info/
test:
	#Not implemented yet
	#py.test

