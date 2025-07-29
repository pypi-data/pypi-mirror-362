# Tablegen

LAMMPS potential table generator for [LAMMPS](https://lammps.sandia.gov), developed by Vasilii Maksimov at the Functional Glasses and Materials Modeling Laboratory (FGM²L) at the University of North Texas, under the supervision of Dr. Jincheng Du.

**Tablegen** is a command-line utility for generating two-body and three-body potential tables for use with LAMMPS simulations. It supports several interaction models commonly used in materials science and glass chemistry, including:

- SHIK potential (Buckingham + Wolf summation)
- Classical Buckingham potential
- Extended Buckingham potential with softening
- Truncated harmonic three-body interactions

## 🔧 Features

- Command-line interface with `argparse`-based subcommands
- Supports plotting potential curves with `matplotlib`
- Generates `.table` and `.3b` files directly usable in LAMMPS
- Fully modular: new potentials can be added as new handler classes
- Handles numeric precision using `mpmath`
- Actively developed for materials modeling workflows

## 📦 Installation

### Install from PyPI (preferred)

The package is now published on PyPI you can install the latest stable release with:

```bash
pip install lammps-tablegen
```

### Install directly from GitHub (bleeding‑edge)

If you need the most recent commit:

```bash
pip install git+https://github.com/superde1fin/tablegen.git
```

### Clone & install locally

For local experimentation or contributing:

```bash
git clone https://github.com/superde1fin/tablegen.git
cd tablegen

# Standard install (no dev extras)
pip install .

# OR editable install (auto‑reload while editing)
pip install -e .
```

> **Tip :** add the `[dev]` extra to pull in testing, type‑checking, and release tools:
>
> ```bash
> pip install .[dev]
> ```
>
> This installs `pytest`, `ruff`, `mypy`, `twine`, and other developer utilities declared in **pyproject.toml**.

*Requires Python ≥ 3.9 and a working C/Fortran toolchain if installing `numpy` from source.*

## 🥪 Usage

After installation, invoke the CLI with:

```bash
tablegen [style] [options]
```

### Available styles:

- `shik`: Generate two-body tables using the SHIK potential

$$
\begin{gather*}
V^{SHIK} = V^{Buck} \left( r_{\alpha\beta} \right) + V^{Wolf}\left( r_{\alpha\beta} \right)\\
V^{Buck} \left( r_{\alpha\beta} \right) = A_{\alpha\beta} \exp\left( -B_{\alpha\beta} r_{\alpha\beta} \right) - \frac{C_{\alpha\beta}}{r_{\alpha\beta}^6} + \frac{D_{\alpha\beta}}{r_{\alpha\beta}^{24}}\\
V^W \left( r_{\alpha\beta} \right) = q_{\alpha} q_{\beta} \left( \frac{1}{r_{\alpha\beta}} - \frac{1}{r_{cut}^W} + \frac{r_{\alpha\beta} - r_{cut}^W}{\left( r_{cut}^W \right)^2} \right)
\end{gather*}
$$

*Note: Currently the pairs with published coefficients will have the wolf part added while no potential entry will be generated for a pair without coefficients (i.e. Na-Al)*

- `buck`: Generate tables using the standard Buckingham potential

$$
\begin{gather*}
V\left( r_{ij} \right) = A_{ij} \exp\left( -\frac{r}{\rho_{ij}} \right)  - \frac{C_{ij}}{r^6}
\end{gather*}
$$

- `buck_ext`: Use the extended Buckingham potential with softened short-range repulsion

$$
\begin{gather*}
V\left( r_{ij} \right) = A_{ij} \exp\left( -\frac{r}{\rho_{ij}} \right)  - \frac{C_{ij}}{r^6} \left( 1 - \exp\left( - \left( \frac{r_{ij}}{43\rho_{ij}} \right)^6 \right) \right) + \frac{D_{ij}}{r_{ij}^{12}}
\end{gather*}
$$

- `3b_trunc`: Generate three-body truncated harmonic tables

$$
\begin{gather*}
V\left(r_{ij}, r_{ik}, \theta_{jik}\right) = \frac{k}{2} (\theta_{jik} - \theta_0)^2 \exp\left(-\frac{r_{ij}^8 + r_{ik}^8}{\rho^8}\right)
\end{gather*}
$$

- `sw`: Generate three-body Stillinger-Weber potential energy tables

$$
\begin{gather*}
V\left(r_{ij}, r_{ik}, \theta_{jik}\right) = \lambda_{ijk}\epsilon_{ijk}\left( \cos\theta_{ijk} - \cos\theta_{0ijk} \right)^2 \exp\left( \frac{\gamma_{ij}\sigma_{ij}}{r_{ij} - a_{ij}\sigma_{ij}} \right)\exp\left( \frac{\gamma_{ik}\sigma_{ik}}{r_{ik} - a_{ik}\sigma_{ik}} \right)
\end{gather*}
$$

### Example usage:

*PLEASE MAKE SURE TO READ THE HELP INFORMATION THOROUGHLY BEFORE USING EACH STYLE* 

Minimal SHIK potential generation for SiO2:

```bash
tablegen shik initial.structure Si O
```

Standard options invoked:

```bash
tablegen shik initial.structure Si O --cutoff 8 --data_points 10000 --table_name SHIK.table --plot -10 10
```

or equivalently

```bash
tablegen shik initial.structure Si O -c 8 -d 10000 -t SHIK.table -p -10 10
```

Minimal Buckingham potential table generation (user will be prompted for coefficients):

```bash
tablegen buck Na-O Si-O
```

Standard options invoked

```bash
tablegen buck Na-O Si-O -c 10 -d 5000 -t buck.table -p -20 10
```

Minimal truncated three-body potential table generation (user will be prompted for coefficients):

```bash
tablegen 3b_trunc Si-O-Si
```

Standard options invoked:

```bash
tablegen 3b_trunc Si-O-Si -t silica -d 30 -c 5
```

Minimal Stillinger-Weber potential table generation (user will be prompted for coefficients):

```bash
tablegen sw Si-O-Si
```

Standard options invoked:
```bash
tablegen sw Si-O-Si -t silica -d 30 -c 5
```




## 📚 Documentation

All styles support `-h` or `--help` flags for detailed usage:

```bash
tablegen shik --help
```

## 🧠 Design Overview

The project is modular:

- `cli.py`: Main entry point, defines CLI and parses arguments
- `handlers/`: Contains one handler class per potential type (`SHIK`, `BUCK`, etc.)
- `constants.py`: Shared constants (e.g., cutoffs, physical constants, default coefficients)
- `__init__.py`: Exposes handler classes and version metadata
- `pyproject.toml`: Build and dependency metadata

Each handler:
- Parses user-provided arguments
- Validates species/pair/triplet input
- Prompts for coefficients
- Provides `eval_force` and `eval_pot` methods used by `two_body()` or `three_body()`

## 📈 Plotting

If the `--plot` option is passed, `matplotlib` will be used to visualize the potential curves for the specified pairs or triplets.

## 🥪 Development

Install dev dependencies:

```bash
pip install .[dev]
```

Run tests:

```bash
pytest
```

## 🔖 License

GNU General Public License v3.0 (GPLv3). See [`LICENSE`](LICENSE) for details.

## 👤 Author

Vasilii Maksimov  
University of North Texas  
✉️ VasiliiMaksimov@my.unt.edu

## 🌐 Links

- 🔬 [LAMMPS Official Site](https://lammps.sandia.gov)
- 📆 [PyPI Page](https://pypi.org/project/lammps-tablegen)
- 🐙 [GitHub Repository](https://github.com/superde1fin/tablegen)

