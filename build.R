#! /usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

if ("--help" %in% args || "-h" %in% args) {
  cat("Usage: Rscript build.R [--preview] [--help, -h]

Follow installation instructions here: https://carpentries.github.io/sandpaper-docs/index.html

Options:
  --preview    Open preview in browser after building
  --help, -h   Show this help message\n")
  quit(save = "no")
}

preview_flag <- "--preview" %in% args

sandpaper::package_cache_trigger(TRUE)
sandpaper::validate_lesson(path = '.')
sandpaper::build_lesson(preview = preview_flag)
