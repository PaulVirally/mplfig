mplfig
======

Matplotlib by default only allows you to export your figures in formats that are used for publishing (e.g., a `.pgf` file, a resterized `.png` file, etc.). MATLAB allows you to save files in a `.fig` format which allows you to change the plot very easily (say, to fix a typo on an axis label, or to change the colorscheme). mplfig strives to bring this functioinality to matplotlib. With mplfig, you can save your matplotlib files and load them right back up in another python script.

Example
=======

First, create a figure and save with it mplfig.
```python
import mplfig
import matplotlib.pyplot as plt

xs = list(range(10))
ys = list(map(lambda x: x**2, xs))

plt.plot(xs, ys)
mplfig.save_figure(plt.gcf(), 'myfig.mplpkl')

plt.show()
```

Next, load it back up and change the figure!
```python
import mplfig
import matplotlib.pyplot as plt

fig = mplfig.load_figure('myfig.mplpkl') # Load the saved figure

axes = fig.get_axes()
axes[0].set_xlabel('$x$') # Add an x label
axes[0].set_ylabel('$y = x^2$') # Add a y label
axes[0].lines[0].set_marker('o') # Add a circle marker

plt.show()
```
