#!/usr/bin/env python

import argparse
import frontmatter
import sys
import yaml


def main():
    config = _parse_args()
    categories = _get_categories(config)
    yaml.dump(categories, sys.stdout)


def _get_categories(config):
    """Extract post categories."""
    result = {}
    for filename in config.posts:
        info = frontmatter.load(filename)
        if "categories" not in info:
            print(f"{filename} has no categories", file=sys.stderr)
        else:
            stripped = filename.replace(config.prefix, "", 1).replace(".md", ".html")
            for cat in info["categories"]:
                result.setdefault(cat, list()).append(stripped)
    return result


def _parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", help="Path prefix to remove from filenames")
    parser.add_argument("posts", nargs="+", help="Paths to blog posts")
    return parser.parse_args()


if __name__ == '__main__':
    main()
