#
#  Created by IntelliJ IDEA.
#  User: jahazielaa
#  Date: 09/12/2022
#  Time: 10:12 a.m.
"""HTML creator

This file allows the user to create a HTML report for RPSs results.

This file requires the following imports: 'datetime', 'ntpath'.

This file contains the following functions:
    * path_leaf - returns properly formatted directory path
    * bootstrapify - returns a HTML table in light or dark mode
    * get_html_string - returns the first part of an HTML document for reports and includes summary RPSs table
    * add_figure - returns an HTML document with a new figure added
    * add_full_requests - returns an HTML document with full RPSs table
    * add_requests_section - returns an HTML snippet for 'Requests' section
    * add_new_section - returns an HTML snippet for new section
    * add_section_content - returns an HTML snippet delimited by HTML breaks
    * get_break - returns an HTML breaks HTML snippet
    * close_html_string - returns an HTML document with 'body' and 'head' tags closed
"""
import datetime as dt
import ntpath


def path_leaf(path: 'str'):
    """
    Gets properly formatted directory path.

    Parameters
    ----------
    path: str
        Directory path given

    Returns
    -------
    Properly formatted directory path
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def bootstrapify(df: 'pandas.core.frame.DataFrame',
                 dark_mode: 'bool'):
    """
    Assigns proper classes to tables.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        Dataframe for html table
    dark_mode: bool
        Dark mode flag
    Returns
    -------
    str
        Properly colored and formatted html string for table
    """
    if dark_mode:
        return df.to_html().replace('<table border="1" class="dataframe">',
                                    '<table class="table table-striped table-hover '
                                    'table-bordered table-responsive table-dark">')
    else:
        return df.to_html().replace('<table border="1" class="dataframe">',
                                    '<table class="table table-striped table-hover table-responsive table-bordered">')


def get_html_string(df: 'pandas.core.frame.DataFrame',
                    dark_mode: 'bool',
                    testing: 'bool',
                    dir_name: 'str'):
    """
    Gets generic HTML document for reports and summary table.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        Summary table DataFrame
    dark_mode: bool
        Dark mode flag
    testing: bool
        Flag for testing mode or report generation mode
    dir_name: str
        Directory path

    Returns
    -------
    str
        HTML generic document for report
    """
    if testing:
        report_name = '''<h1>Reporte ''' + str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '''</h1>'''
    else:
        report_name = '''<h1>Reporte ''' + path_leaf(dir_name) + '''</h1>'''
    if dark_mode:
        style = '''
        <style>
            body {
                padding: 25px;
                margin: 0 100;
                background-color: black;
                background: #121212;
                color: #eee;
            }
        </style>'''
    else:
        style = '''
        <style>
            body {
                padding: 25px;
                margin: 0 100;
                background-color: whitesmoke;
                background: #fff;
                color: #222;
            }
        </style>'''
    general_report = bootstrapify(df, dark_mode)
    return '''
    <html>
        <head>
        
            <!-- CSS only -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" 
            integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" 
            crossorigin="anonymous">

            
            <!-- JavaScript Bundle with Popper -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" 
                integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" 
                crossorigin="anonymous">
            </script>

            ''' + style + '''
        </head>
        <body>
            ''' + report_name + '''
            <hr>

            <!-- *** Resultados *** --->
            <h2>Resultados generales:</h2>
            ''' + general_report + '''
            <br/>
            <!-- *** Gráficas *** --->
            <h2>Resultados gráficos:</h2>
            '''


def add_figure(html_string: 'str',
               figure: 'str'):
    """
    Adds figure to HTML report.

    Parameters
    ----------
    html_string: str
        HTML document string
    figure: str
        Figure HTML string to be added to HTML document string

    Returns
    -------
    str
        HTML document string
    """
    html_string += (get_break() + figure + get_break())

    return html_string


def add_full_requests(html_string: 'str',
                      requests_df: 'pandas.core.frame.DataFrame',
                      dark_mode: 'bool'):
    """
    Add full requests table to HTML document.

    Parameters
    ----------
    html_string: str
        HTML document string
    requests_df: pandas.core.frame.DataFrame
        Full requests DataFrame
    dark_mode: bool
        Dark mode flag

    Returns
    -------
    str
        HTML document string
    """
    df = requests_df[
        ['MethodName', 'Method', 'StatusMessage', 'StatusCode', 'Content']].value_counts().reset_index().rename(
        columns={'MethodName': 'Método', 'Method': 'Ruta', 'StatusMessage': 'Mensaje',
                 'StatusCode': 'Código de estatus', 'Content': 'Contenido', 0: 'Incidencias'})
    summarized_requests_section = (get_break() + bootstrapify(df, dark_mode))
    full_requests_section = get_break() + bootstrapify(requests_df, dark_mode)
    tables = {'Resumen': summarized_requests_section, 'Todas': full_requests_section}
    html_string += add_requests_section()
    for table in tables.keys():
        if table == 'Resumen':
            height = 'auto'
        else:
            height = '600px'
        html_string += ('''
    <div style="width: 100%; height: ''' + height + '''; overflow-y: scroll;">
    <h4>''' + str(table) + '''</h4>
    <br/>
    ''' + tables[table] + get_break()) + '''
    </div>
    '''
    return html_string


def add_requests_section():
    """
    Adds Requests section title.

    Returns
    -------
    str
        Requests title HTMl string
    """
    return add_new_section('Peticiones')


def add_new_section(section: 'str'):
    """
    Adds new section title.

    Parameters
    ----------
    section: str
        New section title

    Returns
    -------
    str
        New section title HTML string
    """
    return get_break() + '''
            <!-- *** ''' + section + ''''*** --->
            <h2>''' + section + ''':</h2>
    '''


def add_section_content(content: 'str'):
    """
    Adds breaks to HTML snippet.
    Parameters
    ----------
    content: str
        HTML snippet

    Returns
    -------
    str
        HTML snippet delimited by breaks
    """
    return get_break() + content + get_break()


def get_break():
    """
    Gets HTML break tag.

    Returns
    -------
    str
        HTML break tag
    """
    return '''
    <br/>
    '''


def close_html_string(html_string: 'str'):
    """
    Closes 'body' abd 'html' tags.

    Parameters
    ----------
    html_string: str
        HTML document string

    Returns
    -------
    str
        HTML document string with 'body' and 'html' tags closed
    """
    html_string += '''
        </body>
    </html>'''
    return html_string
