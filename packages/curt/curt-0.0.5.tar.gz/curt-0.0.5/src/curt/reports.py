#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 09/12/2022
#  Time: 05:07 p.m.
"""Reports

This file allows the user to generate reports for loadtest data.

This file requires the following imports: 'datetime', 'os',
'webbrowser', 'pandas', 'curt'.

This file contains the following functions:
    * loadtest - generates loadtest reports
"""
import datetime as dt
import os
import webbrowser

import pandas as pd

import curt.graphs_generator as gg
import curt.html_creator as hc
import curt.stats_generator as sg


def loadtest(dark_mode: 'bool',
             dir_name: 'str',
             functions: 'list',
             df: 'pd.DataFrame',
             start_time: 'dt.datetime',
             end_time: 'dt.datetime',
             testing: 'bool'):
    """
    Generates loadtest reports.

    Parameters
    ----------
    dark_mode : bool
        Dark theme flag
    dir_name : str
        Previous or custom loadtest directory's name, otherwise use 'NULL'
    functions : list
        Functions names list
    df : pandas.core.frame.DataFrame
        Test's data DataFrame
    start_time : datetime.datetime
        Test start time
    end_time : datetime.datetime
        Test end time
    testing : bool
        True if loadtest data has not been reported, otherwise use False

    Returns
    -------
    None
    """

    df.sort_values(by='End', inplace=True)
    stats_df = sg.generate_stats(df, start_time, end_time)
    error_stats = sg.generate_errors_stats(df)
    
    # Check if any error DataFrame has data (not empty)
    errors_flag = False
    if error_stats:
        for method, error_df in error_stats.items():
            if not error_df.empty:
                errors_flag = True
                break
    
    print(stats_df)
    print('##########################################################################')
    print('Generando reporte...')

    successes = {}
    fails = {}
    function_names = list()
    for function in functions:
        function_names.append(function.__name__)

    for function in function_names:
        successes[function] = sg.get_results_dict_from_condition(df, ("Result == 0 & MethodName == '" + function + "'"),
                                                                 'End', 'ts')
        fails[function] = sg.get_results_dict_from_condition(df, ("Result == 1 & MethodName == '" + function + "'"),
                                                             'End', 'ts')
    success_data = {}
    fails_data = {}

    for function in function_names:
        temp_dict = {}
        for key in fails[function].keys():
            length = len(fails[function].get(key))
            temp = {str(key)[11:]: length if type(length) == int else 0}
            temp_dict.update(temp)
        fails_data[function] = temp_dict
        temp_dict = {}
        for key in successes[function].keys():
            length = len(successes[function].get(key))
            temp = {str(key)[11:]: length if type(length) == int else 0}
            temp_dict.update(temp)
        success_data[function] = temp_dict

    tiempos = []
    for function in function_names:
        for tiempo in fails_data[function]:
            tiempos.append(tiempo)
        for tiempo in success_data[function]:
            tiempos.append(tiempo)

    tiempos = list(set(tiempos))
    registros = len(tiempos)
    oks = {}
    kos = {}

    for function in function_names:
        oks_list = list()
        kos_list = list()
        for i in range(registros):
            if function in success_data:
                oks_list.insert(i, success_data[function][tiempos[i]] if tiempos[i] in success_data[function] else 0)
            else:
                oks_list.insert(i, 0)
            if function in fails_data:
                kos_list.insert(i, fails_data[function][tiempos[i]] if tiempos[i] in fails_data[function] else 0)
            else:
                kos_list.insert(i, 0)

        oks[function] = oks_list
        kos[function] = kos_list

    results_dict = {}
    responses_dict = {}

    for function in function_names:
        results_dict.update({function: {'Tiempo': tiempos,
                                        'OK': oks[function] if function in oks else 0,
                                        'KO': kos[function] if function in kos else 0
                                        }})

        temp = df.query(str("MethodName == '" + function + "'"))
        responses_dict.update({function: {'Inicio': temp['Start'].tolist(),
                                          'Respuesta': ((temp['End'] - temp['Start']).dt.total_seconds()).tolist()}})

    results_df = pd.DataFrame(results_dict)
    responses_df = pd.DataFrame(responses_dict)

    data = list()

    data.append(gg.stacked_total_rps(df=results_df, x='Tiempo', y='OK', z='KO', title="Peticiones por segundo totales",
                                     xaxis_title="Hora", yaxis_title="Número de RPS", legend_title="Tipo de peticiones",
                                     font_family="Courier New, monospace", font_size=18, font_color="RebeccaPurple",
                                     dark_mode=dark_mode))

    data.append(gg.stacked_total_rps(df=responses_df, x='Inicio', y='Respuesta', z='NULL', title="Tiempos de respuesta",
                                     xaxis_title="Hora", yaxis_title="Segundos", legend_title="Respuesta",
                                     font_family="Courier New, monospace", font_size=18, font_color="RebeccaPurple",
                                     dark_mode=dark_mode))

    if errors_flag:
        data.append(
            gg.full_errors_graph(error_stats=error_stats, title="Peticiones fallidas", legend_title="Código de error",
                                 font_family="Courier New, monospace", font_size=18, font_color="RebeccaPurple",
                                 dark_mode=dark_mode))

    print('Hecho.')
    print('##########################################################################')
    print('Generando index.html...')

    html = hc.get_html_string(stats_df, dark_mode, testing, dir_name)

    for figure in data:
        html = hc.add_figure(html, figure.to_html())

    html = hc.add_full_requests(html, df, dark_mode)

    if testing:
        filename = dir_name + '/index.html'
    else:
        filename = dir_name + '/index-' + str(dt.datetime.now().timestamp()) + '.html'

    f = open(filename, 'w', encoding='utf-8')
    f.write(hc.close_html_string(html))
    f.close()

    f_loc = os.path.realpath(filename)

    print('Reporte almacenado en: ' + f_loc)
    print('##########################################################################')
    print('Abriendo reporte...')

    webbrowser.open_new_tab('file://' + f_loc)
    print('Hecho.')
    print('##########################################################################')
    print('Ejecución finalizada.')
    print('##########################################################################')
