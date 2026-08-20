CV_FILE ?= Soheil_Koohi_CV.yaml
RENDERCV_VERSION ?= 2.8

.PHONY: all build open watch install clean

all: build

## build: render the CV and assemble site/
build:
	@CV_FILE=$(CV_FILE) RENDERCV_VERSION=$(RENDERCV_VERSION) ./scripts/build.sh

## open: build then open the PDF (macOS)
open: build
	@open rendercv_output/$(basename $(CV_FILE)).pdf

## watch: re-render automatically on every save of the YAML
watch:
	@rendercv render $(CV_FILE) --watch

## install: install a pinned rendercv via uv
install:
	@uv tool install --python 3.12 "rendercv[full]==$(RENDERCV_VERSION)"

## clean: remove build output
clean:
	@rm -rf rendercv_output site
	@echo "cleaned"
