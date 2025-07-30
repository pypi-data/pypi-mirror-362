# sungazer

**Documentation**: https://sungazer.readthedocs.org

`sungazer` is a command line interface and client library for accessing the the
internal API of the SunPower PVS6 monitoring device installed with a SunPower
solar insallation.

## Installation

`sungazer` supports Python 3.10+.

To install from PyPI:

```shell
pip install sungazer
```

## Usage

Example usage of the command line interface:

```bash
# Get help
sungazer --help
sungazer device --help
sungazer network list --help

# Use JSON output (default)
sungazer session start

# Use table output
sungazer session start --output table
```

## Autocomplete

To enable autocomplete of the `sungazer` command line interface, do:

```bash
# For bash
echo 'eval "$(_SUNGAZER_COMPLETE=bash_source sungazer)"' >> ~/.bashrc

# For zsh
echo 'eval "$(_SUNGAZER_COMPLETE=zsh_source sungazer)"' >> ~/.zshrc

# For fish
echo 'eval (env _SUNGAZER_COMPLETE=fish_source sungazer)' >> ~/.config/fish/config.fish
```
