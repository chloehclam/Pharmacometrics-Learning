import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_effect_concentration(
    dfs,
    labels=None,
    title="PK/PD profile",
    filename=None,
    show=False,
    target_points=None,
):
    """
    Plot effect versus concentration, with optional labeled target points.

    Parameters
    ----------
    dfs : pandas.DataFrame or list of pandas.DataFrame
        DataFrame(s) containing ``Concentration (mg/L)`` and ``Effect``.
    labels : list of str, optional
        Labels for the plotted profiles.
    title : str, optional
        Plot title.
    filename : str or pathlib.Path, optional
        Destination for saving the plot. If None, the plot is not saved.
    show : bool, optional
        If True, display the plot.
    target_points : iterable of (float, float), optional
        Target points given as (concentration, effect) pairs. Each point is
        marked and labeled with its coordinates.

    Raises
    ------
    ValueError
        If the input DataFrames lack required columns, or if the number of
        labels does not match the number of DataFrames.
    """
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]
    elif not isinstance(dfs, list):
        raise ValueError("dfs must be a pandas DataFrame or a list of DataFrames.")

    for df in dfs:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Each item in dfs must be a pandas DataFrame.")
        required_columns = {"Concentration (mg/L)", "Effect"}
        if not required_columns.issubset(df.columns):
            raise ValueError(
                "Each DataFrame must contain 'Concentration (mg/L)' and 'Effect' columns."
            )

    if labels is not None and len(labels) != len(dfs):
        raise ValueError("The number of labels must match the number of DataFrames.")

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, df in enumerate(dfs):
        label = labels[i] if labels is not None else None
        ax.plot(
            df["Concentration (mg/L)"],
            df["Effect"],
            label=label,
        )

    if target_points is not None:
        offsets = [(10, 10), (10, -20), (-10, 10)]

        for index, point in enumerate(target_points):
            if len(point) != 2:
                raise ValueError(
                    "Each target point must be a (concentration, effect) pair."
                )

            concentration, effect = point
            offset = offsets[index % len(offsets)]
            alignment = "left" if offset[0] > 0 else "right"

            ax.scatter(concentration, effect, color="red", zorder=3)
            ax.annotate(
                f"({concentration:.2f}, {effect:.2f})",
                xy=(concentration, effect),
                xytext=offset,
                textcoords="offset points",
                ha=alignment,
                bbox={
                    "boxstyle": "round,pad=0.2",
                    "facecolor": "white",
                    "edgecolor": "none",
                    "alpha": 0.8,
                },
            )

    ax.set_xlabel("Concentration (mg/L)")
    ax.set_ylabel("Effect")
    ax.set_title(title)

    if labels is not None:
        ax.legend()

    ax.grid(True)
    fig.tight_layout()

    if filename is not None:
        fig.savefig(filename, dpi=200)

    if show:
        plt.show()

    plt.close(fig)


def plot_effect_time(
    dfs,
    labels=None,
    title="Effect-Time Profile",
    filename=None,
    show=False,
):
    """
    Plot effect versus time.

    Parameters
    ----------
    dfs : pandas.DataFrame or list of pandas.DataFrame
        DataFrame(s) containing ``Time (hr)`` and ``Effect``.
    labels : list of str, optional
        Labels for the plotted profiles.
    title : str, optional
        Plot title.
    filename : str or pathlib.Path, optional
        Destination for saving the plot. If None, the plot is not saved.
    show : bool, optional
        If True, display the plot.

    Raises
    ------
    ValueError
        If the input DataFrames lack required columns, or if the number of
        labels does not match the number of DataFrames.
    """
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]
    elif not isinstance(dfs, list):
        raise ValueError("dfs must be a pandas DataFrame or a list of DataFrames.")

    for df in dfs:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Each item in dfs must be a pandas DataFrame.")
        required_columns = {"Time (hr)", "Effect"}
        if not required_columns.issubset(df.columns):
            raise ValueError(
                "Each DataFrame must contain 'Time (hr)' and 'Effect' columns."
            )

    if labels is not None and len(labels) != len(dfs):
        raise ValueError("The number of labels must match the number of DataFrames.")

    fig, ax = plt.subplots(figsize=(8, 5))

    for i, df in enumerate(dfs):
        label = labels[i] if labels is not None else None
        ax.plot(
            df["Time (hr)"],
            df["Effect"],
            label=label,
        )

    ax.set_xlabel("Time (hr)")
    ax.set_ylabel("Effect")
    ax.set_title(title)

    if labels is not None:
        ax.legend()

    ax.grid(True)
    fig.tight_layout()

    if filename is not None:
        fig.savefig(filename, dpi=200)

    if show:
        plt.show()

    plt.close(fig)