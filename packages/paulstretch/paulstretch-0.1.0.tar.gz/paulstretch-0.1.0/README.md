# Paulstretch

A modern Python implementation of [Paul Nasca](https://github.com/paulnasca)'s [extreme sound stretch algorithm](https://www.paulnasca.com/algorithms-created-by-me#h.4c6i2abbt3xk). It allows for extremely high stretch factors like 10 or 1000 without introducing the unpleasant grainy artifacts of other time stretch algorithms. It does smear all the transients though.

There is no modern and well maintained python package for this algorithm available on the package index. This is a fun DSP algorithm with a permissive license, so everyone should enjoy it!

### Installation

Install the latest version of the [uv package manager](https://docs.astral.sh/uv/). A virtual environment will automatically be installed when you run or build the project with uv.

### Run Tests

The project uses pytest as its testing framework. 

`uv run pytest`

### Build & Publish Package

1. Increment Version if appropriate

    The package uses semantic versioning, so bump the version depending on the extent of changes.

    `uv version --bump patch` or 

    `uv version --bump minor` or 

    `uv version --bump major`

2. Build both the source distribution and the wheels:

    `uv build`

3. Publish to the test pypi repository:

    `uv run twine upload --repository testpypi dist/*`

    Enter your pypi API token when prompted for username.

4. Test install from test pypi repository:

    `pip install --index-url https://test.pypi.org/simple/ paulstretch`

5. Publish to pypi prepository:

    `uv run twine upload dist/*`

    Enter your pypi API token when prompted for username.