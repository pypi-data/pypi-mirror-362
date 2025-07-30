![Logo](https://bitbucket.org/rfg_lab/climax/raw/0284bca63f357cddcf5c375eae0e2ad4863f9906/docs/climax_logo_full.jpg)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

# [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) (a Command Line IMAge eXplorer)

## Installing [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/)

We recommend that you install [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) as a tool using [uv](https://github.com/astral-sh/uv):

    $ uv tool install climax-rfglab

or

    $ uvx --from climax-rfglab climax

A [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) executable will be created in a bin directory in the PATH, which allows the tool to be run without uv. If the directory with the [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) executable is not in the PATH, a warning will be displayed and the following command can be issued to add it to the PATH:

    $ uv tool update-shell

[CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) can also be installed as a regular [Python](https://www.python.org/downloads/) package using [uv](https://github.com/astral-sh/uv):  

    $ uv pip install climax-rfglab

or [pip](https://pip.pypa.io/en):

    $ python3 -m pip install climax-rfglab

### A note on the Python interpreter

[CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) requires that you have [Python 3.10 or above](https://www.python.org/downloads/) installed.

## Using [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/)

After installing [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) with one of the methods above, You can invoke it with:

    $ climax <filename>

You can also run [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) without installing it, taking advantage of [uvx](https://github.com/astral-sh/uv):

    $ uvx --from climax-rfglab climax <filename>

There are a few ways to open an image with [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/):

- You can specifiy the path to the image that you want to open (e.g. *tests/cells_movie.tif*) :

        $ climax tests/cells_movie.tif

- Or you can indicate a folder (*slices* in this example) that contains an image sequence:

        $ climax ./slices

- If there are image channels split into different files, you can specify a group of substrings to distinguish which files in the folder belong to which channel. For example, to open the files in the *slices* folder containing the substrings '488' and '561' as two different channels:

        $ climax ./slices -s 488 561

- You can use a list of paths to concatenate sideways (i.e. display side-by-side, but all the images must have the same dimensions!!):

        $ climax cells_movie_1.tif cells_movie_2.tif

- You can specify the color map used to display the image. The color map defaults to *'gray'*. Check [here](https://matplotlib.org/stable/tutorials/colors/colormaps.html) for a list of color maps.

        $ climax cells_movie.tif -c viridis

- Notice that if you try to open a color image, the channels will be split and displayed side-by-side (red, green, blue). Thus, for instance, if you open the [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) logo:

![Color](https://bytebucket.org/rfg_lab/climax/raw/3142f0d665a03f763b7c2d71a7b2f5b43eed3c59/docs/color_image_display.png)

[CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) provides a dashboard with additional functionality:

|name|function|
|----------------------------------------|------------------------|
|rotate|rotate 90&deg; clockwise
|flip h.|flip horizontally|
|flip v.|flip vertically|
|invert|invert color map|
|update|continuous/discrete update|
|x-y, z-y, z-x|slicing plane through stack|
|auto|automated contrast adjustment (min-mode, max-99th percentile)|

# [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) today

As we develop and improve [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/), there may be small changes to the user interface. This is how [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/) looks as of today:

![CLIMAX today](./docs/climax_today.gif)

## Citing [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/)
If you use [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/), please cite this repository. We are working on the paper!

## Sponsors

We are grateful for the generous support from the following agencies and institutions, which contribute to the
development and maintenance of [CLImax](https://bitbucket.org/rfg_lab/climax/src/master/):

![Sponsors](https://bitbucket.org/rfg_lab/climax/raw/0367742a0a3f4670b0d8299d52e0d52b6c8c601f/docs/sponsors.png)