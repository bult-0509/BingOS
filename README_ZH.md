# BingOS [![English](https://img.shields.io/badge/Docs-English-blue?style=flat-square)](README.md)  [![中文](https://img.shields.io/badge/文档-简体中文-red?style=flat-square)](README_ZH.md) 

BingOS 是一个轻量级的 Bingo 和词云矩阵编辑器，使用单一 HTML 前端和 Python `pywebview` 包装器构建。

## 功能特性

- 编辑方形 Bingo 网格并手动绘制答案线
- 从自定义词语生成词云矩阵
- 配置矩阵大小、填充字符、重叠选项和允许的词语方向
- 将生成的面板保存为可导入的 JSON 格式，使用原生 `{"N","data","boxes"}` 格式
- 在中文、英文、日文和韩文之间切换界面语言

## 从源码运行

```powershell
pip install -r requirements.txt
python main.py
```

## 保存格式

保存的面板使用无 BOM 的 UTF-8 JSON 格式：

```json
{
  "N": 15,
  "data": ["A", "B"],
  "boxes": [
    { "r1": 0, "c1": 0, "r2": 0, "c2": 4, "color": "#ff3b30" }
  ]
}
```

`data` 必须包含恰好 `N * N` 个单元格，所有 `boxes` 坐标都是从零开始的且在边界内。
