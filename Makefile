JEKYLL=bundle exec jekyll
POSTS:=$(wildcard _posts/*/*.html) $(wildcard _posts/*/*.md)

.DEFAULT: commands

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
build:
	${JEKYLL} build

## serve: build site and run server
serve:
	${JEKYLL} serve

## data: rebuild data files
data: _data/authors.yml _data/categories.yml

_data/authors.yml: bin/from_bib.py bin/util.py tex/nwit.bib tex/strings.bib tex/unreviewed.txt
	@mkdir -p _data
	@python bin/from_bib.py --bib tex/nwit.bib --strings tex/strings.bib --unreviewed tex/unreviewed.txt > $@

_data/categories.yml: bin/from_posts.py bin/util.py $(POSTS)
	@mkdir -p _data
	@python bin/from_posts.py --prefix _posts $(POSTS) > $@
