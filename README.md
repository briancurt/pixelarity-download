# pixelarity-download
[![Build Status](https://travis-ci.org/briancurt/pixelarity-download.svg?branch=master)](https://travis-ci.org/briancurt/pixelarity-download)

[Pixelarity](https://pixelarity.com/) is awesome :heart:

This little utility will download all the templates at once, so you don't have to click one by one every time.

### Usage

With Docker:

`docker run --rm -it -v /your/templates/directory:/tmp/downloads briancurt/pixelarity-download <EMAIL> <PASSWORD>`

Or clone the repo and run:

```bash
pip install -r requirements.txt
src/pixelarity-download.py <EMAIL> <PASSWORD>
```

To force the redownload of already downloaded themes, supply the `-f` parameter.

