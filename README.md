# pixelarity-download
[![Build Status](https://travis-ci.org/briancurt/pixelarity-download.svg?branch=master)](https://travis-ci.org/briancurt/pixelarity-download)

[Pixelarity](https://pixelarity.com/) is awesome :heart:

This little utility will recursively download all the templates at once, so you don't have to click one by one every time.

### Usage

With Docker:

`docker run --rm -it -v /your/templates/directory:/tmp/downloads briancurt/pixelarity-download <EMAIL> <PASSWORD>`

Or run the script directly:

```bash
git clone git@github.com:briancurt/pixelarity-download.git
cd pixelarity-download/
pip3 install -r requirements.txt
src/pixelarity-download.py <EMAIL> <PASSWORD>
```

To re-download existing themes, use the `-f` flag.

### Note

SSL verification has been explicitly disabled because at the time of this writing the website does not return all the intermediate certificates from the chain correctly. It's okay-ish in this use case, but never disable SSL verification otherwise.