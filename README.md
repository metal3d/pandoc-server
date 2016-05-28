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

- "m": markdown content or file
- "t": title that will be used to name the returned pdf file
- "hl": default is None, give the hightlight theme for syntax hightlight blocks
- "tpl": give the template file to use (latex only for now), this file should be contained at root at the tarball
- "tar": tarball file containing template, images, sty file and so on. 

Note that the server will untar the template archive and change working dir to the root of the tarball content, so you may tar you template folder at root.

For exemple, your tempalte is contained in "your-folder":

```
your-folder/
    mytemplate.tex
    images/
      img1.png
      img2.png
    my.sty
```
You should do:

```bash
$ cd ..
$ tar cfz your-template.tgz -C your-folder .
```

That way, the tarball contains files at root:

```bash
$ tar tf your-template.tgz
mytemplate.tex
images/
  img1.png
  img2.png
my.sty
```

And you can now try:

```bash
curl -X POST \
    -F "tar=@your-template.tgz" \
    -F "tpl=mytemplate.tex" \
    -F "m=@my-markdown-content.md" > out.pdf
```


