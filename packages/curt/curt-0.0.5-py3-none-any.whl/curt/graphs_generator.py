#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:59 p.m.
"""Graphs generator

This file allows the user to generate graphs for REST requests.

This file requires the following imports: 'collections', 'math',
'plotly'.

This file contains the following functions:
    * total_rps - returns a line connected scatter plot for total RPSs
    * errors_graph - returns a GET request response
    * stacked_total_rps - returns a line connected scatter plot for total successful and failed RPSs
    * show_fig - shows Plotly figure
    * get_fig_errors_graph - returns errors chart figure
    * get_fig_stacked_errors_graph - returns a set of graphs in two columns
    * configure_stacked_error_graph - returns any Error graph with info text properties
    * full_errors_graph - returns a graph for all errors
"""

import collections
import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def total_rps(df: 'pandas.core.frame.DataFrame',
              x: 'str',
              y: 'str',
              z: 'str',
              title: 'str',
              xaxis_title: 'str',
              yaxis_title: 'str',
              legend_title: 'str',
              font_family: 'str',
              font_size: 'int',
              font_color):
    """
    Creates a line connected scatter plot for total requests per second.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Processed loadtest data dataframe
    x : str
        X-axis dimension name
    y : str
        Y-axis dimension name
    z : str
        Z-axis dimension name, 'NULL' if there's none
    title : str
        Chart title
    xaxis_title : str
        X-axis title
    yaxis_title : str
        Y-axis title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name

    Returns
    -------
    None
    """

    fig = go.Figure([go.Scatter(x=df[x], y=df[y], name=y)])
    if z != 'NULL':
        fig.add_scatter(x=df[x], y=df[z], name=z)

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        )
    )
    fig.show()


def errors_graph(df: 'pandas.core.frame.DataFrame',
                 title: 'str',
                 legend_title: 'str',
                 font_family: 'str',
                 font_size: 'int',
                 font_color: 'str',
                 dark_mode: 'bool'):
    """
    Gets errors chart.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Processed loadtest error data dataframe
    title : str
        Chart title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name
    dark_mode : bool
        Dark mode flag

    Returns
    -------
    None
    """

    get_fig_errors_graph(df, title, legend_title, font_family, font_size, font_color, dark_mode).show()


def stacked_total_rps(df: 'pandas.core.frame.DataFrame',
                      x: 'str',
                      y: 'str',
                      z: 'str',
                      title: 'str',
                      xaxis_title: 'str',
                      yaxis_title: 'str',
                      legend_title: 'str',
                      font_family: 'str',
                      font_size: 'int',
                      font_color: 'str',
                      dark_mode: 'bool'):
    """
     Creates a line connected scatter plot for total successful and failed requests per second.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Processed loadtest data dataframe
    x : str
        X-axis dimension name
    y : str
        Y-axis dimension name
    z : str
        Z-axis dimension name, 'NULL' if there's none
    title : str
        Chart title
    xaxis_title : str
        X-axis title
    yaxis_title : str
        Y-axis title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name
    dark_mode : bool
        Dark mode flag

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Total RPS plotly figure
    """
    if dark_mode:
        template = 'plotly_dark'
        font_color = 'whitesmoke'
    else:
        template = 'plotly'
    traces = list()
    columns = df.columns.values.tolist()
    length = len(df[columns[0]].iloc[df[columns[0]].index.get_loc(x)])
    temp_dict = {}
    for column in columns:
        temp_dict_2 = {}
        temp = df[str(column)]
        for i in range(length):
            if z == 'NULL':
                try:
                    temp_dict_2.update({temp.iloc[temp.index.get_loc(x)][i]: {0: temp.iloc[temp.index.get_loc(y)][i]}})
                except IndexError:
                    pass
            else:
                try:
                    temp_dict_2.update({temp.iloc[temp.index.get_loc(x)][i]: {0: temp.iloc[temp.index.get_loc(y)][i],
                                                                              1: temp.iloc[temp.index.get_loc(z)][i]}})
                except IndexError:
                    pass
            temp_dict.update({column: collections.OrderedDict(sorted(temp_dict_2.items()))})

    for method in temp_dict.keys():
        temp = temp_dict[method]
        traces.append(
            go.Scatter(x=list(temp.keys()), y=list(map(lambda a: a[0], list(temp.values()))),
                       name=y + ' (' + str(method) + ')')
        )
        if z != 'NULL':
            traces.append(
                go.Scatter(x=list(temp.keys()), y=list(map(lambda a: a[1], list(temp.values()))),
                           name=z + ' (' + str(method) + ')')
            )

    fig = go.Figure(data=traces)

    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        ),
        template=template
    )
    return fig


def show_fig(fig: 'go.Figure'):
    """
    Shows Plotly figure.

    Parameters
    ----------
    fig: 'plotly.graph_objs._figure.Figure'
        Figure to be shown.

    Returns
    -------
    None
    """
    fig.show()


def get_fig_errors_graph(df: 'pandas.core.frame.DataFrame',
                         title: 'str',
                         legend_title: 'str',
                         font_family: 'str',
                         font_size: 'int',
                         font_color: 'str',
                         dark_mode: 'bool'):
    """
    Creates errors chart.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Processed loadtest error data dataframe
    title : str
        Chart title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name
    dark_mode : bool
        Dark mode flag

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Errors plotly figure
    """

    if dark_mode:
        template = 'plotly_dark'
        font_color = 'whitesmoke'
    else:
        template = 'plotly'
    errors = df['Error'].map(lambda label: 'Código ' + str(label))
    fig = go.Figure(
        data=[go.Pie(labels=errors, values=df['Incidencias'])])
    fig.update_traces(hoverinfo='label+value', textfont_size=40, marker=dict(line=dict(color='#000000', width=1)),
                      insidetextorientation='radial')

    fig.update_layout(
        title=title,
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        ),
        template=template
    )
    return fig


def get_fig_stacked_errors_graph(graphs: 'list'):
    """
    Gets a set of graphs in two columns.

    Parameters
    ----------
    graphs: 'list'
        Charts names list.

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Stacked errors in two columns
    """
    fig = make_subplots(rows=(len(graphs) - 1), cols=math.ceil(len(graphs) / 2), subplot_titles=graphs)
    return fig


def configure_stacked_error_graph(fig: 'go.Figure',
                                  title: 'str',
                                  legend_title: 'str',
                                  font_family: 'str',
                                  font_size: 'int',
                                  font_color: 'str',
                                  dark_mode: 'bool'):
    """
    Configures any Error graph info text properties.

    Parameters
    ----------
    fig: 'plotly.graph_objs._figure.Figure'
        Figure to be configured.
    title : str
        Chart title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name
    dark_mode : bool
        Dark mode flag

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Configured figure
    """
    if dark_mode:
        template = 'plotly_dark'
        font_color = 'whitesmoke'
    else:
        template = 'plotly'
    fig.update_traces(hoverinfo='label+value', textfont_size=40, marker=dict(line=dict(color='#000000', width=1)),
                      insidetextorientation='radial')
    fig.update_layout(
        title=title,
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        ),
        template=template
    )
    return fig


def full_errors_graph(error_stats: 'dict',
                      title: 'str',
                      legend_title: 'str',
                      font_family: 'str',
                      font_size: 'int',
                      font_color: 'str',
                      dark_mode: 'bool'):
    """
    Creates a graph for all errors.

    Parameters
    ----------
    error_stats: 'dict'
        Error stats dictionary.
    title : str
        Chart title
    legend_title : str
        Legends section title
    font_family : str
        Font family name
    font_size : int
        Font size
    font_color : str
        Font color name
    dark_mode : bool
        Dark mode flag

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Full errors graph
    """
    if dark_mode:
        template = 'plotly_dark'
        font_color = 'whitesmoke'
    else:
        template = 'plotly'
    keys = list(error_stats.keys())

    # Filter out empty DataFrames before processing
    valid_keys = [key for key in keys if not error_stats.get(str(key)).empty]

    length = len(valid_keys)
    rows = math.ceil(math.sqrt(length))
    cols = math.ceil(length / rows)
    specs = [[{'type': 'domain'}] * cols] * rows

    fig = make_subplots(rows=rows, cols=cols, specs=specs, subplot_titles=valid_keys, print_grid=False)

    col = 0

    for i, l in enumerate(valid_keys):
        graphs = valid_keys[i]
        row = i // cols + 1
        col = col + 1
        if col > cols:
            col = 1
        df = error_stats.get(str(graphs))
        
        # Check if DataFrame has the required columns and is not empty
        if df is not None and not df.empty and 'Error' in df.columns and 'Incidencias' in df.columns:
            errors = list(df['Error'].map(lambda label: 'Código ' + str(label)))
            values = list(df['Incidencias'])
            if len(errors) != 0 and len(values) != 0:
                fig.add_trace(go.Pie(labels=errors, values=values, name=graphs), row=row, col=col)

    fig.update_traces(hoverinfo='label+value', textfont_size=40, marker=dict(line=dict(color='#000000', width=1)),
                      insidetextorientation='radial')
    fig.update_layout(
        title=title,
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size,
            color=font_color
        ),
        template=template
    )
    return fig
