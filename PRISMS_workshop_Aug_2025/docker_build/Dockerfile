# CASM Tutorial Docker Image
# Based on Ubuntu 24.04 with Python 3.13 and GCC 13, using mamba for package management
FROM ubuntu:24.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set up timezone
ENV TZ=UTC

# Install system dependencies, GCC 13 (latest in Ubuntu 24.04), and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-13 \
    g++-13 \
    gfortran-13 \
    git \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set GCC 13 as default
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-13 100 \
    && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-13 100 \
    && update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-13 100

# Install Miniforge (includes mamba and conda) - auto-detect architecture
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        MINIFORGE_ARCH="x86_64"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        MINIFORGE_ARCH="aarch64"; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    wget -q "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-${MINIFORGE_ARCH}.sh" -O /tmp/miniforge.sh && \
    bash /tmp/miniforge.sh -b -p /opt/miniforge && \
    rm /tmp/miniforge.sh

# Add conda to PATH
ENV PATH="/opt/miniforge/bin:${PATH}"

# Initialize conda for bash
RUN conda init bash

# Create conda environment with Python 3.13
RUN mamba create -n casm python=3.13 -y

# Activate environment by default
ENV CONDA_DEFAULT_ENV=casm
ENV PATH="/opt/miniforge/envs/casm/bin:${PATH}"

# Set working directory
WORKDIR /workspace

# Install CASM from PyPI in the conda environment
RUN /opt/miniforge/envs/casm/bin/pip install casm-project==2.0a1

# Download and install notebook requirements from CASMcode_project
RUN wget -q https://raw.githubusercontent.com/prisms-center/CASMcode_project/main/notebooks_requirements.txt -O /tmp/notebooks_requirements.txt && \
    /opt/miniforge/envs/casm/bin/pip install -r /tmp/notebooks_requirements.txt && \
    rm /tmp/notebooks_requirements.txt

# Set environment variables for CASM
ENV CASM_SOFLAGS="-shared -Wl,--no-as-needed"
RUN export CASM_PREFIX=$(/opt/miniforge/envs/casm/bin/python -m libcasm.casmglobal --prefix) && \
    echo "export CASM_PREFIX=${CASM_PREFIX}" >> /root/.bashrc && \
    echo "export CASM_SOFLAGS=\"${CASM_SOFLAGS}\"" >> /root/.bashrc

# Expose Jupyter Lab port
EXPOSE 8888

# Set working directory
WORKDIR /workspace

# Create a startup script to activate environment and launch Jupyter
RUN echo '#!/bin/bash\n\
source /opt/miniforge/bin/activate casm\n\
export CASM_PREFIX=$(python -m libcasm.casmglobal --prefix)\n\
export CASM_SOFLAGS="-shared -Wl,--no-as-needed"\n\
echo "CASM_PREFIX: ${CASM_PREFIX}"\n\
echo "CASM_SOFLAGS: ${CASM_SOFLAGS}"\n\
echo "Python version: $(python --version)"\n\
echo "GCC version: $(gcc --version | head -n1)"\n\
echo "Starting Jupyter Lab..."\n\
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token="" --NotebookApp.password=""\n\
' > /workspace/start.sh && chmod +x /workspace/start.sh

# Ensure conda environment is activated for interactive shells
RUN echo "source /opt/miniforge/bin/activate casm" >> /root/.bashrc

# Default command
CMD ["/workspace/start.sh"]
