# sgfutil <!-- omit in TOC -->

sgfutil 是一个处理 SGF (Smart Game Format) 棋谱文件的 Python 工具。支持 SGF FF4.0 语法。

<div align="center">
    <img src="docs/img/logo.svg" width=70%>
</div>

*该 Logo 由本人使用 TikZ 绘制。*

如果您希望了解关于 SGF 格式的更多信息（比如其文法），可以前往 [SGF 官方页面](https://www.red-bean.com/sgf/sgf4.html#ebnf-def)。

目录：
1. [安装与依赖](#安装与依赖)
2. [用法](#用法)
3. [开发计划](#开发计划)
4. [许可证](#许可证)

## 安装与依赖

依赖项：

- Python >= 3.6
- ply 库：已不在 pip 更新，如需最新的版本可前往其官方 Github 仓库 [dabeza/ply](https://github.com/dabeaz/ply)。不过一个稳定的、但稍旧的 ply 版本仍然可以从 pip 直接安装：
  
  `python -m pip install ply`


## 用法

下面是一个示例。

可以向 `sgf_parse()` 函数传入 sgf 文件路径：
```python
>>> from sgfutil import SgfParser
>>> parser = SgfParser()
>>> parser.sgf_parse('demo/Eg-single-branch.sgf')
>>> print(parser)

--- Tree #0 ---
(('CA', 'utf-8'), ('AB', ['rd', 'sd', 'oa', 'ob', 'oc', 'od', 'pd']), ('AW', ['pa', 'pb', 'pc', 'qc', 'rc', 'sc']))
```

也可以直接传入 sgf 字符串：
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

## 开发计划

- [ ] 将 Parser 过程改写为 Tree 与 Node 类。
- [ ] 对输入的 SGF 进行语法检查。
- [ ] 编辑 SGF 节点。
- [ ] 可视化。


## 许可证

[MIT](LICENSE)
