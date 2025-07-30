from loadData import gistDataBase
from plotData import *
from helperFunctions import *
from dash_iconify import DashIconify

from dash import Dash, dcc, callback, Output, Input, ctx, State, no_update, Patch, clientside_callback
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash.exceptions import PreventUpdate
import dash_auth

import warnings
warnings.filterwarnings("ignore")


# Incorporate data
module_names = ["TABLE", "MASK", "KIN", "GAS", "SFH", "LS"]
module_table_names = ["table", "Mask", "kinResults", "gasResults", "sfhResults", "lsResults"]
global database
database = gistDataBase()


# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# auth = dash_auth.BasicAuth(
#     app,
#     {
#         'testgeckos': 'geckostest'
#     }
# )




def create_property_groups(database):
    '''
    Function to create the selection buttons for all galxy properties
    :param database:
    :return:
    '''
    print("Function call create_property_groups")
    if hasattr(database, "module") == False:
        if database.KIN == True:
            database.module = "KIN"
        else:
            database.module = "TABLE"
    return [
            dmc.SegmentedControl(
                    id="module-select",
                    value=module_table_names[module_names.index(database.module)],
                    # value=None,
                    data=[{"value": "table", "label": "TABLE"}] +
                         [{"value": module_table_names[i], "label": module_names[i]}
                          for i in range(1, len(module_names)) if getattr(database, module_names[i])],
                    style={"width": "20vw", "marginTop": 12, "marginBottom": 12},
                ),
            dmc.Select(
                placeholder="choose a parameter",
                id="parameter-select",
                data=[{"value": parameter_i, "label": parameter_i}
                      for parameter_i in getattr(database, module_table_names[module_names.index(database.module)]).names],
                style={"width": '12vw', "marginTop": 12, "marginBottom": 12},
                maxDropdownHeight=500,
            ),
            dmc.ActionIcon(
                DashIconify(icon="ph:info-fill"),
                id="config-demo-button",
                color="blue",
                variant="filled",
                size="lg",
                style={"marginTop": 12, "marginBottom": 12}
            ),
            dmc.Modal(
                title="Master-Configuration",
                id="config-show",
                size="70%",
                zIndex=10000,
            ),
        ]


def create_main_table(database, value):
    '''
    Function to create AgGrid Table for inspection
    :param database:
    :param value:
    :return:
    '''
    print("Function call create_main_table")
    if value in ["table", "Mask"]:
        database.current_df = getattr(database, value+"_df")
    else:
        database.current_df = getattr(database, value+"_Vorbin_df")

    return  dag.AgGrid(
        id="main-table",
        rowData=database.current_df.to_dict("records"),
        # rowData=None,
        columnDefs=[{"field": i} for i in database.current_df.columns],
        columnSize="sizeToFit",
        columnSizeOptions={
            "defaultMinWidth": 120,
        },
        defaultColDef={"resizable": True, "sortable": True},
        rowModelType="infinite",
        className="ag-theme-balham",
        dashGridOptions={
           "rowBuffer": 0,
           "maxBlocksInCache": 1,
           "infiniteInitialRowCount": 20,
           "rowSelection":"single",
        },
        style={"height": "55vh"},
    )

def create_main_map(database):
    '''
    Function to create main property distribution map
    :param database:
    :return:
    '''
    print("Function call create_main_map")
    return dcc.Graph(id="main-map",
                 figure=plotMap(database, database.module, database.maptype),
                 style={"height": "55vh"},
                 )


def update_main_map_selectedbin(database, patched_main_map):
    '''
    Using Patch function to update main table when selecting a VorBin
    :param database:
    :param patched_main_map:
    :return:
    '''
    if hasattr(database, "idxBinShort") == True:
        patched_main_map.data[1]['x'] = [database.table.XBIN[database.table['BIN_ID']==database.idxBinShort][0]]
        patched_main_map.data[1]['y'] = [database.table.YBIN[database.table['BIN_ID']==database.idxBinShort][0]]
    else:
        patched_main_map.data[1]['x'] = None
        patched_main_map.data[1]['y'] = None
    if hasattr(database, "idxBinLong") == True:
        patched_main_map.data[2]['x'] = [database.table.X[database.idxBinLong]]
        patched_main_map.data[2]['y'] = [database.table.Y[database.idxBinLong]]
    else:
        patched_main_map.data[2]['x'] = None
        patched_main_map.data[2]['y'] = None
    return patched_main_map


def update_dashboard(database, patched_main_map):
    '''
    Function to update all the figures after selecting a VorBin
    :param database:
    :return:
    '''
    print("Function call update_dashboard")
    if hasattr(database, "idxBinLong") == True and hasattr(database, "idxBinShort") == True:
        if database.idxBinShort < 0:
                return \
                    update_main_map_selectedbin(database, patched_main_map), \
                    None, \
                    None
    return \
        update_main_map_selectedbin(database, patched_main_map), \
        [ dcc.Graph(figure=x, style={"height": "35vh"}) for x in plotSpectra(database) ], \
        [ dcc.Graph(figure=plotSFH(database), style={"height": "35vh"} ) ] + [ dcc.Graph( figure=x, style={"height": "35vh"} ) for x in plotMDF(database) ]


def show_config(database):
    return [dag.AgGrid(
                id="config_table",
                rowData=database.CONFIG_df.to_dict("records"),
                columnDefs=[{"field": "Module", "width": "10"}, {"field": "Configs", "width": "10"}, {"field": "Values", "width": "80"}],
                columnSize="sizeToFit",
                columnSizeOptions={
                    "defaultMinWidth": 120,
                },
                defaultColDef={"resizable": True},
                className="ag-theme-balham",
                style={"height": "55vh"}
            )]

# App layout
app.layout = dmc.Container([
    dmc.Title("MapViewer-Web: Visualizing galaxy properties from the GIST pipeline products", color="blue", size="h3"),
    dmc.Grid(
        children=[
            dmc.Col(
                children=[
                    dmc.Group(
                        children=[
                            dmc.TextInput(
                                style={"width": "35vw", "marginTop": 12, "marginBottom": 12},
                                placeholder="please input your GIST directory path",
                                id="data-directory-ptah",
                            ),
                            dmc.Button(
                                id="load-data",
                                children="Load Database",
                                leftIcon=DashIconify(icon="fluent:database-plug-connected-20-filled"),
                                style={"width": "10vw", "marginTop": 12, "marginBottom": 12}
                            ),
                        ],
                    ),
                ],
                span=6
            ),
            dmc.Col(
                children=[
                    dmc.Group(
                        children=[
                            dmc.SegmentedControl(
                                id="module-select",
                                data = [{"value": "tem", "label": "Wait for data to be loaded"}],
                                style={"width": "20vw", "marginTop": 12, "marginBottom": 12},
                            ),
                            dmc.Select(
                                id="parameter-select",
                                style={"width": '12vw', "marginTop": 12, "marginBottom": 12},
                                maxDropdownHeight=500,
                            ),
                            dmc.ActionIcon(
                                DashIconify(icon="ph:info-fill"),
                                id="config-demo-button",
                                color="blue",
                                variant="filled",
                                size="lg",
                                style={"marginTop": 12, "marginBottom": 12}
                            ),
                            dmc.Modal(
                                title="Master-Configuration",
                                size="70%",
                                id="config-show",
                                zIndex=10000,
                            ),
                        ],
                        align="inherit",
                        id="property-selections",
                        # position="apart",
                    ),
                ],
                span=6,
                )
        ],
    ),
    dmc.Grid(
        children=[
            dmc.Col(
                id="child-main-map",
                children=[dcc.Graph(id="main-map")],
                span=6,
            ),
            dmc.Col(
                id="child-main-table",
                children=[dag.AgGrid(
                    id="main-table",
                    # columnSize="sizeToFit",
                    # columnSizeOptions={
                    #     "defaultMinWidth": 120,
                    # },
                    # defaultColDef={"resizable": True, "sortable": True},
                    # rowModelType="infinite",
                    # className="ag-theme-balham",
                )
                ],
                span=6,
            ),
        ],
        justify="center",
        align="stretch",
        gutter="sm",
        id="children-main-info",
    ),

    dmc.Grid(
        children=[
            dmc.Col(
                id="plot-spec-map",
                span=8,),
            dmc.Col(
                id="plot-mfd-map",
                span=4,),
        ],
        justify="space-around",
        align="flex-start",
        gutter="md",
        id="spec-inspect",
    ),

], fluid=True)


@callback(
    Output("property-selections", "children"),
    Output("children-main-info", "children"),
    Output("spec-inspect", "children"),
    Input("load-data", "n_clicks"),
    State("data-directory-ptah", "value"),
    prevent_initial_call=True
)
def call_load_selects(n_clicks, path_gist_run):
    '''
    Update the figures after selecting a new galaxy property
    :param n_clicks:
    :param path_gist_run:
    :return:
    '''
    print("----------------------------------")
    print("Interactivity call load_selects")
    database.reset()
    database.loadData(path_gist_run)
    return create_property_groups(database), \
        [
            dmc.Col(
                id="child-main-map",
                children=[
                    dcc.Graph(
                        id="main-map",
                        style={"height": "55vh"},
                    )
                ],
                span=6,
            ),
            dmc.Col(
                id="child-main-table",
                children=[dag.AgGrid(id="main-table")],
                span=6,
            ),
        ], \
        [
            dmc.Col(
                id="plot-spec-map",
                span=8,),
            dmc.Col(
                id="plot-mfd-map",
                span=4,),
        ]


@callback(
    Output("child-main-table", "children"),
    Output("parameter-select", "data"),
    Output("parameter-select", "value"),
    Input("module-select", "value"),
    prevent_initial_call=True
)
def call_select_module(value):
    '''
    Callback when clicking a galaxy property module
    :param value:
    :return:
    '''
    print("Interactivity call select_module")
    names = getattr(database, value).names
    database.module = module_names[module_table_names.index(value)]
    return [create_main_table(database, value)], [{"value": parameter_i, "label": parameter_i} for parameter_i in names], names[0]


@callback(
    Output("child-main-map", "children"),
    Input("parameter-select", "value"),
    prevent_initial_call=True
)
def call_select_parameter(value):
    '''
    Callback when clicking a galaxy property parameter
    :param value:
    :return:
    '''
    print("Interactivity call select_parameter")
    if value == None:
        raise PreventUpdate
    database.maptype = value
    return [create_main_map(database)]



# @callback(
#     Output("main-table", "getRowsResponse"),
#     Input("main-table", "getRowsRequest"),
# )
# def infinite_scroll(request):
#     print('infinite_scroll')
#     print(request)
#     # print(database.current_df)
#     try:
#         type(database.current_df)
#     except:
#         return no_update
#     if request == None:
#         request = dict()
#         request["startRow"] = 0
#         request["endRow"] = 100
#         # return no_update
#     partial = database.current_df.iloc[request["startRow"] : request["endRow"]]
#     print(partial)
#     return {"rowData": partial.to_dict("records"), "rowCount": len(database.current_df.index)}
#
# app.clientside_callback(
#     """function (n) {
#         dash_ag_grid.getApi('grid').purgeInfiniteCache()
#         return dash_clientside.no_update
#     }""",
#     Output("module-select", "n_clicks"),
#     Input("module-select", "n_clicks"),
#     prevent_initial_call=True)


@callback(
    Output("main-map", "figure"),
    Output("plot-spec-map", "children"),
    Output("plot-mfd-map", "children"),
    Input("main-map", "clickData"),
    Input("main-table", "cellClicked"),
    prevent_initial_call=True
)
def call_display_click_vorbin(clickData, cellClicked):
    '''
    Callback when clicking a Voronoi Bin on the map or table
    :param clickData:
    :param cellClicked:
    :return:
    '''
    print("Interactivity call display_click_vorbin")
    triggered_id = ctx.triggered_id
    patched_main_map = Patch()

    if triggered_id == "main-map":
        if clickData == None:
            raise PreventUpdate
        else:
            remove_idxBin(database)
            database.idxBinLong, database.idxBinShort = getVoronoiBin(database, clickData["points"][0]["x"], clickData["points"][0]["y"])
            return update_dashboard(database, patched_main_map)
    elif triggered_id == "main-table":
        if cellClicked == None:
            raise PreventUpdate
        else:
            remove_idxBin(database)
            if database.module in ['TABLE', 'MASK']:
                database.idxBinLong = int(cellClicked["rowId"])
                database.idxBinShort = database.table['BIN_ID'][database.idxBinLong]
            else:
                database.idxBinShort = int(cellClicked["rowId"])
            return update_dashboard(database, patched_main_map)


@callback(
    Output("config-show", "opened"),
    Output("config-show", 'children'),
    Input("config-demo-button", "n_clicks"),
    State("config-show", "opened"),
    prevent_initial_call=True,
)
def call_show_config(nc, opened):
    return [not opened, show_config(database)]



# Run the App
# if __name__ == "__main__":
#     app.run(debug=False, host="0.0.0.0", port=5801)
