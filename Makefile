venv: venv/touchfile

venv/touchfile: requirements.txt
ifeq ($(wildcard ./venv/.*),)
	@echo "Did not find ./venv directory, creating.."
	mkdir ./venv
endif
	python3 -m venv ./venv
	./venv/bin/pip install -Ur requirements.txt
	touch ./venv/touchfile

lint:
	./venv/bin/pylint --rcfile .pylintrc $(shell git ls-files '*.py')

test:
	./venv/bin/python test.py

clean_cache:
	find . -type d -name __pycache__ -exec rm -r {} \+

clean: clean_cache
	rm -rf ./venv