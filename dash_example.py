# pip install dash
from dash import Dash, dcc, html, Input, Output

################
from typing import Final, List

import pandas as pd
import plotly.io as pio
# pio.renderers.default = 'iframe'



def read_dataframe():
    """
    TODO: Save this df in RAM somewhere so we don't re-read it every time??
    """
    DATAFILE: Final[str] = "seatgeek_data.txt"

    # Read the csv file 
    df = pd.read_csv(DATAFILE, delimiter="|")
    df.columns = df.columns.str.strip()   # Remove leading and trailing spaces from columns
    # df[df['id'] == 5958769][['date retrieved', 'num listings', 'lowest price']]

    # Remove trailing and leading spaces from all strings in the dataframe
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Some entries have "None" returned from SeatGeek, replace them with -1
    df.replace("None", "-1", inplace=True)

    # Convert some columns from object (string) to float
    for col in ['num listings', 'lowest price', 'median price']:
        df[col] = pd.to_numeric(df[col])

    # Convert string to datetime object
    # TODO: Keep this in UTC and display it in the user's local timezone
    df['date retrieved MT'] = pd.to_datetime(df['date retrieved'], utc=True).dt.tz_convert('America/Denver')

    df.set_index('date retrieved MT', inplace=True)
    return df


# fig.show()

# import plotly 
# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')})

# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')}, include_plotlyjs=False, output_type='div')
###################

df = read_dataframe()
options = []
for id_num in df.id.unique():
    row = df[df.id == id_num].iloc[0]
    label = row.title
    value = row.id
    search_str = row.type + '; '
    search_str += row['event datetime'] + '; '
    search_str += row.title + '; '
    search_str += row['performer names']
    options.append({'label': label, 'value': value, 'search': search_str})
print(f"Example option:\n{options[0]}")

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
                # "label": "value"
                # label shown in drop down: actual value when selected
        # options=[{'label': 'Quinn Concert Red Rocks', 
        #           'value': 'Quinn',
        #           'search': 'Quinn XCII Concert Red Rocks'},
        #          {'label': 'The Concert Red Rocks', 
        #           'value': 'The ',
        #           'search': 'nothing'},
        #          {'label': 'Denver Nuggets Ball Arena', 
        #           'value': 'Denver Nuggets',
        #           'search': 'Denver Nuggets Ball Arena 2022-06-21 19:27:53.74452'}],
        options=options,
        # df.title.unique()
        # value=['Montreal', 'San Francisco'],
        multi=True,
        id='demo-dropdown',
        searchable=True,
        placeholder="Select an event"
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(id='ticket-price-graph')
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


@app.callback(
    Output('ticket-price-graph', 'figure'),
    Input('demo-dropdown', 'value'),
)
def update_graph(event_id: List[int]):
    print(f"running update_graph with event_id: {event_id}")
    if event_id is None or len(event_id) == 0:
        return {}
    
    df = read_dataframe()
    df_2 = df[df['id'].isin(event_id)]
    import plotly.express as px
    fig = px.line(data_frame=df_2.reset_index(),
                    x='date retrieved MT',
                    # TOOD: Get these y values from a check box
                    y=['num listings', 'lowest price', 'median price'],
                    title=df_2.iloc[0].title)
    return fig




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)


# Self hosting: 
# https://community.plotly.com/t/deploying-dash-app-as-self-hosted/8728/3
# https://dash.plotly.com/deployment
# Or maybe we can use iframes
# https://dash.plotly.com/integrating-dash
