#!/bin/bash
set -e
rm -rf build dist
uv build
echo "Uploading the package to PyPI via Twine…"
uv add twine
twine upload dist/* --verbose
# echo Pushing git tags…