CV_FILE ?= Soheil_Koohi_CV.yaml
RENDERCV_VERSION ?= 2.8

.PHONY: all build linkedin open watch install clean

all: build

## build: render the CV and assemble site/
build:
	@CV_FILE=$(CV_FILE) RENDERCV_VERSION=$(RENDERCV_VERSION) ./scripts/build.sh

## linkedin: render the LinkedIn profile copy to linkedin/preview.html
linkedin:
	@python3 linkedin/build.py linkedin/preview.html

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
	@rm -rf rendercv_output site linkedin/preview.html linkedin/__pycache__
	@echo "cleaned"
