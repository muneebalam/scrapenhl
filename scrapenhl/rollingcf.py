import dash
import dash_core_components as dcc
import dash_html_components as html
import scrapenhl_globals

app = dash.Dash()

### Get data--dummy for now

### Set options
#### Player (str-->int ID--default Erik Karlsson)
allplayers = scrapenhl_globals.get_preferred_player_names().sort_values(by='Name')
player_select = dcc.Dropdown(
        options=[{'label': pname, 'value': pid} for pname, pid in zip(allplayers.Name, allplayers.ID)],
        value='8474578')

#### Date range (default to last 3 years) (two dates) via https://plot.ly/python/range-slider/
#### Team(s) (list of str--default all)
allteams = scrapenhl_globals.get_team_id_file().sort_values(by='Name')
team_select = dcc.Dropdown(
    options=[{'label': tname, 'value': tid} for tname, tid in zip(allteams.Name, allteams.Abbreviation)],
    value=allteams.Abbreviation.values, multi=True)

#### Roll length (int--default 25)
window_slider = dcc.Slider(min=5, max=80,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(5, 81, 5)},
        value=25)

#### Score adjust (bool--default False)
scoreadjust_button = dcc.RadioItems(
        options=[
            {'label': 'None', 'value': 'None'}, {'label': '@IneffectiveMath', 'value': '@IneffectiveMath'}],
        value='None')

#### Include playoffs (bool--default True)
playoff_button = dcc.RadioItems(
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}], value='Yes')

#### Show missing games through gaps in graph (bool--default True)
gpgaps_button = dcc.RadioItems(
        options=[
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}], value='Yes')
#### Show offseason via gap in graph (bool--default False)

### Calculate, using external method (replace with dummy output)

### Plot this output

### Option to save

app.layout = html.Div([html.Label('Player'), player_select,
    html.Label('Team(s)'), team_select,
    html.Label('Include playoffs?'), playoff_button,
    html.Label('Score-adjustment'), scoreadjust_button,
    html.Label('Window size'), window_slider,
    html.Label('Show missed games?'), gpgaps_button],
                      style={'columnCount': 2})

if __name__ == '__main__':
    app.run_server(debug=True)