import subprocess
from cooolpackage.example import picture_generator
from functools import reduce


def execute(table):
    result ='''\\documentclass[a4paper,12pt,oneside]{scrbook}
\\usepackage{graphicx}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[ngerman]{babel}
\\usepackage[none]{hyphenat} % suppress hyphenation *globally*
\\sloppy
\\usepackage{tabularx,ragged2e}
\\newcommand{\\HY}{\\hyphenpenalty=25\\exhyphenpenalty=25}
\\newcolumntype{Z}{>{\\HY\\centering\\arraybackslash\\hspace{0pt}}X}
\\newcolumntype{M}{>{\\HY\\RaggedRight\\arraybackslash\\hspace{0pt}}c}
\\newcolumntype{L}{>{\\HY\\RaggedRight\\arraybackslash\\hspace{0pt}}l}

\\begin{document}
\\begin{tabularx}{\\linewidth}{|'''
    result += 'Z|' * len(table) + '}\n\\hline'
    result += reduce(
        lambda x, y: x + reduce(lambda t, u: t + ' & ' + u, y) + '\\\\\n\hline',
        table,
        ''
    )
    result += '''\n\\end{tabularx}
\\includegraphics[width=\\textwidth]{picture.png}
\\end{document}
    '''
    return result


if __name__ == '__main__':
    list_ = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    latex = execute(list_)
    with open('file.tex', 'w') as f:
        f.write(latex)
    picture_generator.get_ast_picture()
    subprocess.run('pdflatex file.tex')
