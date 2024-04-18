---
title: "About this website"
excerpt: "How this website was created"
collection: misc
permalink: /misc/website
date:  2024-04-18
---

I created this website in 2020 by forking [academicpages](https://academicpages.github.io/) (see this [post](/posts/2020/08/blog-post-1/)). I significantly updated it in 2024 to automate [publications](/publications/) and [talks](/talks/). This post is primarily intended for myself so that I don't forget, but it might be useful for others too.

1. Use [Markdown](https://www.markdownguide.org/) to write most posts.
1. For using \\(\LaTeX\\) in Markdown, use `\\(...\\)` for inline texts such as \\(\Pr(X>x)\sim x^{-\alpha}\\) and `\\[...\\]` for displayed texts such as
\\[\rho(\Pi\odot \Upsilon \odot \Psi(z)) = 1.\\]
1. To embed images, save the image file in `.png` format (you can use [this](https://pdf2png.com/) to convert from `.pdf` to `.png`), place it in the "assets" folder, and write
````
![<Some explanation>](/assets/<filename>.png)
````
in the Markdown file.
1. For creating a nice publication list, you need three components. The first is the Markdown files for each publication, say `2022-ECMA.md`, saved in the `_publication` folder. The second is the publication page, say `publications.html`, saved in the `_pages` folder. The third is the html file that specifies the format of including each publication file into the publication page. There could be various formats for published papers, working papers, etc. These files, such as `archive-wp.html` (for working papers), are saved in the `_includes` folder. To define different collections such as publications, working papers, talks, blog posts, etc., one needs to edit the `_config.yml` file.