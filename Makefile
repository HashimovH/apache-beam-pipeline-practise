# Simple Makefile for Windows users (requires `make` from Git for Windows or similar)

.PHONY: test-unit

test-unit:
	pytest -q tests/unit -c setup.cfg
