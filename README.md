# adlist-wizard
Wizard for working with adlists (made with pi-hole in mind).

## Features
- combine host-list files
- remove duplicates

## Current Version V1.0.0
Version v1.0.0 is here!

### New Features
- combine space separated list of host-list files
- remove duplicates

### Options
Example:
```commandline
alwiz --rd --out /home/user/myadlist.list list1 list2 ...
```
- --out
  - the file to write to \[default: adlist.list]
- --rd
  - removes duplicates


## Building
Binary built with pyinstaller
```commandline
pyinstaller ./src/alwiz.py --name alwiz --onefile
```


## Contributing
Please feel free to open an issue for any bugs you find or
features you would like.
