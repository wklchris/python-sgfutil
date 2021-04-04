# sgfutil

sgfutil 是一个处理 SGF (Smart Go Format) 围棋棋谱文件的 Python 工具。

1. [sgfutil](#sgfutil)
   1. [安装与依赖](#安装与依赖)
   2. [用法](#用法)
   3. [许可证](#许可证)

## 安装与依赖

依赖项：

- Python >= 3.6
- ply 库： `python -m pip install ply`


## 用法

一个示例：

```python
>>> from Parser import parse_sgf
>>> parse_sgf('demo/Eg-single-branch.sgf')
[['CA', 'utf-8'], ['AB', 'rd', 'sd', 'oa', 'ob', 'oc', 'od', 'pd'], ['AW', 'pa', 'pb', 'pc', 'qc', 'rc', 'sc']]
```

## 许可证

[MIT](LICENSE)
