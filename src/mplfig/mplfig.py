from matplotlib.figure import _AxesStack
import matplotlib.pyplot as plt
# import pickle
import dill as pickle

def save_figure(figure, fpath):
    # Get the properties of the figure that we need to save
    data = {
        'fig_props' : {
            'agg_filter' : figure.get_agg_filter(),
            'alpha' : figure.get_alpha(),
            'animated' : figure.get_animated(),
            'clip_box' : figure.get_clip_box(),
            'clip_on' : figure.get_clip_on(),
            'clip_path' : figure.get_clip_path(),
            'constrained_layout' : figure.get_constrained_layout(),
            'dpi' : figure.get_dpi(),
            'edgecolor' : figure.get_edgecolor(),
            'facecolor' : figure.get_facecolor(),
            'figheight' : figure.get_figheight(),
            'figwidth' : figure.get_figwidth(),
            'frameon' : figure.get_frameon(),
            'gid' : figure.get_gid(),
            'in_layout' : figure.get_in_layout(),
            'label' : figure.get_label(),
            'linewidth' : figure.get_linewidth(),
            'path_effects' : figure.get_path_effects(),
            'picker' : figure.get_picker(),
            'rasterized' : figure.get_rasterized(),
            'size_inches' : figure.get_size_inches(),
            'sketch_params' : figure.get_sketch_params(),
            'snap' : figure.get_snap(),
            'tight_layout' : figure.get_tight_layout(),
            'transform' : figure.get_transform(),
            'url' : figure.get_url(),
            'visible' : figure.get_visible(),
            'zorder' : figure.get_zorder(),
        },
        'constrained_layout_pads' : dict(zip(['w_pad', 'h_pad', 'wspace', 'hspace'], figure.get_constrained_layout_pads())),
        'axes' : figure.get_axes()
    }

    # Pickle the data
    with open(fpath, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

def load_figure(fpath):
    # Taken from https://github.com/matplotlib/matplotlib/blob/4f5cacfde9024076d9ab0cb6ad1c9a7cf352d5f9/lib/matplotlib/figure.py#L46
    def _stale_figure_callback(self, val):
        if self.figure:
            self.figure.stale = val

    # Taken from https://github.com/matplotlib/matplotlib/blob/4f5cacfde9024076d9ab0cb6ad1c9a7cf352d5f9/lib/matplotlib/figure.py#L776
    def _add_axes_internal(fig, ax, key):
        fig._axstack.add(ax)
        fig._localaxes.add(ax)
        fig.sca(ax)
        ax._remove_method = fig.delaxes
        # this is to support plt.subplot's re-selection logic
        ax._projection_init = key
        fig.stale = True
        ax.stale_callback = _stale_figure_callback

    # Unpickle the data
    with open(fpath, 'rb') as pkl_file:
            data = pickle.load(pkl_file)

    # Sett all the figure properties from the data
    new_fig = plt.figure(1)
    new_fig.set(**data['fig_props'])
    new_fig.set_constrained_layout_pads(**data['constrained_layout_pads'])

    # Add in the axes (this is the hard part)
    new_fig._localaxes = _AxesStack()
    new_fig._axstack = _AxesStack()
    for ax in data['axes']:
        # Taken from https://github.com/matplotlib/matplotlib/blob/4f5cacfde9024076d9ab0cb6ad1c9a7cf352d5f9/lib/matplotlib/figure.py#L770
        projection_class, pkw = new_fig._process_projection_requirements() # TODO: Figure out the projection requirements from the axis and pass them to this function
        key = (projection_class, pkw)
        _add_axes_internal(new_fig, ax, key)
        ax.figure = new_fig

    return new_fig
