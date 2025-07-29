# audio-dataset-converter
For converting audio datasets from one format into another.
Filters can be supplied as well, e.g., for cleaning up the data.


## Installation

Via PyPI:

```bash
pip install audio-dataset-converter
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-llm/audio-dataset-converter.git
```


## Docker

Docker images are available as well. Please see the following page por more information:

https://github.com/waikato-llm/audio-dataset-converter-all/tree/main/docker


## Dataset formats

The following dataset formats are supported:

| Domain         | Format                                                       | Read | Write | 
|:---------------|:-------------------------------------------------------------|:-----|:------| 
| Classification | [ADAMS](formats/adams.md)                                    | Y    | Y     | 
| Classification | [subdir](formats/subdir.md)                                  | Y    | Y     | 
| Classification | [TXT](formats/txt.md)                                        | Y    | Y     | 
| Speech         | [ADAMS](formats/adams.md)                                    | Y    | Y     | 
| Speech         | [CommonVoice](formats/commonvoice.md)                        | Y    | Y     | 
| Speech         | [Festvox](formats/festvox.md)                                | Y    | Y     | 
| Speech         | [Hugginface AudioFolder](formats/huggingface_audiofolder.md) | Y    | Y     | 
| Speech         | [TXT](formats/txt.md)                                        | Y    | Y     | 


## Tools

### Dataset conversion

```
usage: adc-convert [-h|--help|--help-all|--help-plugin NAME]
                   [-u INTERVAL] [-b|--force_batch] [--placeholders FILE]
                   [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   reader
                   [filter [filter [...]]]
                   [writer]

Tool for converting between audio dataset formats.

readers (12):
   from-adams-ac, from-adams-sp, from-commonvoice-sp, from-data, 
   from-festvox-sp, from-hf-audiofolder-sp, from-multi, from-pyfunc, 
   from-subdir-ac, from-txt-ac, from-txt-sp, poll-dir
filters (23):
   check-duplicate-filenames, convert-to-mono, convert-to-wav, 
   discard-by-name, discard-negatives, max-records, metadata, 
   metadata-from-name, metadata-to-placeholder, passthrough, 
   pitch-shift, pyfunc-filter, randomize-records, record-window, rename, 
   resample, sample, set-placeholder, split-records, strip-annotations, 
   tee, time-stretch, trim-silence
writers (12):
   to-adams-ac, to-adams-sp, to-audioinfo, to-commonvoice-sp, to-data, 
   to-festvox-sp, to-hf-audiofolder-sp, to-multi, to-pyfunc, 
   to-subdir-ac, to-txt-ac, to-txt-sp

optional arguments:
  -h, --help            show basic help message and exit
  --help-all            show basic help message plus help on all plugins and exit
  --help-plugin NAME    show help message for plugin NAME and exit
  -u INTERVAL, --update_interval INTERVAL
                        outputs the progress every INTERVAL records (default: 1000)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        the logging level to use (default: WARN)
  -b, --force_batch     processes the data in batches
  --placeholders FILE
                        The file with custom placeholders to load (format: key=value).
```

### Executing pipeline multiple times

```
usage: adc-exec [-h] -p PIPELINE -g GENERATOR [-n] [-P PREFIX]
                [--placeholders FILE] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for executing a pipeline multiple times, each time with a different set
of variables expanded. A variable is surrounded by curly quotes (e.g.,
variable 'i' gets referenced with '{i}'). Available generators: dirs, list,
null, range

options:
  -h, --help            show this help message and exit
  -p PIPELINE, --pipeline PIPELINE
                        The pipeline template with variables to expand and
                        then execute. (default: None)
  -g GENERATOR, --generator GENERATOR
                        The generator plugin to use. (default: None)
  -n, --dry_run         Applies the generator to the pipeline template and
                        only outputs it on stdout. (default: False)
  -P PREFIX, --prefix PREFIX
                        The string to prefix the pipeline with when in dry-run
                        mode. (default: None)
  --placeholders FILE   The file with custom placeholders to load (format:
                        key=value). (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Locating files

Readers tend to support input via file lists. The `adc-find` tool can generate
these.

```
usage: adc-find [-h] -i DIR [DIR ...] [-r] -o FILE [-m [REGEXP [REGEXP ...]]]
                [-n [REGEXP [REGEXP ...]]]
                [--split_ratios [SPLIT_RATIOS [SPLIT_RATIOS ...]]]
                [--split_names [SPLIT_NAMES [SPLIT_NAMES ...]]]
                [--split_name_separator SPLIT_NAME_SEPARATOR]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for locating files in directories that match certain patterns and store
them in files.

optional arguments:
  -h, --help            show this help message and exit
  -i DIR [DIR ...], --input DIR [DIR ...]
                        The dir(s) to scan for files. (default: None)
  -r, --recursive       Whether to search the directories recursively
                        (default: False)
  -o FILE, --output FILE
                        The file to store the located file names in (default:
                        None)
  -m [REGEXP [REGEXP ...]], --match [REGEXP [REGEXP ...]]
                        The regular expression that the (full) file names must
                        match to be included (default: None)
  -n [REGEXP [REGEXP ...]], --not-match [REGEXP [REGEXP ...]]
                        The regular expression that the (full) file names must
                        match to be excluded (default: None)
  --split_ratios [SPLIT_RATIOS [SPLIT_RATIOS ...]]
                        The split ratios to use for generating the splits
                        (int; must sum up to 100) (default: None)
  --split_names [SPLIT_NAMES [SPLIT_NAMES ...]]
                        The split names to use as filename suffixes for the
                        generated splits (before .ext) (default: None)
  --split_name_separator SPLIT_NAME_SEPARATOR
                        The separator to use between file name and split name
                        (default: -)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Generating help screens for plugins

```
usage: adc-help [-h] [-c [PACKAGE [PACKAGE ...]]] [-e EXCLUDED_CLASS_LISTERS]
                [-T {pipeline,generator}] [-p NAME] [-f {text,markdown}]
                [-L INT] [-o PATH] [-i FILE] [-t TITLE]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for outputting help for plugins in various formats.

optional arguments:
  -h, --help            show this help message and exit
  -c [PACKAGE [PACKAGE ...]], --custom_class_listers [PACKAGE [PACKAGE ...]]
                        The custom class listers to use, uses the default ones
                        if not provided. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -T {pipeline,generator}, --plugin_type {pipeline,generator}
                        The types of plugins to generate the help for.
                        (default: pipeline)
  -p NAME, --plugin_name NAME
                        The name of the plugin to generate the help for,
                        generates it for all if not specified (default: None)
  -f {text,markdown}, --help_format {text,markdown}
                        The output format to generate (default: text)
  -L INT, --heading_level INT
                        The level to use for the heading (default: 1)
  -o PATH, --output PATH
                        The directory or file to store the help in; outputs it
                        to stdout if not supplied; if pointing to a directory,
                        automatically generates file name from plugin name and
                        help format (default: None)
  -i FILE, --index_file FILE
                        The file in the output directory to generate with an
                        overview of all plugins, grouped by type (in markdown
                        format, links them to the other generated files)
                        (default: None)
  -t TITLE, --index_title TITLE
                        The title to use in the index file (default: audio-
                        dataset-converter plugins)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Plugin registry

```
usage: adc-registry [-h] [-c CUSTOM_CLASS_LISTERS] [-e EXCLUDED_CLASS_LISTERS]
                    [-l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}]

For inspecting/querying the registry.

optional arguments:
  -h, --help            show this help message and exit
  -c CUSTOM_CLASS_LISTERS, --custom_class_listers CUSTOM_CLASS_LISTERS
                        The comma-separated list of custom class listers to
                        use. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -l {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}, --list {plugins,pipeline,custom-class-listers,env-class-listers,readers,filters,writers,generators}
                        For outputting various lists on stdout. (default:
                        None)
```

### Testing generators

```
usage: adc-test-generator [-h] -g GENERATOR
                          [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for testing generators by outputting the generated variables and their
associatd values. Available generators: dirs, list, null, range

optional arguments:
  -h, --help            show this help message and exit
  -g GENERATOR, --generator GENERATOR
                        The generator plugin to use. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


## Plugins

You can find help screens for the plugins here:

* [Pipeline plugins](plugins/README.md) (reades/filters/writers)
* [Generator plugins](generators/README.md) (used by `adc-exec`)


## Command-line examples

Examples can be found on the [audio-dataset-converter-examples](https://waikato-llm.github.io/audio-dataset-converter-examples/)
website.


## Class listers

The *adc-dataset-converter* uses the *class lister registry* provided 
by the [seppl](https://github.com/waikato-datamining/seppl) library.

Each module defines a function, typically called `list_classes` that returns
a dictionary of names of superclasses associated with a list of modules that
should be scanned for derived classes. Here is an example:

```python
from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "mod.ule1",
            "mod.ule2",
        ],
        "seppl.io.Filter": [
            "mod.ule3",
            "mod.ule4",
        ],
        "seppl.io.Writer": [
            "mod.ule5",
        ],
    }
```

Such a class lister gets referenced in the `entry_points` section of the `setup.py` file:

```python
    entry_points={
        "class_lister": [
            "unique_string=module_name:function_name",
        ],
    },
```

`:function_name` can be omitted if `:list_classes`.

The following environment variables can be used to influence the class listers:

* `ADC_CLASS_LISTERS`
* `ADC_CLASS_LISTERS_EXCL`

Each variable is a comma-separated list of `module_name:function_name`, defining the class listers.


## Additional libraries

* [Faster whisper](https://github.com/waikato-llm/audio-dataset-converter-faster-whisper)
* [Redis](https://github.com/waikato-llm/audio-dataset-converter-redis)
* [Visualization](https://github.com/waikato-llm/audio-dataset-converter-visualization)
