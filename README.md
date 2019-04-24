# Usage

```
usage: gen_sim [-h] [-d DURATION] [-m MODEL] [-f FILE] [-D DIR] [-o OUTFILE]

Fire simulator animation generator

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        Duration for each frame of the gif in milliseconds
  -m MODEL, --model MODEL
                        A string representing the model. e.g. "[[2, 2], [2,
                        2]], [[1, 1], [1, 1]], 1, 'N', [(0, 0)]"
  -f FILE, --file FILE  A filename containing output filenames (optional) and
                        models (one per line) of the form filename:model
  -D DIR, --dir DIR     A directory to save output files to
  -o OUTFILE, --outfile OUTFILE
                        Output .gif file
```
