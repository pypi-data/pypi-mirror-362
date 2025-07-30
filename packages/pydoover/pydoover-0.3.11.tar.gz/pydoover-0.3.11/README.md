# PyDoover: The Python Package for Doover

PyDoover is a Python package that provides a simple and easy-to-use interface for using the Doover platform on devices, in tasks and CLIs.

# Getting Started

## Installing
**Python 3.11 or higher is required**

```shell
# Linux/macOS
python3 -m pip install -U pydoover

# Windows
py -3 -m pip install -U pydoover

# to install the development version:
python3 -m pip install -U git+https://github.com/spaneng/pydoover
```

There are some optional dependencies that can be installed in a few different use cases:

For using `pydoover` as a CLI tool, install the CLI optional dependencies:
```bash
python3 -m pip install -U pydoover[cli]
```

If you are using `pydoover` and need **grpc** support and **are not** using the `doover_device_base` docker image, install the grpc optional dependencies:

We currently use `grpcio==1.65.1` across all our services, so you need to install this version of `grpcio` to avoid issues.
```bash
python3 -m pip install -U pydoover[grpc]
```

## Quickstart

TODO

## Contributing

For more information, please reach out to the maintainers at hello@doover.com

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.