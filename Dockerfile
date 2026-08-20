FROM ruby:3.2-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
