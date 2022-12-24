#!/usr/bin/env python

"""Construct table of articles by author."""

import argparse
import sys
import yaml


from util import LATEX_CHARS, read_bib


def main():
    """Main driver."""
    config = _parse_args()
    bib = read_bib(config.bib, config.strings)
    unreviewed = _read_unreviewed(config)
    bib = _remove_unreviewed(bib, unreviewed)

    authors = _by_author(bib)
    yaml.dump(authors, sys.stdout)


def _clean(text):
    """Clean up LaTeX characters in a string."""
    text = str(text)
    for (latex, html) in LATEX_CHARS:
        text = text.replace(latex, html)
    return text


def _by_author(bib):
    """Convert entries to YAML of 'author' => [{'date', 'key', 'reviewed'}]."""
    accum = {}

    for key in sorted(bib.keys()):
        reviewed = bib[key].fields["reviewed"]
        for p in bib[key].persons:
            for name in bib[key].persons[p]:
                date = "-".join(reviewed.split("/")[1:4])
                accum.setdefault(_clean(name), set()).add((date, key, reviewed))

    result = []
    for name in sorted(accum.keys()):
        entries = list(sorted(accum[name]))
        entries = [{"date": i[0], "key": i[1], "reviewed": i[2]} for i in entries]
        result.append({"name": name, "entries": entries})
        
    return result


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--bib", help="Bibliography BibTeX file")
    parser.add_argument("--strings", help="String definitions BibTeX file")
    parser.add_argument("--unreviewed", help="Plaintext file with keys of unreviewed items")
    return parser.parse_args()


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
