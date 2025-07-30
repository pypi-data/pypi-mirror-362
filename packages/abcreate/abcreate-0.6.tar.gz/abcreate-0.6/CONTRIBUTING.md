# Development guidelines

At the moment, the scope of this project is very limited. As hinted at in the [README](README.md), it was created to solve a specific problem for a specific use case. I do not expect that this will ever pique sombody else's interest, but should you be reading this, it's probably best to create an [issue](https://github.com/dehesselle/abcreate/issues) and talk to me before you start developing something.

## Branching

While I'm doing this for myself, I'm too lazy to create short-lived feature branches, I use `develop` for this instead. Despite it being a public and permanent branch, I treat it like a feature branch, i.e. I rebase and mess with the history there all the time.

Only the `main` branch is to be considered "safe territory" where I don't mess around. PR's should always target the `main` branch.

## Versioning

This project uses [semantic versioning](https://semver.org) and will stay at a `0.x` version for a long time (or even forever).

## Releases

Proper releases are created by tagging a version (e.g. `v0.1`) on the `main` branch and published to [PyPi](https://pypi.org/project/abcreate/).

A rolling release is created/updated on GitHub from every push to the `develop` branch (tagged as [`latest`](https://github.com/dehesselle/abcreate/releases/tag/latest)). For testing purposes only!

## Python

- Targeting Python >= 3.10.  
  _This will change in the near future to >=3.12!_
- Using [uv](https://github.com/astral-sh/uv) for package management.
- [Black](https://black.readthedocs.io/en/stable/) all they way.
