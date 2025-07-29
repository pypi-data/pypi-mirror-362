name: publish
on:
  workflow_dispatch:
    inputs:
      tag_name:
        description: 'Tag name'
        required: true
        type: string
permissions:
  id-token: write
  contents: write
  pull-requests: write
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: release
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
      - name: Twine check
        run: twine check --strict dist/*
      - name: Publish to GitHub Releases
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TAG_NAME: ${{ inputs.tag_name }}
        run: gh release upload ${{ inputs.tag_name }} dist/*
      - name: Publish to PyPI
        run: twine upload dist/*
