# pdf-tool

A lightweight CLI utility for manipulating PDFs.

## Features

- Merge two PDFs

- Rotate selected pages

- Reverse page order

- Delete pages

- Operate on specific pages or ranges

- In-place or save as new file

- Simple and intuitive CLI with helpful options

## Installation

### Option 1 — Install from PyPI (recommended)

```bash
pip install pdf-tool
```

### Option 2 — Install from source

```bash
git clone https://github.com/kavehfayyazi/pdf-tool.git
cd pdf-tool
pip install --user .
# or 
python3 -m pip install --user .
```

If `pdf-tool` is not found after install, make sure the appropriate scripts folder is in your `PATH`:

- macOS/Linux: `~/.local/bin`

- Windows: `%APPDATA%\Python\Scripts`

See [Troubleshooting](#troubleshooting) below for more details.

## Updating & Uninstalling

### Update to the latest version

If you installed from PyPI:

```bash
pip install --upgrade --user pdf-tool
# or
python3 -m pip install --upgrade --user pdf-tool
```

If you installed from source:

```bash
cd pdf-tool
git pull origin main
pip install --user .
# or
python3 -m pip install --user .
```

### Uninstall

```bash
pip uninstall pdf-tool
# or
python3 -m pip uninstall pdf-tool
```

## Usage

```bash 
pdf-tool <command> [options]
```

### Available commands:

| Command | Description |
| :--- | :---: |
| `merge` | Merge two PDFs |
| `rotate` | Rotate pages |
| `reverse` | Reverse page order |
| `delete` | Delete selected pages |

### Example:

```bash
pdf-tool merge file1.pdf file2.pdf -o merged.pdf
pdf-tool rotate file.pdf -p 1:3 -a 90 -o rotated.pdf
```

Run:

```bash
pdf-tool --help
pdf-tool <command> --help
```

for full options.

## Specifying Pages and Ranges

Many commands in `pdf-tool` allow you to operate on specific pages or ranges of pages in a PDF.

You can specify pages using:

- Individual page numbers (1-based, e.g. `1,3,5`)

- Ranges using a colon (e.g. `2:4` for pages 2, 3, and 4)

- Combinations of both

### Examples

| Input | Expanded Pages |
| :--- | :---: |
| `all` | All pages in the document (default) |
| `1,3,5` | Pages 1, 3, and 5 |
| `2:4` | Pages 2, 3, and 4 |
| `1,3:5,7` | Pages 1, 3, 4, 5, and 7 |

## Contributing

1. **Fork** this repository.

2. **Clone** your fork locally:

    ```bash
    git clone https://github.com/<your-username>/pdf-tool.git
    cd pdf-tool
    ```

3. **Create** a new branch:

    ```bash
    git checkout -b feature/your-feature
    ```

4. **Commit** your changes:

    ```bash
    git commit -m "Add feature-name."
    ```

5. **Push** to the branch

    ```bash
    git push origin feature/feature-name
    ```

6. **Open** a pull request.

## Troubleshooting

**Command not found?**

Your Python "scripts" folder may not be in your PATH.

- **macOS/Linux**:

    Add to your shell config (`~/.bashrc` or `~/.zshrc`):

    ```bash
    export PATH="$HOME/.local/bin:$PATH"
    ```
- **Windows**:

    Add `%APPDATA%\Python\Scripts` to your User PATH via System &rarr; Environment Variables.

Then restart your terminal and try `pdf-tool --help` again.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Creator: kavehfayyazi
- Email: [kfayyazi@andrew.cmu.edu](mailto:kfayyazi@andrew.cmu.edu)
- Github: [@kavehfayyazi](https://github.com/kavehfayyazi)