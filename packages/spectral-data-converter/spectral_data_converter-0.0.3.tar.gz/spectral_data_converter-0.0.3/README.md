# spectral-data-converter
Python library for converting (and filtering) spectral data in various formats.

Some of the formats make use of the [wai_spectralio](https://github.com/waikato-datamining/wai-spectralio) 
library and some of the filters use the [wai_ma](https://github.com/waikato-datamining/py-matrix-algorithms) 
library for processing the data.

## Installation

Via PyPI:

```bash
pip install spectral_data_converter
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-datamining/spectral-data-converter.git
```

## Docker

Docker images are available as well. Please see the following page por more information:

https://github.com/waikato-datamining/spectral-data-converter-all/tree/main/docker


## Dataset formats

The following dataset formats are supported:

| Format                         | Read                          | Write                      | 
|:-------------------------------|:------------------------------|:---------------------------| 
| [ADAMS](formats/adams.md)      | [Y](plugins/from-adams.md)    | [Y](plugins/to-adams.md)   | 
| [ARFF](formats/arff.md)        | [Y](plugins/from-arff.md)     | [Y](plugins/to-arff.md)    | 
| [ASC](formats/asc.md)          | [Y](plugins/from-asc.md)      | [Y](plugins/to-asc.md)     | 
| [ASCII XY](formats/asciixy.md) | [Y](plugins/from-asciixy.md)  | [Y](plugins/to-asciixy.md) | 
| CAL (FOSS)                     | [Y](plugins/from-cal.md)      | [Y](plugins/to-cal.md)     | 
| CSV                            | [Y](plugins/from-csv.md)      | [Y](plugins/to-csv.md)     | 
| [DPT](formats/dpt.md)          | [Y](plugins/from-dpt.md)      | [Y](plugins/to-dpt.md)     | 
| MPS                            | [Y](plugins/from-mps.md)      | N                          | 
| NIR (FOSS)                     | [Y](plugins/from-nir.md)      | [Y](plugins/to-nir.md)     | 
| OPUS (Bruker)                  | [Y](plugins/from-opus.md)     | N                          | 
| OPUS Ext (Bruker)              | [Y](plugins/from-opus-ext.md) | N                          | 
| SPA (Thermo Scientific)        | [Y](plugins/from-spa.md)      | N                          | 


The following sample data formats are supported:

| Format                                  | Read                           | Write                        | 
|:----------------------------------------|:-------------------------------|:-----------------------------| 
| [ADAMS Report](formats/adams_report.md) | [Y](plugins/from-report-sd.md) | [Y](plugins/to-report-sd.md) | 
| CSV                                     | [Y](plugins/from-csv-sd.md)    | [Y](plugins/to-csv-sd.md)    | 
| JSON                                    | [Y](plugins/from-json-sd.md)   | [Y](plugins/to-json-sd.md)   | 


## Tools

### Dataset conversion

```
usage: sdc-convert [-h|--help|--help-all|--help-plugin NAME]
                   [-u INTERVAL] [-b|--force_batch] [--placeholders FILE] [--dump_pipeline FILE]
                   [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                   reader
                   [filter [filter [...]]]
                   [writer]

Tool for converting between spectral data formats.

readers (19):
   from-adams, from-arff, from-asc, from-asciixy, from-cal, from-csv, 
   from-csv-sd, from-dpt, from-json-sd, from-mps, from-multi, from-nir, 
   from-opus, from-opus-ext, from-pyfunc, from-report-sd, from-spa, 
   from-zip, poll-dir
filters (30):
   add-sampledata, apply-cleaner, center, check-duplicate-filenames, 
   discard-by-name, downsample, equi-distance, log, max-records, 
   metadata, metadata-from-name, metadata-to-placeholder, passthrough, 
   pca, pls1, pyfunc-filter, randomize-records, record-window, rename, 
   row-norm, sample, savitzky-golay, savitzky-golay2, set-placeholder, 
   simpls, spectrum-to-sampledata, split-records, 
   standard-normal-variate*, standardize, tee
writers (14):
   to-adams, to-arff, to-asc, to-asciixy, to-cal, to-csv, to-csv-sd, 
   to-dpt, to-json-sd, to-multi, to-nir, to-pyfunc, to-report-sd, 
   to-zip

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
  --dump_pipeline FILE
                        The file to dump the pipeline command in.
```

### Executing pipeline multiple times

```
usage: sdc-exec [-h] -p PIPELINE -g GENERATOR [-n] [-P PREFIX]
                [--placeholders FILE] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for executing a pipeline multiple times, each time with a different set
of variables expanded. A variable is surrounded by curly quotes (e.g.,
variable 'i' gets referenced with '{i}'). Available generators: dirs, list,
null, range

optional arguments:
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

Readers tend to support input via file lists. The `idc-find` tool can generate
these.

```
usage: sdc-find [-h] -i DIR [DIR ...] [-r] -o FILE [-m [REGEXP ...]]
                [-n [REGEXP ...]] [--split_ratios [SPLIT_RATIOS ...]]
                [--split_names [SPLIT_NAMES ...]]
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
  -m [REGEXP ...], --match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be included (default: None)
  -n [REGEXP ...], --not-match [REGEXP ...]
                        The regular expression that the (full) file names must
                        match to be excluded (default: None)
  --split_ratios [SPLIT_RATIOS ...]
                        The split ratios to use for generating the splits
                        (int; must sum up to 100) (default: None)
  --split_names [SPLIT_NAMES ...]
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
usage: sdc-help [-h] [-c [PACKAGE ...]] [-e EXCLUDED_CLASS_LISTERS]
                [-T {pipeline,generator}] [-p NAME] [-f {text,markdown}]
                [-L INT] [-o PATH] [-i FILE] [-t TITLE]
                [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for outputting help for plugins in various formats.

optional arguments:
  -h, --help            show this help message and exit
  -c [PACKAGE ...], --custom_class_listers [PACKAGE ...]
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
                        The title to use in the index file (default: spectral-
                        data-converter plugins)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Plugin registry

```
usage: sdc-registry [-h] [-c CUSTOM_CLASS_LISTERS] [-e EXCLUDED_CLASS_LISTERS]
                    [-l {plugins,pipeline,custom-class-listers,env-class-listers,readers,direct-readers,filters,writers,direct-writers,generators,cleaners}]

For inspecting/querying the registry.

options:
  -h, --help            show this help message and exit
  -c CUSTOM_CLASS_LISTERS, --custom_class_listers CUSTOM_CLASS_LISTERS
                        The comma-separated list of custom class listers to
                        use. (default: None)
  -e EXCLUDED_CLASS_LISTERS, --excluded_class_listers EXCLUDED_CLASS_LISTERS
                        The comma-separated list of class listers to exclude.
                        (default: None)
  -l {plugins,pipeline,custom-class-listers,env-class-listers,readers,direct-readers,filters,writers,direct-writers,generators,cleaners}, --list {plugins,pipeline,custom-class-listers,env-class-listers,readers,direct-readers,filters,writers,direct-writers,generators,cleaners}
                        For outputting various lists on stdout. (default:
                        None)
```

### Testing generators

```
usage: sdc-test-generator [-h] -g GENERATOR
                          [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Tool for testing generators by outputting the generated variables and their
associated values. Available generators: dirs, list, null, range

options:
  -h, --help            show this help message and exit
  -g GENERATOR, --generator GENERATOR
                        The generator plugin to use. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


## Plugins

You can find help screens for the plugins here:

* [Pipeline plugins](plugins/README.md) (readers/filters/writers)
* [Generator plugins](generators/README.md) (used by `sdc-exec`)
* [Cleaner plugins](cleaners/README.md) (used by `apply-cleaner` filter)


## Class listers

The *spectral-data-converter* uses the *class lister registry* provided 
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

* `SDC_CLASS_LISTERS`
* `SDC_CLASS_LISTERS_EXCL`

Each variable is a comma-separated list of `module_name:function_name`, defining the class listers.

## Additional libraries

* [Scikit-learn](https://github.com/waikato-datamining/image-dataset-converter-sklearn)
* [Visualizations](https://github.com/waikato-datamining/image-dataset-converter-vis)
