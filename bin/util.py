from pybtex.database import parse_string as pybtex_parse_string


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


def read_bib(bib_path, strings_path):
    """Read bibliography and strings and convert."""
    bib = open(bib_path, "r").read()
    strings = open(strings_path, "r").read()
    bib = strings + "\n\n" + bib
    return pybtex_parse_string(bib, "bibtex").entries
