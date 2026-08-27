---
title: "Coauthors"
excerpt: "A record of my coauthors and collaborative research."
collection: misc
permalink: /misc/coauthor
date: 2025-01-17
section: research
section_order: 3
---

<section class="coauthors-intro" aria-labelledby="coauthors-heading">
  <p id="coauthors-heading">Collaborators on my published research, listed alphabetically by last name.</p>
  <p class="coauthors-count">{{ site.data.coauthors | size }} coauthors</p>
</section>

<div class="coauthor-grid" role="list">
{% for coauthor in site.data.coauthors %}
  <div class="coauthor-card" role="listitem">
  {% if coauthor.url %}
    <a href="{{ coauthor.url }}">{{ coauthor.name }}</a>
  {% else %}
    <span>{{ coauthor.name }}</span>
  {% endif %}
  </div>
{% endfor %}
</div>

<style>
  .coauthors-intro {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    max-width: 54rem;
    margin-bottom: 1.35rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--global-border-color);
  }

  .coauthors-intro p {
    margin: 0;
  }

  .coauthors-intro > p:first-child {
    color: var(--global-text-color-light);
    line-height: 1.6;
  }

  .coauthors-count {
    flex: 0 0 auto;
    color: var(--global-link-color);
    font-size: 0.82em;
    font-weight: 700;
    white-space: nowrap;
  }

  .coauthor-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(12.5rem, 1fr));
    gap: 0.7rem;
    max-width: 54rem;
  }

  .coauthor-card {
    display: flex;
    align-items: center;
    min-height: 3.15rem;
    padding: 0.65rem 0.8rem;
    border: 1px solid var(--global-border-color);
    border-radius: 0.45rem;
    font-size: 0.93em;
    line-height: 1.35;
  }

  .coauthor-card a {
    color: var(--global-text-color) !important;
    font-weight: 650;
    text-decoration: none !important;
  }

  .coauthor-card a:hover {
    color: var(--global-link-color-hover) !important;
  }

  .coauthor-card a:focus-visible {
    outline: 3px solid var(--global-link-color);
    outline-offset: 3px;
  }

  @media (max-width: 540px) {
    .coauthors-intro {
      align-items: flex-start;
      flex-direction: column;
      gap: 0.45rem;
    }

    .coauthor-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
