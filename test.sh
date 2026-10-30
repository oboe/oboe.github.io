#!/bin/bash
# Serve the site locally with live reload (see README.md).
cd "$(dirname "$0")"
bundle exec jekyll serve --livereload
