#!/usr/bin/env python

"""Construct table of articles by author."""

import argparse
from pybtex.database import parse_string as pybtex_parse_string
import sys
import yaml


LATEX_CHARS = (
    ('---', '—'),
    (r"\`{A}", 'À'),
    (r"\`{E}", 'È'),
    (r"\'{E}", 'É'),
    (r"\'{S}", 'Ś'),
    (r"\'{a}", 'á'),
    (r"\'{c}", 'ć'),
    (r"\`{a}", 'à'),
    (r"\`{e}", 'è'),
    (r"\'{e}", 'é'),
    (r"\'{i}", 'í'),
    (r"\'{o}", 'ó'),
    (r"\'{u}", 'ú'),
    (r"\'{\i}", 'í'),
    (r'\"{a}', 'ä'),
    (r'\"{o}', 'ö'),
    (r'\"{u}', 'ü'),
    (r'\'{O}', 'Ó'),
    (r'\'{o}', 'ó'),
    (r'\c{C}', 'Ç'),
    (r'\c{c}', 'ç'),
    (r'\v{S}', 'Š'),
    (r'\v{e}', 'ě'),
    (r'\v{r}', 'ř'),
    (r'\v{s}', 'š'),
    (r'\v{z}', 'ž'),
    (r'\~{a}', 'ã'),
    (r'\~{n}', 'ñ'),
    (r'{\AA}', 'Å'),
    (r'{\aa}', 'å'),
    (r'{\o}', 'ø'),
    (r'\%', '%'),
    (r'\#', '#'),
    (r'${\approx}$', '≈'),
    (r'${\pm}$', '±'),
    (r'${\times}$', '×'),
    (r'\textquotesingle', "'"),
    (r'\textquotedblleft', "'"),
    (r'\textquotedblright', "'"),
    (r'{\ldots}', '…'),
    (r'{\textemdash}', '—'),
    (r'{\textendash}', '–'),
    ('{', ''),
    ('}', ''),
    ('\$', '$'),
    ('\\', ''),
    ('  ', ' '),
    ('&', '&amp;'),
    ('<', '&lt;'),
    ('>', '&gt;')
)


def main():
    config = _parse_args()
    bib = _read_bib(config)
    unreviewed = _read_unreviewed(config)
    bib = _remove_unreviewed(bib, unreviewed)

    authors = _by_author(bib)
    with open(config.authors, "w") as writer:
        yaml.dump(authors, writer)


def _clean(name):
    name = str(name)
    for (latex, html) in LATEX_CHARS:
        name = name.replace(latex, html)
    return name


def _by_author(bib):
    """Convert entries to YAML of authors and entries."""
    authors = {}

    for key in sorted(bib.keys()):
        reviewed = bib[key].fields["reviewed"]
        for p in bib[key].persons:
            for name in bib[key].persons[p]:
                authors.setdefault(_clean(name), set()).add((key, reviewed))

    return {a: [{r[0]:r[1]} for r in sorted(authors[a])] for a in authors}


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--authors", help="Output authors YAML file")
    parser.add_argument("--bib", help="Bibliography BibTeX file")
    parser.add_argument("--strings", help="String definitions BibTeX file")
    parser.add_argument("--unreviewed", help="Plaintext file with keys of unreviewed items")
    return parser.parse_args()


def _read_bib(config):
    """Read bibliography and strings and convert."""
    bib = open(config.bib, "r").read()
    strings = open(config.strings, "r").read()
    bib = strings + "\n\n" + bib
    return pybtex_parse_string(bib, "bibtex").entries


def _read_unreviewed(config):
    """Read keys of unreviewed bibliography entries."""
    lines = open(config.unreviewed, "r").readlines()
    lines = [ln.strip() for ln in lines]
    return {ln for ln in lines if ln}


def _remove_unreviewed(bib, unreviewed):
    """Remove unreviewed items from bibliography."""
    return {k:bib[k] for k in bib.keys() if k not in unreviewed}


if __name__ == "__main__":
    main()
