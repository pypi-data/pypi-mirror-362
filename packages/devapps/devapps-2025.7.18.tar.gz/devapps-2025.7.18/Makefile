.DEFAULT_GOAL := help
SHELL := bash

DUTY = $(shell [ -n "${VIRTUAL_ENV}" ] || echo poetry run) duty

BASIC_DUTIES = \
	clean \
	combine \
	coverage \
	docs \
	docs-deploy \
	docs-regen \
	docs-serve \
	format \
	badges \
	release

QUALITY_DUTIES = \
	check \
	check-code-quality \
	check-dependencies \
	check-docs \
	check-types \
	ci \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: setup
setup:
	@bash scripts/setup.sh

.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	@bash scripts/multirun.sh duty $@

