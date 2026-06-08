# BingOS

BingOS is a lightweight Bingo and word-matrix editor built with a single HTML frontend and a Python `pywebview` wrapper.

## Features

- Edit a square Bingo grid and manually draw answer lines.
- Generate a word-cloud matrix from custom words.
- Configure matrix size, fill characters, overlap, and allowed word directions.
- Save generated boards as importable JSON in the native `{"N","data","boxes"}` format.
- Switch the interface language between Chinese, English, Japanese, and Korean.

## Run From Source

```powershell
pip install -r requirements.txt
python main.py
```

## Build

```powershell
pyinstaller main.spec --noconfirm
```

The generated executable is written to `dist/main.exe`.

## Save Format

Saved boards use UTF-8 JSON without a BOM:

```json
{
  "N": 15,
  "data": ["A", "B"],
  "boxes": [
    { "r1": 0, "c1": 0, "r2": 0, "c2": 4, "color": "#ff3b30" }
  ]
}
```

`data` must contain exactly `N * N` cells, and all `boxes` coordinates are zero-based and in bounds.
