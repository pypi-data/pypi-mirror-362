# SeaVoice SDK V2

### How to publish this package

#### Prerequisite
1. cd in to this folder `SeaVoice/backend/sdk/v2`
2. pip install build twine

#### publish a version
1. change version in `pyproject.toml`
2. cp .pypirc.example .pypirc
3. set up token in .pypirc `password`, e.g. `pypi-...`
4. source publish_package.sh
