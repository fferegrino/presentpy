PresentPy
=========

# PresentPy

 > Create slides from Jupyter Notebooks

_PresentPy_ allows you to take your Jupyter Notebooks and turn them into slides (compatible with PowerPoint, Keynote, LibreOffice...) that then can be integrated into your presentation decks.

## Installation

I strongly recommend using `pipx` to install _PresentPy_:

```bash
pipx install presentpy
```

Otherwise, you can install it using `pip` or your favorite package manager – the package is called `presentpy`.

## Usage

To turn a notebook into slides, simply run:

```bash
Usage: presentpy [OPTIONS] NOTEBOOK

  presentpy: A CLI tool to convert Jupyter Notebooks to ODP presentations.

Options:
  --output PATH  Directory or file path where the output ODP file will be
                 saved. Defaults to the current directory.
  --theme TEXT   Pygments style to be applied to the presentation. Defaults to
                 'default'. See https://pygments.org/docs/styles/ for
                 available styles.
```

<!-- 
It also works with Python scripts:

```bash
presentpy [OPTIONS] py SCRIPT_PATH
```
-->

## Code configuration

You can configure the code cells to be displayed in the slides by adding a comment on the last line of the cell. The comment should start with `#%` and then you can add the following options:

 - `title`: The title of the slide
 - `highlights`: A comma separated list of lines to highlight, each highlight could be a number or a range of lines separated by a dash, e.g. `1,3-6,6-7`

For example, take the following code:

```python
def compute_hcf(x, y):
    if x > y:
        smaller = y
    else:
        smaller = x
    for i in range(1, smaller+1):
        if((x % i == 0) and (y % i == 0)):
            hcf = i 
    return hcf
#% title="Find the H.C.F of two numbers" highlights=1,2-3,4-5,9
```

The code above will generate 5 slides showing the same code but highlighting different lines in each slide – see how it looks below:

<iframe src="https://www.slideshare.net/slideshow/embed_code/key/LmOcrrRuEaitnJ?hostedIn=slideshare&page=upload" width="476" height="400" frameborder="0" marginwidth="0" marginheight="0" scrolling="no"></iframe>

You can then use these slides in your presentation deck.
