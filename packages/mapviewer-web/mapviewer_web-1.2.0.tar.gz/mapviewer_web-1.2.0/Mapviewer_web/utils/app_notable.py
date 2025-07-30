from Mapviewer_web.utils.loadData import gistDataBase
from Mapviewer_web.utils.plotData import *
from Mapviewer_web.utils.helperFunctions import *

from dash_iconify import DashIconify
from dash import Dash, dcc, callback, Output, Input, ctx, State, no_update, Patch, clientside_callback
import dash_mantine_components as dmc
import dash_ag_grid as dag
from dash.exceptions import PreventUpdate
import dash_auth
import time

import warnings
warnings.filterwarnings("ignore")


# Incorporate data
module_names = ["TABLE", "MASK", "KIN", "GAS", "SFH", "LS"]
module_table_names = ["table", "Mask", "kinResults", "gasResults", "sfhResults", "lsResults"]
global settings, settings_cache, database
settings = {
    "restrict2voronoi": 2,
    "gasLevelSelected": "BIN",
    "LsLevelSelected": "ADAPTED",
    "AoNThreshold": 3,
}
settings_cache = {}
database = gistDataBase(settings)

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
            database.maptype = "V"
            database.current_df = database.kinResults_Vorbin_df
        else:
            database.module = "TABLE"
            database.maptype = "FLUX"
            database.current_df = database.table_df
    return [
            dmc.SegmentedControl(
                    id="module-select",
                    value=module_table_names[module_names.index(database.module)],
                    # value=None,
                    data=[{"value": "table", "label": "TABLE"}] +
                         [{"value": module_table_names[i], "label": module_names[i]}
                          for i in range(1, len(module_names)) if getattr(database, module_names[i])],
                    style={"width": "22vw", "marginTop": 12, "marginBottom": 12},
                ),
            dmc.Select(
                placeholder="choose a parameter",
                id="parameter-select",
                value=database.maptype,
                data=[{"value": parameter_i, "label": parameter_i}
                      for parameter_i in getattr(database, module_table_names[module_names.index(database.module)]).names],
                style={"width": '8vw', "marginTop": 12, "marginBottom": 12},
                maxDropdownHeight=500,
            ),
        ]



def create_main_map(database):
    '''
    Function to create main property distribution map
    :param database:
    :return:
    '''
    print("Function call create_main_map")
    if hasattr(database, "maptype") == False:
        return \
            dcc.Graph(
                id="main-map",
                style={"height": "60vh"},
            )
    else:
        return \
            dcc.Graph(
                id="main-map",
                figure=plotMap(database, database.module, database.maptype),
                style={"height": "60vh"},
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
        [ dcc.Graph(figure=x, style={"height": "20vh"}) for x in plotSpectra(database) ], \
        [ dmc.Col(dcc.Graph(figure=plotSFH(database), style={"height": "30vh"} ), span=4) ] + [ dmc.Col(dcc.Graph(figure=x, style={"height": "30vh"}), span=4) for x in plotMDF(database) ]


def show_config(database):
    return \
        [
            dag.AgGrid(
                id="config_table",
                rowData=database.CONFIG_df.to_dict("records"),
                columnDefs=[{"field": "Module", "width": "10"}, {"field": "Configs", "width": "10"}, {"field": "Values", "width": "80"}],
                columnSize="sizeToFit",
                columnSizeOptions={
                    "defaultMinWidth": 120,
                },
                defaultColDef={"resizable": True},
                className="ag-theme-balham",
                style={"height": "60vh"}
            )
        ]


def show_table(database):
    print("Function call create_main_table")
    # print(database.current_df)
    return  \
        [
            dag.AgGrid(
                id="main-table",
                rowData=database.current_df.to_dict("records"),
                # rowData=None,
                columnDefs=[{"field": i} for i in database.current_df.columns],
                columnSize="sizeToFit",
                columnSizeOptions={
                    "defaultMinWidth": 120,
                },
                defaultColDef={"resizable": True, "sortable": True},
                className="ag-theme-balham",
                dashGridOptions={
                   "rowBuffer": 0,
                   "maxBlocksInCache": 1,
                   "infiniteInitialRowCount": 20,
                   "rowSelection":"single",
                },
                style={"height": "60vh"},
            )
        ]

def show_settings(settings):
    components_list = []
    components_list.append(
        dmc.Space(h=10),
    )
    components_list.append(
        dmc.CheckboxGroup(
            id="checkbox-group-vorbin",
            label="General settings:",
            orientation="vertical",
            offset="md",
            mb=6,
            children=[
                dmc.Checkbox(
                    label="Restrict to Voronoi region",
                    value="2",
                ),
            ],
            value=[str(settings['restrict2voronoi'])],
        )
    )
    components_list.append(
        dmc.Space(h=10),
    )
    components_list.append(
        dmc.RadioGroup(
            id="radiogroup-emission",
            label="Display emissionLines results on bin or spaxel level?",
            orientation="vertical",
            offset="md",
            mb=6,
            children=[
                dmc.Radio("Bin level", value='BIN'),
                dmc.Radio("Spaxel level", value='SPAXEL'),
            ],
            value=settings['gasLevelSelected']
        )
    )
    components_list.append(
        dmc.Space(h=10),
    )
    components_list.append(
        dmc.RadioGroup(
            id="radiogroup-ls",
            label="Display LS results measured on adapted or original resolution?",
            orientation="vertical",
            offset="md",
            mb=6,
            children=[
                dmc.Radio("Original resolution", value='ORIGINAL'),
                dmc.Radio("Adapted resolution", value='ADAPTED'),
            ],
            value=settings['LsLevelSelected'],
        )
    )
    components_list.append(
        dmc.Space(h=10),
    )
    components_list.append(
        dmc.TextInput(
            id='aoninput',
            label="AoN Threshold for displayed line detections:",
            style={"width": "100%"},
            value=str(settings['AoNThreshold'])
        ),
    )
    components_list.append(
        dmc.Space(h=30),
    )
    components_list.append(
        dmc.Group(
            [
                dmc.Button("Submit", id="settings-submit-button"),
                dmc.Button(
                    "Close",
                    color="red",
                    variant="outline",
                    id="settings-close-button",
                ),
            ],
            position="right",
        ),
    )
    return components_list

# App layout
app.layout = dmc.Container([
    dmc.Title(
        "MapViewer-Web: Visualizing galaxy properties from the GIST pipeline products",
        color="blue",
        size="h3",
        id="title"
    ),
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
                                style={"width": "11vw", "marginTop": 12, "marginBottom": 12}
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
                                style={"width": "22vw", "marginTop": 12, "marginBottom": 12},
                            ),
                            dmc.Select(
                                id="parameter-select",
                                style={"width": '8vw', "marginTop": 12, "marginBottom": 12},
                                maxDropdownHeight=500,
                            ),
                        ],
                        align="left",
                        id="property-selections",
                        # position="apart",
                    ),
                ],
                span=4,
            ),
            dmc.Col(
                children=[
                    dmc.Group(
                        children=[
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
                            dmc.ActionIcon(
                                DashIconify(icon="ph:table-fill"),
                                id="table-demo-button",
                                color="blue",
                                variant="filled",
                                size="lg",
                                style={"marginTop": 12, "marginBottom": 12}
                            ),
                            dmc.Modal(
                                title="Parameter-Table",
                                size="70%",
                                id="table-show",
                                zIndex=10000,
                            ),
                            dmc.ActionIcon(
                                DashIconify(icon="uiw:setting"),
                                id="settings-demo-button",
                                color="blue",
                                variant="filled",
                                size="lg",
                                style={"marginTop": 12, "marginBottom": 12}
                            ),
                            dmc.Modal(
                                title="Settings",
                                size="30%",
                                id="settings-show",
                                zIndex=10000,
                                children=show_settings(settings),
                            ),
                        ],
                        position="right",
                        spacing="xs",
                        id="demo-buttons",
                        # position="apart",
                    ),
                ],
                span=2,
            )
        ],
    ),
    dmc.Grid(
        children=[
            dmc.Col(
                id="child-main-map",
                children=[dcc.Graph(id="main-map")],
                span=5,
            ),
            dmc.Col(
                id="plot-spec-map",
                span=7,
            ),
        ],
        justify="center",
        align="stretch",
        gutter="sm",
        id="main-map-spec",
    ),
    dmc.Grid(
        children=[
            dmc.Col(
                id="plot-sfh-map",
                span=4,),
            dmc.Col(
                id="plot-mfd-map1",
                span=4,),
            dmc.Col(
                id="plot-mfd-map2",
                span=4,),
        ],
        justify="flex-start",
        align="flex-start",
        gutter="md",
        id="plot-sfh-mfd-map",
    ),

], fluid=True)


@callback(
    Output("property-selections", "children"),
    Output("main-map-spec", "children"),
    Output("plot-sfh-mfd-map", "children", allow_duplicate=True),
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
    database.reset(settings)
    database.loadData(path_gist_run)
    if database.gasLevel_onlyBIN == True:
        settings['gasLevelSelected'] = "BIN"
    if database.LsLevel_onlyORIGINAL == True:
        settings['LsLevelSelected'] = "ORIGINAL"

    return \
        create_property_groups(database), \
        [
            dmc.Col(
                id="child-main-map",
                children=[create_main_map(database)],
                span=5,
            ),
            dmc.Col(
                id="plot-spec-map",
                span=7,
            ),
        ], \
        [
            dmc.Col(
                id="plot-sfh-map",
                span=4,),
            dmc.Col(
                id="plot-mfd-map1",
                span=4,),
            dmc.Col(
                id="plot-mfd-map2",
                span=4,),
        ]


@callback(
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
    if value in ["table", "Mask"]:
        database.current_df = getattr(database, value+"_df")
    else:
        database.current_df = getattr(database, value+"_Vorbin_df")
    return [{"value": parameter_i, "label": parameter_i} for parameter_i in names], names[0]


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



@callback(
    Output("main-map", "figure"),
    Output("plot-spec-map", "children"),
    Output("plot-sfh-mfd-map", "children"),
    Input("main-map", "clickData"),
    prevent_initial_call=True
)
def call_display_click_vorbin(clickData):
    '''
    Callback when clicking a Voronoi Bin on the map or table
    :param clickData:
    :param cellClicked:
    :return:
    '''
    print("Interactivity call display_click_vorbin")
    patched_main_map = Patch()
    if clickData == None:
        raise PreventUpdate
    else:
        remove_idxBin(database)
        database.idxBinLong, database.idxBinShort = getVoronoiBin(database, clickData["points"][0]["x"], clickData["points"][0]["y"])
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

@callback(
    Output("table-show", "opened"),
    Output("table-show", 'children'),
    Input("table-demo-button", "n_clicks"),
    State("table-show", "opened"),
    prevent_initial_call=True,
)
def call_show_table(nc, opened):
    return [not opened, show_table(database)]


@callback(
    Output("title", "children"),
    Input("checkbox-group-vorbin", "value"),
    prevent_initial_call=True,
)
def call_checkbox_Vorbin(value):
    if "2" in value:
        settings_cache['restrict2voronoi'] = 2
    else:
        settings_cache['restrict2voronoi'] = None
    # print("Print settings_cache", value, settings_cache)
    raise PreventUpdate


@callback(
    Output("title", "children", allow_duplicate=True),
    Input("radiogroup-emission", "value"),
    prevent_initial_call=True,
)
def call_radiogroup_emission(value):
    settings_cache['gasLevelSelected'] = value
    # print("Print settings_cache", value, settings_cache)
    raise PreventUpdate

@callback(
    Output("title", "children", allow_duplicate=True),
    Input("radiogroup-ls", "value"),
    prevent_initial_call=True,
)
def call_radiogroup_ls(value):
    settings_cache['LsLevelSelected'] = value
    # print("Print settings_cache", value, settings_cache)
    raise PreventUpdate

@callback(
    Output("title", "children", allow_duplicate=True),
    Input("aoninput", "value"),
    prevent_initial_call=True,
)
def call_aoninput(value):
    settings_cache['AoNThreshold'] = int(value)
    # print("Print settings_cache", value, settings_cache)
    raise PreventUpdate

@callback(
    Output("settings-show", "opened"),
    Output("settings-show", 'children'),
    Output("load-data", "n_clicks"),
    Input("settings-demo-button", "n_clicks"),
    Input("settings-close-button", "n_clicks"),
    Input("settings-submit-button", "n_clicks"),
    State("settings-show", "opened"),
    prevent_initial_call=True,
)
def call_show_settings(nc1, nc2, nc3, opened):
    triggered_id = ctx.triggered_id
    # print(triggered_id)
    if triggered_id == "settings-submit-button":
        original_vorbin = settings['restrict2voronoi']
        new_vorbin = settings_cache['restrict2voronoi']
        original_ls = settings['LsLevelSelected']
        new_ls = settings_cache['LsLevelSelected']
        original_emission = settings['gasLevelSelected']
        new_emission = settings_cache['gasLevelSelected']
        print("before", settings)
        for key in settings.keys():
            settings[key] = settings_cache[key]
            settings_cache[key] = None
        print("after", settings)
        if original_vorbin != new_vorbin or original_ls != new_ls or original_emission != new_emission:
            return [not opened, show_settings(settings), 1]
        else:
            return [not opened, show_settings(settings), no_update]
    else:
        return [not opened, show_settings(settings), no_update]


# Run the App
# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5802)
