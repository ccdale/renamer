#!/bin/bash

# this script deletes all the files in the current directory
# generated during the package build process.

medir=${0%/*}
cd ${medir:-.}

# ensure we are in a directory called 'archlinux'
dname=$(basename $PWD)
if [ "$dname" != "archlinux" ]; then
    echo "ERROR: must be run from the 'archlinux' directory"
    exit 1
fi


# the 3 directories that may exist that we want to remove
# are 'src', 'pkg' and a copy of the repo
# the repo name should be the same name as the package
read xname xversion < <(poetry version)

xdirs=(src pkg ${xname})
for xdir in ${xdirs[@]}; do
    [ -d ${xdir} ] && rm -rf ${xdir}
done
