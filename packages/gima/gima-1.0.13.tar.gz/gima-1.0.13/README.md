# gima

`gima` is a `Python` software which simplifies managing many git repositories through the console. It stands for `GI`t `MA`nager.

`gima` is intended to make it easy to `commit`, `pull` and `push` changes for many repositories with easy console interface. The goal of `gima` is not to replace any git client.


## Installation

To install `gima` type in the console:

```
pip install gima
```

To upgrade `gima` type in the console:

```
pip install gima --upgrade
```

## Usage

Type in the console:

```
gima
```

and you should see:

```
gima usage:
        --summary - prints summary
         --commit - interactively make a commit
                a pattern - add file(s) by id, idFrom-idTo or using wildcard pattern
                i pattern - ignore file(s) by id, idFrom-idTo or using wildcard pattern
                c         - commit
                cp        - commit and then push
                push      - push only
                pull      - pull only
                n         - go to the next repository
                q         - quit
        --scan [--path ...] - scans for git repos in the current folder or in the folder specified with --param
```


## Roadmap
There is no specific roadmap for `gima`. New features are added if they are needed.

## Contributing
Feel free to contribute to this project by sending me your opinion, patches, or requesting some features through gitlab issue system.

## License
`gima` is released under the MIT license.
