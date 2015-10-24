# pandoc-server

A WSGI service that allow you to create pdf from markdown

# Installation

You must install "pandoc", "texlive" and additionnal dependencies if needed to build specific PDF.

Get the repository:

```
git clone git@github.com:metal3d/pandoc-server.git
cd pandoc-server
```

# Usage

Launch:

```
python main.py

# or

gunincorn -w 4 -b 0.0.0.0:8000 main:app
```

The service listens now the `:8000` port where you can POST data.

# POST Data

Eache value are sent as POST forma data:

- "m": markdown content
- "t": title that will be used to name the returned pdf file
- "hl": default is None, give the hightlight theme for syntax hightlight blocks

