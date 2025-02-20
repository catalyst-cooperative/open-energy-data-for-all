# follow installation instructions here: https://carpentries.github.io/sandpaper-docs/index.html
# then run `Rscript build.R` - this will build the lesson and open in your browser.
sandpaper::package_cache_trigger(TRUE)
sandpaper::validate_lesson(path = '.')
sandpaper::build_lesson()
