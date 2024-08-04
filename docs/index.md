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

## Example

Consider the notebook shown below, when converted to slides using the `default` theme, it will look like the first image in the table below. When converted using the `fruity` theme, it will look like the second image.

<table>
	<tbody>
        <tr>
			<th colspan="2">Original notebook</th>
        </tr>
        <tr>
			<td colspan="2">
                <img src="images/demo-notebook.png" />
            </td>
        </tr>
		<tr>
			<th>Default theme</th>
			<th>Fruity theme</th>
		</tr>
		<tr>
            <td>
                <img src="images/demo-default/Slide1.jpeg" />
            </td>
			<td>
                <img src="images/demo-fruity/Slide1.jpeg" />
            </td>
		</tr>
		<tr>
            <td>
                <img src="images/demo-default/Slide2.jpeg" />
            </td>
			<td>
                <img src="images/demo-fruity/Slide2.jpeg" />
            </td>
		</tr>
	</tbody>
</table>

You can then use these slides in your presentation deck.
