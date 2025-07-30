#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 07/12/2022
#  Time: 01:56 p.m.
"""Stats generator

This file allows the user to generate stats for reports.

This file requires the following imports: 'datetime', 'itertools', 'math', 'pandas.

This file contains the following functions:
    * get_key - Function for itertools that removes milliseconds in date
    * get_groupby - returns filtered DataFrame groupby object
    * get_df_from_condition - returns query filtered column from DataFrame
    * get_groupby_from_df - returns a DataFrame as itertools.groupby object
    * get_dict_from_groupby - returns a dictionary from itertools.groupby object
    * get_df_from_key_value_pair - creates a DataFrame from dictionary
    * get_results_df_from_condition - returns a query filtered DataFrame
    * get_results_dict_from_condition - returns a dictionary from itertools.groupby object
    * generate_stats - generates a global and per-method stats DataFrame
    * generate_stats_dataframe - generates a global or per-method stats DataFrame
    * generate_errors_stats - returns a global or per-method error stats DataFrame
    * generate_errors_stats_dataframe - returns a global or per-method error stats DataFrame
"""
import datetime as dt
import itertools as it
import math

import pandas as pd


def get_key(d: 'dt'):
    """
    Function for itertools that removes milliseconds in date.

    Parameters
    ----------
    d
        Date to be reformatted

    Returns
    -------
    datetime
        Fate without milliseconds
    """
    k = d - dt.timedelta(seconds=d.second % 1)
    return dt.datetime(k.year, k.month, k.day, k.hour, k.minute, k.second)


def get_groupby(df: 'pd.DataFrame',
                column: 'str'):
    """
    Returns a filtered DataFrame groupby object.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be grouped by
    column: str
        Column name

    Returns
    -------
    it.groupby
        DataFrame grouped by given column groupby object
    """
    return it.groupby(sorted(pd.to_datetime(df[column]).tolist()), key=get_key)


def get_df_from_condition(df: 'pd.DataFrame',
                          query: 'str',
                          column: 'str',
                          final_column_name: 'str'):
    """
    Gets a query filtered column from DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be filtered
    query: str
        Query to be used
    column: str
        Column to be filtered
    final_column_name
        Resulting column name

    Returns
    -------
    pandas.DataFrame
        Query filtered column from DataFrame
    """
    return pd.DataFrame(((df.query(query))[column]).tolist(), columns=[final_column_name])


def get_groupby_from_df(df: 'pd.DataFrame',
                        query: 'str',
                        column: 'str',
                        final_column_name: 'str'):
    """
    Gets a DataFrame as itertools.groupby object.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be filtered
    query: str
        Query to be used
    column: str
        Column to be filtered
    final_column_name
        Resulting column name

    Returns
    -------
    itertools.groupby
        DataFrame as a groupby object
    """
    return get_groupby(get_df_from_condition(df, query, column, final_column_name), final_column_name)


def get_dict_from_groupby(groupby: 'it.groupby'):
    """
    Returns a dictionary from itertools.groupby object.

    Parameters
    ----------
    groupby: it.groupby
        itertools.groupby object

    Returns
    -------
    dict
        dictionary from itertools.groupby object
    """
    return_dict = {}
    for key, items in groupby:
        values = []
        for item in items:
            values.append(str(item))
        return_dict[key] = values.copy()
    return return_dict


def get_df_from_key_value_pair(d: 'dict'):
    """
    Creates a DataFrame from dictionary.

    Parameters
    ----------
    d: dict
        Dictionary to be converted to DataFrame

    Returns
    -------
    pandas.DataFrame
        DataFrame from dictionary given
    """
    return pd.DataFrame(index=list(d.keys()), data=d.values())


def get_results_df_from_condition(df: 'pd.DataFrame',
                                  query: 'str',
                                  column: 'str',
                                  final_column_name: 'str'):
    """
    Gets a query filtered DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be filtered
    query: str
        Query to be used
    column: str
        Column to be filtered
    final_column_name
        Resulting column name

    Returns
    -------
    pandas.DataFrame
        Query filtered DataFrame
    """
    return get_df_from_key_value_pair(get_results_dict_from_condition(df, query, column, final_column_name))


def get_results_dict_from_condition(df: 'pd.DataFrame',
                                    query: 'str',
                                    column: 'str',
                                    final_column_name: 'str'):
    """
    Gets a dictionary from itertools.groupby object.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be filtered
    query: str
        Query to be used
    column: str
        Column to be filtered
    final_column_name
        Resulting column name

    Returns
    -------
    dict
        Dictionary from itertools.groupby object
    """
    return get_dict_from_groupby(get_groupby_from_df(df, query, column, final_column_name))


def generate_stats(df: 'pd.DataFrame',
                   start: 'dt.datetime',
                   end: 'dt.datetime'):
    """
    Generates global and per-method stats DataFrame.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        DataFrame to be transformed
    start: datetime.datetime
        DataFrame start time
    end: datetime.datetime
        DataFrame end time

    Returns
    -------
    pandas.core.frame.DataFrame
        Global and per-method stats DataFrame
    """
    methods = set(df['MethodName'])
    full_df = generate_stats_dataframe(df, start, end, True)
    for method in methods:
        full_df = pd.concat(
            [full_df, generate_stats_dataframe(df.query(str("MethodName == '" + method + "'")), start, end, False)])
    return full_df


def generate_stats_dataframe(df: 'pd.DataFrame',
                             start: 'dt.datetime',
                             end: 'dt.datetime',
                             global_flag: 'bool'):
    """
    Generates global or per-method stats DataFrame.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        DataFrame to be transformed
    start: datetime.datetime
        DataFrame start time
    end: datetime.datetime
        DataFrame end time
    global_flag: bool
        If data is global or per-method

    Returns
    -------
    pandas.core.frame.DataFrame
        Stats DataFrame
    """
    if global_flag:
        scope = ['Global']
    else:
        scope = list(set(df['MethodName']))
    sps_df = get_results_df_from_condition(df, 'Result == 0', 'End', 'ts')
    fps_df = get_results_df_from_condition(df, 'Result == 1', 'End', 'ts')
    if (type(df['End'].values[0])) is str:
        datetime_format = '%Y-%m-%d %H:%M:%S.%f'
        df['Start'] = df['Start'].apply(lambda x: dt.datetime.strptime(x, datetime_format))
        df['End'] = df['End'].apply(lambda x: dt.datetime.strptime(x, datetime_format))
    mean_time = ((df['End'] - df['Start']).mean()).total_seconds()
    min_time = ((df['End'] - df['Start']).min()).total_seconds()
    max_time = ((df['End'] - df['Start']).max()).total_seconds()
    fps = fps_df.count(axis=1).mean()
    sps = sps_df.count(axis=1).mean()
    test_duration = (end - start).total_seconds()
    request_stats = {'Test duration(s)': float(test_duration),
                     'Requests': len(df),
                     'Success': len(df.query('Result == 0')),
                     'Fails': len(df.query('Result == 1')),
                     'Mean(s)': float(mean_time),
                     'Min(s)': float(min_time),
                     'Max(s)': float(max_time),
                     'Fails/s': 0 if math.isnan(fps) else fps,
                     'Success/s': 0 if math.isnan(sps) else sps
                     }

    return pd.DataFrame(request_stats, index=[scope[0]])


def generate_errors_stats(df: 'pd.DataFrame'):
    """
    Gets global and per-method error stats DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be transformed

    Returns
    -------
    dict
        Dictionary with error stats DataFrames for each method
    """
    errors_df = df.query('Result == 1')
    total_errors = len(errors_df)
    methods = set(df['MethodName'])

    full_df = {'Global': generate_errors_stats_dataframe(df)}
    for method in methods:
        temp = {str(method): generate_errors_stats_dataframe(df.query(str("MethodName == '" + method + "'")))}
        full_df.update(temp)
    return full_df


def generate_errors_stats_dataframe(df: 'pd.DataFrame'):
    """
    Gets global or per-method error stats DataFrame.

    Parameters
    ----------
    df: pd.DataFrame
        DataFrame to be transformed

    Returns
    -------
    pandas.DataFrame
        Error stats DataFrame with columns ['Error', 'Incidencias', 'Porcentaje']
    """
    errors_df = df.query('Result == 1')
    total_errors = len(errors_df)
    
    # Always return a DataFrame with the expected columns, even if empty
    if total_errors <= 0:
        return pd.DataFrame(columns=['Error', 'Incidencias', 'Porcentaje'])
    
    bd_df = errors_df.StatusCode.value_counts().reset_index().rename(
        columns={'StatusCode': 'Error', 'count': 'Incidencias'})

    bd_df['Incidencias'] = pd.to_numeric(bd_df['Incidencias'], errors='coerce').fillna(0)

    percents = pd.DataFrame(bd_df['Incidencias'].map(lambda error: str((error * 100) / total_errors) + "%")).rename(
        columns={'Incidencias': 'Porcentaje'})
    return pd.concat([bd_df, percents], axis=1)
