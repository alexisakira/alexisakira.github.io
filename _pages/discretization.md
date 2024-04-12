---
layout: archive
title: "Discretization"
permalink: /discretization/
author_profile: true
---

{% include base_path %}

I have written several papers (Tanaka & Toda, [2013](http://doi.org/10.1016/j.econlet.2012.12.020), [2015](http://doi.org/10.1137/140971269); Farmer & Toda, [2017](https://doi.org/10.3982/QE737); Toda, [2021](https://doi.org/10.1007/s10614-020-10012-6)) on discretizing probability distributions and stochastic processes.

I have compiled the discretization codes in a [Matlab package](https://github.com/alexisakira/discretization) that allows the user to:
- discretize a VAR(1) with Gaussian shocks,
- discretize an AR(p) process with Gaussian mixture shocks,
- discretize an AR(1) with log AR(1) stochastic volatility,
- discretize the [Cox-Ingersoll-Ross model](https://en.wikipedia.org/wiki/Cox%E2%80%93Ingersoll%E2%80%93Ross_model),
- calibrate a discrete distribution directly from data.

The package also contains a [tutorial](https://github.com/alexisakira/discretization/blob/master/discretization.pdf) on how to write your own discretization codes. If you find any bugs or you have other processes that you would like to be discretized, please let me know by email. 
