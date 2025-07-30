# application bundle creator

`abcreate` is a CLI tool to create a macOS application bundle from executables, libraries and resource files in a given installation prefix directory. It takes its instructions from an XML based configuration file (see the [examples](examples)).

This tool was built to replace [GTK Mac Bundler](https://gitlab.gnome.org/GNOME/gtk-mac-bundler) in my projects. That means it is specifically targeted towards GTK based applications and makes certain assumptions like "I always expect you to specify a GTK version". It is _not_ a general-purpose packaging tool at this point. Features and fixes will be developed as I go and to the extent as required for my projects.

💁 _For the time being, this is to be considered "alpha" software. It works for the cases I need it to work._

## Features

- Require as little configuration as possible in a simple XML file that's easy to understand.
- Automatically pull in linked libraries.
- Automatically adjust library link paths in executables and libraries with relocatability in mind.
- Targeted towards GTK based apps (GTK versions 3 and 4), e.g. take care of pixbuf loaders, compile typelib files etc.  

## Installation

`abcreate` is on [PyPi](https://pypi.org/project/abcreate/), simply run:

```bash
pip install abcreate
```

## Usage

Let's look at an example:

```bash
abcreate create bundle.xml -i $HOME/install_prefix -o $HOME/output_dir
```

- The first argument is a command. At the moment, there is only one command available, which is `create`.
- The `create` command expects
  - the name of a XML configuration file, e.g. `bundle.xml`
  - the install prefix directory (`-i`) containing `bin`, `lib`, `share` etc. directories of the applicatin you want to package
  - the output directory (`-o`) where the application bundle will be created in

## License

[GPL-2.0-or-later](LICENSE)
