# Python bindings for the DiffSol library for PyBOP

## Development

### Getting started

You will need to have `maturin` installed to build the bindings. You can install it in a virtual environment like this:

```bash
python3 -m venv env
source env/bin/activate
pip install maturin
```

You will also need to have LLVM installed. On Ubuntu, you can install it with:

```bash
sudo apt install llvm-dev
```

Make a note of the directory where LLVM is installed as well as the version number, as you will need to pass it to `maturin` when building the bindings.

### Building the bindings

To build the bindings, run the following command in the root directory of the project, replacing the llvm directory and version number with the ones you noted earlier:

```bash
LLVM_DIR=/usr/lib/llvm-17  LLVM_SYS_170_PREFIX=/usr/lib/llvm-17 maturin develop --features diffsol-llvm17
```