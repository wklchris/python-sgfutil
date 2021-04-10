# sgfutil <!-- omit in TOC -->

\>\> Languages: [中文](./docs/Readme-cn.md)

sgfutil is a Python library (see [Github repo](https://github.com/wklchris/python-sgfutil)) for utilizing SGF (Smart Game Format) files. It supports SGF FF4.0 syntax.

<img src="./docs/img/logo.svg" alt="sgfutil logo" width="70%" style="display: block; margin-left: auto; mergin-right: auto">

*Logo drawn by myself using TikZ*

If you are willing to know more about the SGF format, please visit the [SGF official site](https://www.red-bean.com/sgf/sgf4.html).

Table of Contents：
1. [Installation & Dependency](#installation--dependency)
2. [Usage](#usage)
3. [Future Plan](#future-plan)
4. [License](#license)

## Installation & Dependency

Installation:

```python
python -m pip install sgfutil 
```

Dependency：

- Python >= 3.6
- `ply` library：This library is no longer maintained on pip. Users can visit its official Github repo [dabeza/ply](https://github.com/dabeaz/ply) for the latest version.
  
  However, a stable yet a little older version (3.11) of ply is still accessible through pip installation:
  
  `python -m pip install ply`


## Usage

Here is an example.

You can pass an SGF filepath to the `sgf_parse()` function：
```python
>>> from sgfutil import SgfParser
>>> parser = SgfParser()
>>> parser.sgf_parse('demo/Eg-single-branch.sgf')
>>> print(parser)

--- Tree #0 ---
(('CA', 'utf-8'), ('AB', ['rd', 'sd', 'oa', 'ob', 'oc', 'od', 'pd']), ('AW', ['pa', 'pb', 'pc', 'qc', 'rc', 'sc']))
```

Or you can simply input an SGF string：
```python
>>> parser.sgf_parse('(;CA[utf-8]SZ[19];B[ab](;W[cd]C[Good move])(;W[ef];B[gh]))')
>>> print(parser)

--- Tree #0 ---
(('CA', 'utf-8'), ('SZ', 19))
(('B', 'ab'),)

--- Tree #1 ---
(('W', 'cd'), ('C', 'Good move'))

--- Tree #2 ---
(('W', 'ef'),)
(('B', 'gh'),)
```

## Future Plan

- [ ] Rewrite parsed data as Tree & Node class.
- [ ] Syntax check for the input SGF string.
- [ ] SGF nodes editing.
- [ ] Visualization.


## License

[MIT](LICENSE)
