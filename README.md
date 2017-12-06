This repository is for command line utilities that I find useful. Maybe you will too.


### spill
This command line utility "spills" the contents of a directory into another. By default
the target directory is that in which the source directory exists.

    `spill some/path/garbage`

will move all of the contents of the directory `garbage` into `some/path` and will
then delete the directory `garbage` if it has become empty.

    `spill some/path/garbage ~/trash`

will move the contetns of `garbage` into `~/trash` instead of `some/path`

To create a binary: 

`cp spill.py spill.pyx`
`cython spill.pyx --embed`
`gcc -Os -I /usr/include/python3.6m -o spill spill.pyx -lpython3.6m -lpthread -lm -lutil -ldl`
