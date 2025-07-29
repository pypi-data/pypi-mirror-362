# Agilix API
### By fr8train-sv

A Python SDK for integrating with Agilix Buzz API. Install with:

```bash
  pip install agilix_api_fr8train
```

Upgrade this specific library by running:

```bash
  pip install --upgrade agilix_api_fr8train
```

## Important Commands

The following list of commands are important for project maintenance.

## Building the Library

To build the library, ensure that the necessary build tools are installed in your environment. This can be done by installing `setuptools`, `build`, and `wheel`:

```bash
  pip install build twine setuptools wheel
```

`twine` can also be installed here while we're installing shit since we'll need it later. 

**REMEMBER**: INCREMENT YOUR VERSION NUMBER IN THE TOML BEFORE BUILDING.  

**REMEMBER**: REMOVE THE /DIST DIRECTORY BEFORE BUILDING FOR A CLEAN BUILD

Now, you can create the distribution files (source distribution and wheel) using the following command:

```bash
  python3 -m build
```

This will generate builds in the `dist/` directory.

## Deploying to PyPI

Ensure you have a valid PyPI account and credentials added to your `.pypirc` file or provide them during the publish process. Then, upload your package to PyPI with:

```bash
  python3 -m twine upload dist/*
```

Follow any prompts from `twine` to successfully upload your package. Once deployed, your package will be available on PyPI. 
