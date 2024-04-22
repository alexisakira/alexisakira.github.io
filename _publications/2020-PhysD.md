---
title: "👍On the Emergence of a Power Law in the Distribution of COVID-19 Cases"
collection: publications
link: https://doi.org/10.1016/j.physd.2020.132649
venue: "Physica D: Nonlinear Phenomena"
date: 2020-11-01
history: https://alexisakira.github.io/publications/2020-PhysD
tags:
  - empirical
  - power law
coauthor: "Brendan K. Beare"
wpurl: https://arxiv.org/abs/2004.12772
code: https://github.com/alexisakira/COVID-19_power_law
excerpt: "👍(Power law, Empirical) Size distribution of COVID-19 cases across US counties as of March 2020 obeys the power law; empirical Pareto exponent is consistent with the estimated growth rate and age distributions."
---

In March 2020, I was working on [my paper](https://cepr.org/publications/covid-economics-issue-1) estimating the [SIR model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology) and obtained daily data on COVID-19 cases. I was naturally interested in the size distribution of COVID cases, and not surprisingly, it obeyed the power law. But what is cool about the COVID dataset is that it is a panel data that is updated daily. Because [Brendan](https://www.brendanbeare.com/) and I had been working on the generative mechanism of power laws based on random multiplicative growth and the distribution of age (for COVID, the number of days elapsed since the first case in the particular location), it was an ideal dataset to test the theory. The empirical Pareto exponent estimated from the cross-sectional data, \\(\hat{\zeta}=0.930\\), and the theoretical Pareto exponent implied by the random growth mechanism, \\(\zeta=0.928\\), are nearly identical.

Although the paper is simple and short, I consider it one of the best papers I have written. As far as I am aware, this is the only paper that provides direct evidence for random multiplicative growth as a generative mechanism of power laws.

![Log-log plot of confirmed COVID-19 cases](/assets/images/fig_Pareto_Cases.png)