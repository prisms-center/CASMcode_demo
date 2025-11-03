# CASM Tutorial Docker Image

This Docker image provides a complete environment for running CASM tutorials in Jupyter Lab.

## Specifications

- **Base OS**: Ubuntu 24.04 LTS
- **Python**: 3.13 (in conda environment)
- **Package Manager**: Miniforge (mamba/conda)
- **GCC**: 13 (latest available in Ubuntu 24.04)
- **CASM Version**: 2.0a1 (installed from PyPI)
- **Architecture**: Multi-arch support (x86_64 and ARM64/aarch64)
- **Includes**: CASMcode_project notebooks, Jupyter Lab, and all required dependencies

## Building the Image

### Single Platform Build

To build for your current platform:

```bash
docker build -t casm .
```

## Running the Container

### Setup

First, clone the CASMcode_project repository to get the tutorial notebooks:

```bash
git clone https://github.com/prisms-center/CASMcode_project.git
cd CASMcode_project
```

### Basic Usage

Run the container with the notebooks directory mounted:

```bash
docker run -p 8888:8888 -v $(pwd)/notebooks:/workspace/notebooks casm
```

Then open your browser to `http://localhost:8888`

Your work in the notebooks will be saved to the local `CASMcode_project/notebooks` directory.

### Interactive Shell

To start an interactive shell instead of Jupyter Lab:

```bash
docker run -it casm /bin/bash
```

The conda environment is automatically activated. You can manually start Jupyter Lab with:

```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

Or run CASM commands directly:

```bash
casm-calc -h
```

## Environment Variables

The following environment variables are set automatically:

- `CASM_PREFIX`: Set to the CASM installation prefix
- `CASM_SOFLAGS`: Set to `"-shared -Wl,--no-as-needed"` for shared library compilation
- `PATH`: Includes the conda environment bin directory for CASM executables
- `CONDA_DEFAULT_ENV`: Set to `casm`

## Notes

- CASM is installed in an isolated conda environment named `casm`, avoiding system package conflicts
- CASM is installed from PyPI (`casm-project==2.0a1`) rather than built from source
- The image does NOT include the CASMcode_project repository - you must clone it separately and mount the notebooks directory
- Jupyter Lab runs without authentication by default (suitable for local use only)
- The container runs as root (use `--user` flag if you need a different user)
- The image automatically detects and supports both x86_64 and ARM64 architectures

## Troubleshooting

If you encounter issues:

1. **Port already in use**: Change the port mapping `-p 9999:8888`
2. **Permission issues**: Ensure Docker has necessary permissions
3. **Build failures**: Check your internet connection and Docker disk space

