*PresentPy* allows you to add dataframes and plots to your slides.

## Images and plots

To add an image to your slide all you need to do is plot your image using matplotlib and have it as a result in your slide, for example:

### Configuration

You can configure the title of the slide by using the *PresentPy* cell "magic" comment at the end of your cell, for example:

```python
#% title="My nice plot" 
```

If you provide a title, it will be used as the title of the slide, otherwise the slide will not have a title and the image or plot will use all the available space.

## DataFrames

Adding a dataframe to your slide is as simple as creating a dataframe and having it as an output of a cell in your notebook.

### Configuration

You can configure the title of the slide by using the *PresentPy* cell "magic" comment at the end of your cell, for example:

```python
#% title="My amazing DataFrame" 
```