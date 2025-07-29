name: release-please
on:
  push:
permissions:
  contents: write
  pull-requests: write
  issues: write
  actions: write
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install lint tools
        run: pip install black mypy
      - name: Run black --check
        run: black --check .
      - name: Run mypy
        run: mypy src/
  build-check:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install build tools
        run: pip install build twine
      - name: Build package
        run: python -m build
      - name: Check package with twine
        run: twine check dist/*
  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: pip install .
        run: pip install .
      - name: python -m unittest
        run: python -m unittest
  coverage:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: pip install coverage
        run: pip install coverage
      - name: pip install .
        run: pip install .
      - name: coverage run
        run: coverage run --source %%PROJECT_NAME%% -m unittest
      - name: coverage report
        run: coverage report -m --fail-under 100
  release-please:
    runs-on: ubuntu-latest
    needs: [lint, test, coverage, build-check]
    steps:
      - name: release-please
        if: github.ref == 'refs/heads/%%DEFAULT_BRANCH%%'
        id: release-please
        uses: googleapis/release-please-action@v4
        with:
          release-type: python
      - name: checkout
        if: steps.release-please.outputs.release_created
        uses: actions/checkout@v4
      - name: trigger-publish
        if: steps.release-please.outputs.release_created
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TAG_NAME: ${{ steps.release-please.outputs.tag_name }}
        run: gh workflow run publish.yml -f tag_name=${TAG_NAME}
