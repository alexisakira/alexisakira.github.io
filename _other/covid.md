---
title: "Susceptible-Infected-Recovered (SIR) Dynamics of COVID-19 and Economic Impact"
collection: other
link: https://cepr.org/publications/covid-economics-issue-1
venue: Covid Economics, Vetted and Real-Time Papers
date: 2020-04-03
history: https://alexisakira.github.io/other/covid
slides: https://alexisakira.github.io/files/slides/slides_covid19.pdf
---

After returning from my UK trip in early March 2020, just a few days before the closure of the border, I got interested in COVID-19, like many of us. I played around with some models and I derived a system of differential equations that turned out to be identical to the [Kermack & McKendrick (1927)](https://doi.org/10.1098/rspa.1927.0118) [susceptible-infected-recovered (SIR) model](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology). I searched the literature and found the closed-form solution by [Harko et al. (2014)](10.1016/j.amc.2014.03.030). At that time, little was known about COVID-19, so I decided to estimate the epidemiological parameters from data to predict the epidemic dynamics.

In mid March 2020, the state of California imposed lockdown, my kids' school suddenly closed (teachers were not yet used to online teaching, so education was *laissez faire* to parents), tennis courts closed, and we could no longer eat at restaurants. I thought this was all wrong. I have a medical degree and knew about herd immunity, so just shutting down everything would simply delay the problem without solving it, while imposing significant economic costs to the society. So for the first time in my career as a researcher, I worked on a project not just driven by scientific curiosity but also by a sense of civic duty to inform the public and policy makers.

According to my analysis in the figure below, imposing an early (and necessarily temporary) lockdown would simply delay the spread of the epidemic without affecting the ultimate toll.

![Early mitigation](/assets/images/covid_benchmark.png)

However, if the government delays intervention until about 1% of the population is infected, it would significantly reduce the total cumulative number of infections due to the build up of herd immunity, as the following figure shows.

![Early mitigation](/assets/images/covid_optimal.png)

The analysis was of course not perfect, but because I thought the problem was urgent, I submitted this paper to AER: Insights on March 26, 2020. I presented the paper at the UCSD Econometrics seminar on March 31, 2020, and the paper was included in the first issue of the working paper series [Covid Economics](https://cepr.org/publications/covid-economics-issue-1). It was also featured in the [April 2020 VoxEU](https://voxeu.org/article/early-draconian-social-distancing-may-be-suboptimal-fighting-covid-19-epidemic#) and [May 2020 Fortune](https://fortune.com/2020/05/04/reopening-reopen-economy-coronavirus-covid-19-lifting-lockdown-economists) articles. This paper is by far my most cited paper. Unfortunately, AER: Insights rejected my paper in May 2020, by which time so many things have changed and there was so much competition, so I gave up the project.

After this experience, I started to question the relevance of traditional economics research. I felt that the long review process at typical economics journals prevents researchers from working on pressing issues. Of course, one could write a sophisticated paper after the pandemic is long gone (instead of writing a preliminary paper in a few weeks), but what is the benefit to the society? I also felt that most COVID papers written by economists encouraged lockdown and sided with increased government control, perhaps because researchers wanted to play the good guy. Later, I published a more [sophisticated paper](https://doi.org/10.1016/j.jet.2022.105570) in JET.