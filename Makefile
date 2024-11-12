.PHONY: build clean
# Makefile for CanvasAIAssistant
# @author James Shima

build:
	@uvicorn main:app --reload

canvas:
	@./canvas.py

ed:
	@./ed.py