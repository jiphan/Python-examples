# Python-examples

## yotsuba/

### config.py
- handles command line args
- pulls default flags from config.yaml

### yotsuba.py
- simple wrapper for basic api calls to yotsuba
- pulls flags from config.py

### calcActivity.py
- calculates thread activity formatted as (posts / 15 min)
- accepts backlinks for cross-thread calculation

### count Bumps.py
- board-level metrics
- `---loop` displays the time since last bump for the top thread on each page
- `--recent <n>` displays the time since last bump for last `n` threads
- `--bucket` displays the count of threads, grouped by time since last bump

### scanPosts.py
- comment-level filter
- returns posts matching thread and post regex
- `--refresh <n>` for scanning every `n` minutes