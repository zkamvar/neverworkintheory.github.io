_data/authors.yml: bin/authors.py tex/nwit.bib tex/strings.bib tex/unreviewed.txt
	mkdir -p _data
	python bin/authors.py --authors $@ --bib tex/nwit.bib --strings tex/strings.bib --unreviewed tex/unreviewed.txt
