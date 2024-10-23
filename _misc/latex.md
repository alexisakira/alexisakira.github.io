---
title: "LaTeX"
excerpt: "Resources on LaTeX"
collection: misc
permalink: /misc/latex
date:  2024-10-22
---

\\(\LaTeX\\) is "the" standard document preparation system in economics and finance (and many other fields that are math-intensive, such as mathematics, physics, computer science, statistics, etc.).  Nowadays writing a paper without using \\(\LaTeX\\) will signal that your research is not serious, so all Ph.D. students seeking academic jobs should learn how to use \\(\LaTeX\\) at an early stage.  (A good commitment device is to typeset all homework assignments with \\(\LaTeX\\).)  The fixed cost of learning is high, but the marginal cost of creating complex documents is really low!  Since there are abundant online resources on \\(\LaTeX\\), I will list only a few links that I feel particularly useful.

## Small tips

1. [Overleaf](https://www.overleaf.com) is an online \\(\LaTeX\\) editor, which is my preferred choice when working online.
1. [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX) is an online tutorial for using \\(\LaTeX\\).
1. When you write research papers, you need to create a reference list. See [here](https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management) for how to manage the bibliography (I recommend BibLaTeX). [JabRef](http://www.jabref.org/) is a useful reference manager compatible with BibTeX.
1. When submitting papers to [arXiv](https://arxiv.org/), to allow line breaks within url, insert the line `\pdfoutput=1` in the preamble right after `\documentclass` in the .tex document. Also, when the TeX Live version of Overleaf and arXiv are different, `biblatex` may not compile properly. In that case, change the TeX Live version in Overleaf to a previous version by going to `Menu -> TeX Live version`.
1. [Here](/files/latextips.pdf) is a writing tip.
1. [TikZ](https://en.wikibooks.org/wiki/LaTeX/PGF/TikZ) lets you draw nice pictures. I also like the [tkz package](https://ctan.org/tex-archive/macros/latex/contrib/tkz) (especially tkz-euclide) for Euclidean geometry, though the documentation is in French.
1. The [moderncv package](https://ctan.org/tex-archive/macros/latex/contrib/moderncv) lets you create a nice CV.  What I especially like is that you can create arbitrary categories of reference lists and list them reverse-chronologically. For example, see [my CV](https://alexisakira.github.io/cv/). Click [here](/files/syllabus_template.zip) for a syllabus template based on this package.
1. The [exam package](https://ctan.org/tex-archive/macros/latex/contrib/exam) lets you write exams, with or without solutions.
1. See [here](https://tex.stackexchange.com/questions/837/pdf-letterhead-as-document-background) for how to write \\(\LaTeX\\) documents using official letterheads from your institution. Click [here](/files/university_letter_template.zip) for an example that uses the official Emory letterhead designed for the Economics Department.
1. [Here](/files/test.sty) is a style file that I use whenever I write papers.
1. For writing coauthored papers, [Overleaf](https://www.overleaf.com) is the simplest, though you need the paid version for more than two coauthors.
1. When you get stuck or want to do something with \\(\LaTeX\\) but don't know what or how to do, just google it.  Oftentimes the search will lead you to [LaTeX Stack Exchange](https://tex.stackexchange.com/), which is quite useful for resolving your questions.

## \\(\LaTeX\\) for Windows

1. [MiKTeX](https://miktex.org/) is a no-brainer \\(\LaTeX\\) distribution for Windows.
1. After installing MikTeX, open the MikTeX console and set path to your favorite folder that stores custom files (.sty, .bib, etc.).
1. Although any text editor can be used to create \\(\LaTeX\\) documents offline, there are many that are developed specifically for the use with \\(\LaTeX\\). See [here](https://en.wikipedia.org/wiki/Comparison_of_TeX_editors) for a comparison of various editors.  After experimenting with many of them, I have converged to [TeXstudio](https://texstudio.org/).

## \\(\LaTeX\\) for Mac

1. [MacTeX](https://www.tug.org/mactex/) is a no-brainer \\(\LaTeX\\) distribution for Mac.
1. After installing MacTeX, go to [this page](https://github.com/amunn/make-local-texmf) and run ``make-local-texmf`` to create a local texmf folder that stores custom files (.sty, .bib, etc.).
1. In TeXShop, the default BibTeX engine is bibtex. To use biber, go to ``TeXShop -> Settings -> Engine`` and type ``biber`` in BibTeX Engine. Finally, to compile documents with a single command-T, write ``% !TEX TS-program = pdflatexmk`` at the first line of the .tex document.

## `biblatex`

I find `biblatex` to be the most convenient way to compile a bibliography because there is so much freedom in customization. Below is my format for writing economics papers.

````
\usepackage[style=ext-authoryear-comp,
sorting=nyt,
dashed=false, % don't use dash for repeated author
maxcitenames=2, % maximum names to cite in text
maxbibnames=99, % maximum names to list in reference
uniquelist=false,
uniquename=false,
giveninits=true, % first name initials
natbib, % use natbib commands
date=year % year only
]{biblatex}

\AtBeginRefsection{\GenRefcontextData{sorting=ynt}}
\AtEveryCite{\localrefcontext[sorting=ynt]}

\DeclareFieldFormat{pages}{#1} % suppress pp.
\renewbibmacro{in:}{\ifentrytype{article}{}{\printtext{\bibstring{in}\intitlepunct}}} % delete In:

\DeclareFieldFormat[article,inbook,incollection,inproceedings,patent,thesis,unpublished]{titlecase:title}{\MakeSentenceCase*{#1}} % change title to sentence case

\addbibresource{<filename>.bib}

\printbibliography

````