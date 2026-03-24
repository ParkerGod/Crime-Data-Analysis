import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Tuple


def setup_plotting_style():
    sns.set_style("whitegrid")
    sns.set_palette("husl")
    plt.rcParams.update({
        "font.size": 12,
        "axes.titlesize": 16,
        "axes.labelsize": 12
    })


def save_figure(
    fig: plt.Figure,
    filename: str,
    output_dir: Path,
    dpi: int = 150,
    tight_layout: bool = True
) -> Path:
    if tight_layout:
        fig.tight_layout()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    fig.savefig(filepath, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return filepath


def create_bar_plot(
    data,
    x: str = None,
    y: str = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (10, 6),
    palette: str = "cubehelix",
    horizontal: bool = False
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    if horizontal:
        if hasattr(data, "index") and hasattr(data, "values"):
            sns.barplot(x=data.values, y=data.index, palette=palette, ax=ax, width=0.5)
        else:
            sns.barplot(x=x, y=y, data=data, palette=palette, ax=ax)
    else:
        if hasattr(data, "index") and hasattr(data, "values"):
            sns.barplot(x=data.index, y=data.values, palette=palette, ax=ax)
        else:
            sns.barplot(x=x, y=y, data=data, palette=palette, ax=ax)
    ax.set_title(title, fontsize=20, weight="bold")
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.grid(True, linestyle="--", alpha=0.7)
    return fig


def create_histogram(
    data,
    bins: int = 20,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "Frequency",
    figsize: Tuple[int, int] = (10, 6),
    color: str = "green",
    kde: bool = True
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    sns.histplot(data, bins=bins, kde=kde, color=color, ax=ax)
    ax.set_title(title, fontsize=20, weight="bold")
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    return fig


def create_heatmap(
    data,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (10, 6),
    cmap: str = "Blues",
    extent: Optional[Tuple[float, float, float, float]] = None
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    if extent:
        im = ax.imshow(data.T, cmap=cmap, origin="lower", aspect="auto", extent=extent)
    else:
        im = ax.imshow(data.T, cmap=cmap, origin="lower", aspect="auto")
    plt.colorbar(im, ax=ax, label="Crime Density")
    ax.set_title(title, fontsize=20, weight="bold")
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.grid(True, linestyle="-", color="black", alpha=0.3)
    return fig


def create_pie_chart(
    data,
    title: str = "",
    figsize: Tuple[int, int] = (8, 8),
    explode: Optional[Tuple[float, ...]] = None,
    palette: str = "Spectral"
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    colors = sns.color_palette(palette, n_colors=len(data))
    if explode is None:
        explode = tuple([0.1] * len(data))
    ax.pie(
        data,
        autopct="%1.1f%%",
        startangle=120,
        colors=colors,
        textprops={"fontsize": 12, "fontweight": "bold"},
        explode=explode,
        labels=None,
        pctdistance=0.85
    )
    ax.set_title(title, fontsize=18, weight="bold")
    ax.axis("equal")
    labels = data.index.tolist()
    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=10)
        for color in colors
    ]
    ax.legend(
        handles=legend_handles,
        labels=labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=12
    )
    return fig


def create_strip_plot(
    data,
    x: str,
    y: str,
    hue: str,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (12, 6),
    palette: str = "coolwarm",
    rotation: int = 25
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    sns.stripplot(
        data=data,
        x=x,
        y=y,
        hue=hue,
        jitter=True,
        dodge=True,
        alpha=0.7,
        palette=palette,
        ax=ax
    )
    ax.set_title(title, fontsize=20, weight="bold")
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    ax.tick_params(axis="x", rotation=rotation)
    ax.legend(title=hue, fontsize=14)
    return fig


def create_line_plot(
    data,
    x: str = None,
    y: str = None,
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    figsize: Tuple[int, int] = (10, 8),
    marker: str = "o",
    hue: str = None
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    if hue:
        for col in data.columns:
            sns.lineplot(y=data.index, x=data[col], label=col, marker=marker, ax=ax)
    else:
        sns.lineplot(x=x, y=y, data=data, marker=marker, ax=ax)
    ax.set_title(title, fontsize=20, weight="bold")
    ax.set_xlabel(xlabel, fontsize=16)
    ax.set_ylabel(ylabel, fontsize=16)
    if hue:
        ax.legend(title=hue, bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=14)
    return fig
