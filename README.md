# Renamer

Renames all files in a directory with an increasing number.

## usage

```
# on it's own defaults to $HOME/dwhelper/
numd
```

```
# rename all the files in the "~/example" directory with a numeric name, keeping
# the extension intact.
numd ~/example
```

```
# same as above, but start numbering at 100.
numd ~/example --start 100
```

```
# dry-run (report only, no changes made)
numd ~/example --dry-run
```

```
# choose width and add a prefix
numd ~/example --width 6 --prefix clip_
```

```
# randomise processing order before renaming
numd ~/example --randomise
```
