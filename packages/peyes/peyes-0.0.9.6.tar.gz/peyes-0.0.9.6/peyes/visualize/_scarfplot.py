import numpy as np
import plotly.graph_objects as go

import peyes._utils.visualization_utils as vis_utils
from peyes._DataModels.EventLabelEnum import EventLabelEnum, EventLabelSequenceType


def scarfplot_comparison_figure(
        t: np.ndarray, *labels, **kwargs
) -> go.Figure:
    """
    Creates a figure with multiple scarfplots stacked on top of each other.
    :param t: The time axis.
    :param labels: multiple sequences of event labels to be plotted, each must have the same length as `t`.
    :keyword scarf_height: The height (in y-axis units) of each scarfplot, default is 1.
    :keyword scarf_spacing: The spacing (in y-axis units) between scarfplots, default is 0.25.
    :keyword label_colors: A dictionary mapping event labels to their respective colors. If a label is missing, the
        default color is used.
    :keyword title: The title of the figure, default is "Scarfplot Comparison".
    :keyword names: The names of the scarfplots, default is [0, 1, 2, ...].
    :return: The figure with the scarfplots.
    """
    num_scarfs = len(labels)
    scarf_height = kwargs.get("scarf_height", 1)
    scarf_spacing = 1 + kwargs.get("scarf_spacing", 0.25)
    label_colors = vis_utils.get_label_colormap(kwargs.get("label_colors", None))
    fig = go.Figure()
    for i, l in enumerate(labels):
        bottom, top = scarf_spacing * i * scarf_height, (scarf_spacing * i + 1) * scarf_height
        fig = add_scarfplot_to_figure(fig, t, l, top, bottom, label_colors=label_colors, show_colorbar=i == 0)
    names = kwargs.get("names", [str(i) for i in range(num_scarfs)])
    assert len(names) == num_scarfs
    fig.update_layout(
        title=kwargs.get("title", "Scarfplot Comparison"),
        yaxis=dict(
            range=[0, 1 + scarf_spacing * scarf_height * (num_scarfs - 1)],
            tickmode='array',
            tickvals=[(scarf_spacing * i + 0.5) * scarf_height for i in range(num_scarfs)],
            ticktext=names,
        ),
    )
    return fig


def add_scarfplot_to_figure(
        fig: go.Figure,
        t: np.ndarray,
        labels: EventLabelSequenceType,
        top: float,
        bottom: float,
        label_colors: vis_utils.LabelColormapType = None,
        colorbar_length: float = 1,
        colorbar_thickness: int = 25,
        show_colorbar: bool = True,
) -> go.Figure:
    """
    Adds a scarfplot to the provided figure.

    :param fig: the figure to add the scarfplot to.
    :param t: the time axis, must have the same length as `labels`.
    :param labels: the event labels to plot, must have the same length as `t`.
    :param top: the top y-coordinate of the scarfplot.
    :param bottom: the bottom y-coordinate of the scarfplot.
    :param label_colors: a dictionary mapping event labels to their respective colors. If a label is missing, the
        default color is used.
    :param colorbar_length: the length of the colorbar (range [0, 1] where 1 is the full height of the plot), default is 1.
    :param colorbar_thickness: the thickness of the colorbar, default is 25.
    :param show_colorbar: whether to show the colorbar, default is True.
    """
    assert len(t) == len(labels), f"Length mismatch: len(t)={len(t)} != {len(labels)}=len(labels)"
    label_colors = vis_utils.get_label_colormap(label_colors)
    label_colors = {k: v for k, v in label_colors.items() if k in labels}   # Remove unused colors
    colormap, tick_centers = _discrete_colormap(label_colors)
    # # Normalize tick centers to [0, 1]
    # see https://community.plotly.com/t/heatmap-colorbar-displays-ticks-in-incorrect-locations/84278/3?u=jonnir
    tick_centers = tick_centers * colorbar_length * (np.max(tick_centers) - np.min(tick_centers)) / len(tick_centers)
    scarfplot = go.Heatmap(
        x=t,
        y=[bottom, top],
        z=[np.asarray(labels, dtype=EventLabelEnum)],
        zmin=min(EventLabelEnum),
        zmax=max(EventLabelEnum),
        colorscale=colormap,
        colorbar=dict(
            len=colorbar_length,
            thickness=colorbar_thickness,
            tickvals=tick_centers,
            ticktext=list(map(lambda lbl: EventLabelEnum(lbl).name, label_colors.keys())),
        ),
        showscale=show_colorbar,
    )
    fig.add_trace(scarfplot)
    return fig


def _discrete_colormap(colors: dict):
    borders = np.arange(len(colors) + 1)
    centers = (borders[1:] + borders[:-1]) / 2
    borders = borders / len(colors)  # Normalize to [0, 1]
    colormap = []
    for i, key in enumerate(sorted(colors.keys())):
        colormap.extend([(borders[i], f"rgb{colors[key]}"), (borders[i + 1], f"rgb{colors[key]}")])
    return colormap, centers
