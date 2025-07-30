# cbler

> Concatenate code into your clipboard with filters.

**cbler** is a CLI tool for extracting source files, filtering them, and copying the result to your clipboard.

- Built with [Typer](https://typer.tiangolo.com/)
- Rich output
- Multi-flag filtering
- Regex support
- Designed for piping code into ChatGPT or similar

---

## Install

```bash
pip install cbler
```

---

## Usage

```bash
cbler code gml . --contains Step
cbler code py . --not-suffix .test.py .old.py --prefix util_
```

Filters the files, copies them to your clipboard, prints a tree of what got included, and shows a summary panel.

---

## Filters (all optional)

Each of these accepts multiple values and regex patterns:

- `--prefix`, `--not-prefix`
- `--suffix`, `--not-suffix`
- `--contains`, `--not-contains`
- `--path-contains`, `--not-path-contains`
- `--parent-contains`, `--not-parent-contains` (matches immediate folder only)
- `--changed` (only get's changed files from git diff)

---

## Examples

All .gml and .yy scripts under weather-related GameMaker objects:

```bash
cbler code gml . --path-contains Weather
```

All Python files that aren't test files:

```bash
cbler code py . --not-parent-contains test --not-suffix _test.py
```

Python utility scripts:

```bash
cbler code py . --parent-contains utils helpers
```

---

## Output

- Copies code to your clipboard using `pyperclip`
- Shows a Rich tree of included files
- Summary panel shows copied and skipped counts

---

## CLI Layout

```bash
cbler code gml [path] [filters]
cbler code py  [path] [filters]
cbler git log  [repo] [count]
```

---

## Roadmap

- [ ] `--max-files` limit with confirmation
- [ ] Progress bar
- [ ] `--output` for saving to file
- [ ] Show skipped files with reasons

---

## Dev install

```bash
uv pip install -e .
cbler code py . --suffix .py
```

---

## License

MIT

---

## Name

"cbler" = clipboard + -ler
