<!-- markdownlint-disable -->

# 🐍 pypi2aur

**pypi2aur** is a command-line tool that helps you convert Python packages from PyPI into Arch Linux AUR PKGBUILD templates. It streamlines the process of packaging Python projects for the Arch User Repository, automating metadata extraction and template generation.

<div align="center">
  <span>
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pypi2aur">
    <img alt="AUR Version" src="https://img.shields.io/aur/version/pypi2aur">
    <img alt="Python Version from PEP 621 TOML" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FAntraXClown%2Fpypi2aur%2Frefs%2Fheads%2Fmain%2Fpyproject.toml">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/AntraXClown/pypi2aur">
    <img alt="GitHub License" src="https://img.shields.io/github/license/AntraXClown/pypi2aur">
  </span>
</div>

## Demo

https://github.com/user-attachments/assets/441369e7-cf6e-42c6-b33c-17a035c6149e

## ⚙️ Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for project management
- [requests](https://pypi.org/project/requests/) for HTTP requests
- [click](https://pypi.org/project/click/) for CLI

## 📦 Installation

### with PIP

```bash
pip install pypi2aur
```

### with UV

```bash
uv pip install pypi2aur
```

### with AUR (Arch Linux repository)

```bash
yay -S pypi2aur
```

## 🚀 Usage

After installing the dependencies and activating your virtual environment, you can use the `pypi2aur` CLI to generate and manage PKGBUILD files for Python packages from PyPI.

### 🔨 Commands

- **create [PKG]**

  Generates a new PKGBUILD file for the specified PyPI package.

  **Usage:**

  ```bash
  pypi2aur create <package-name>
  ```

  - `<package-name>`: The name of the PyPI package to generate the PKGBUILD for.

- **update**

  Updates the existing PKGBUILD file in the current directory to match the latest version of the package on PyPI. The package name is read from the `pkgname` field in the PKGBUILD file.

  **Usage:**

  ```bash
  pypi2aur update
  ```

- **showdeps [PKG]**

  Displays the dependencies of the specified PyPI package as listed on PyPI.

  **Usage:**

  ```bash
  pypi2aur showdeps <package-name>
  ```

  - `<package-name>`: The name of the PyPI package to inspect.

### 📋 Example

- Create a PKGBUILD for the 'requests' package

```bash
pypi2aur create requests
```

- Update the PKGBUILD to the latest version

```bash
pypi2aur update
```

- Show dependencies for the 'requests' package

```bash
pypi2aur showdeps requests
```

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests. Follow the code style and naming conventions described above.

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.
