.PHONY: build clean

build:
	uvicorn main:app --reload
	