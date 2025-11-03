# PRISMS Workshop August 2025 - CASM Tutorial

This directory contains materials and installation instructions for the CASM tutorial presented at the PRISMS Workshop in August 2025.

## Installation Options

There are several ways to install and run CASM for this tutorial:

**Note**: CASM requires Python 3.9 or later and a C++17 compatible compiler. CASM requires a Linux-compatible environment; Windows users should use WSL2 or Docker.

### 1. Native Installation

For everyday use, CASM is typically installed natively on a user's system or HPC cluster. CASM can be installed using pip in a virtual environment or conda/mamba environment.

In some cases, environment variables need to be set to compile CASM clexulators. The following includes a configuration step to check common configurations and print the variables used in a successful configuration to the file `casmenv.sh`. This file can be sourced in future sessions before running JupyterLab or Python.

The following instructions outline the native installation process.

#### Using conda/mamba

```bash
# Create and activate a conda environment
conda create -n casm python=3.13
conda activate casm

# Install CASM
pip install casm-project==2.0a1

# Run CASM configuration tests
python -m casm.bset --autoconfigure --shfile casmenv.sh

# Set the environment variables
source casmenv.sh

# Clone the casm-project repository with tutorial notebooks and install requirements
git clone https://github.com/prisms-center/CASMcode_project.git
cd CASMcode_project
pip install -r notebooks_requirements.txt

# Launch Jupyter Lab
jupyter lab
```

#### Using pip (Virtual Environment)

```bash
# Create and activate a virtual environment
python -m venv casm_env
source casm_env/bin/activate  # On Windows: casm_env\Scripts\activate

# Install CASM
pip install casm-project==2.0a1

# Run CASM configuration tests
python -m casm.bset --autoconfigure --shfile casmenv.sh

# Set environment variables
source casmenv.sh

# Clone the casm-project repository with tutorial notebooks and install requirements
git clone https://github.com/prisms-center/CASMcode_project.git
cd CASMcode_project
pip install -r notebooks_requirements.txt

# Setup environment
export CASM_PREFIX=$(python -m libcasm.casmglobal --prefix)

# Launch Jupyter Lab
jupyter lab
```

### 2. Docker Installation

For participants who prefer a containerized environment or are working on systems where native installation is challenging, we provide a complete Docker build process.

**Location**: `docker_build/`

**Features**:
- Complete isolated environment with Ubuntu 24.04 LTS
- Python 3.13 in conda environment
- Pre-configured with all CASM dependencies
- Jupyter Lab ready to run
- Multi-architecture support (x86_64 and ARM64)

**Quick Start**:
```bash
cd docker_build/
docker build -t casm .
git clone https://github.com/prisms-center/CASMcode_project.git
cd CASMcode_project
docker run -p 8888:8888 -v $(pwd)/notebooks:/workspace/notebooks casm
```

Then open your browser to `http://localhost:8888`

See [docker_build/README.md](docker_build/README.md) for detailed Docker setup instructions.

### 3. CAEN Lab Installation (University of Michigan)

For participants using University of Michigan CAEN lab computers, we provide streamlined installation instructions using pre-installed modules and software.

**Location**: `caenlab_linux/`

**Features**:
- Uses CAEN lab's module system (Python 3.11, GCC 13.2.1)
- Installs CASM in user space (no admin privileges required)
- Includes Jupyter Lab setup for running tutorials
- Quick installation process optimized for CAEN environment

See [caenlab_linux/CAEN_lab_install.txt](caenlab_linux/CAEN_lab_install.txt) for detailed installation steps.


## Tutorial Materials

- **Slides**: `CASM_PRISMS_2025_wide.pdf` - Workshop presentation slides
- **Notebooks**: Available in the [CASMcode_project repository](https://github.com/prisms-center/CASMcode_project)

The slides provide a guide for the Si-Ge cluster expansion tutorial notebooks:

- `notebooks/SiGe_occ_part1.v2.ipynb`
  - CASM project initialization
  - Configuration enumeration
  - Calculation
  - Import and mapping
- `notebooks/SiGe_occ_part2.v2.ipynb`
  - Cluster expansion construction & fitting
  - Monte Carlo calculation


## Support

For issues or questions:
- CASM v2 package overview and documentation links: https://prisms-center.github.io/CASMcode_pydocs/overview/latest/
- GitHub repository: https://github.com/prisms-center/CASMcode_project
- Report issues: https://github.com/prisms-center/CASMcode_project/issues

## License

CASM is distributed under the LGPL license. See the [CASMcode_project repository](https://github.com/prisms-center/CASMcode_project) for details.
