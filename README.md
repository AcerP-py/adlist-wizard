# adlist-wizard
Wizard for working with adlists (made with pi-hole in mind).

## Features
- combine host-list files
- remove duplicates
- combine files from the web

## Current Version V1.1.0


### New Features
- rewrite of codebase
- combine files from the web

### Usage
```commandline
usage: alwiz [-h] [-v] [-o OUT] [-m {files,lists}] [-rd] [source ...]

positional arguments:
  source                list of input files/lists

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUT, --out OUT     output file
  -m {files,lists}, --mode {files,lists}
                        source mode
  -rd, --remove_duplicates
                        remove duplicates


```


## Building
Binary built with pyinstaller
```commandline
pyinstaller --name alwiz --onefile
```


## Contributing
Please feel free to open an issue for any bugs you find or
features you would like.
