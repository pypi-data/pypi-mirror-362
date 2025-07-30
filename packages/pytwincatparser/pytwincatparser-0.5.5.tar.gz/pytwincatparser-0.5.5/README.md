# pytwincatparser
A Python package for parsing TwinCAT PLC files (TcPOU, TcDUT, TcIO, TcPlcProj, TcGvl, TcIO).

## Description

This package provides tools to parse and work with TwinCAT PLC files. It uses xsdata to handle XML parsing. Be aware, that this is a python lib written by a beginner with help of AI assisted programming. My main work task is to design and program industrial machines, not develop python programms!

## Features

- Parse TwinCAT PLC files (.TcPOU, .TcDUT, .TcIO, .TcGvl, .TcPlcProj)
- Load the twincatfile in python dataclasses
- parse variable blocks
- parse documentation
- parse dependencies

## Installation


```
pip install pytwincatparser

```


## Usage

```python

_strategy: BaseStrategy = None
_collected: dict[str, Objects] = {}

# for now only "twincat4024" strategy is allowed
if config.default_strategy is not None:
    strategy = get_strategy(config.default_strategy)
else:
    strategy = get_default_strategy()

# set the loader with the right strategy
_strategy = strategy()
_loader: Loader = Loader(loader_strategy=_strategy)

# load every file
for path in paths:
    tcobjects = _loader.load_objects(path=path)
    # for every found object
    for tcobject in tcobjects:
        # get identifier (fb_main.Do_This) and check if such a object is not loaded already
        if not tcobject.get_identifier() in _collected:
            _collected[tcobject.get_identifier()] = tcobject
```

## Requirements

- Python 3.11
- lxml >= 5.3.0
- xsdata[lxml] >= 24.12

## License

MIT


## Todo

- [ ] Add support for return values of methods and functions
- [ ] Add support for specifier like CONSTANT and PERSISTEN in Variable blocks