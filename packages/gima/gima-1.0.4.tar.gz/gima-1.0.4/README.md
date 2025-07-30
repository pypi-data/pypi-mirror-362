# gim

`gim` is a `Python` software which simplifies managing many git repositories through the console. `gim` is intended to make it easy to `commit`, `pull` and `push` changes for many repositories with easy console interface. The goal of `gim` is not to replace any git client.


## Installation

`TODO` pip

## Usage

Type in the console:

```
gim
```

and you should see:

```
gim usage:
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

## Support


## Roadmap
There is no specific roadmap for `gim` project. New features are added if they are needed.

## Contributing
Feel free to contribute to this project by sending me your opinion, requesting some features through gitlab issue system.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
`gim` is released under the MIT license.
