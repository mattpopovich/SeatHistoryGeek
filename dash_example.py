# pip install dash
from dash import Dash, dcc, html, Input, Output

################
from typing import Final

import pandas as pd
import plotly.io as pio
# pio.renderers.default = 'iframe'

DATAFILE: Final[str] = "seatgeek_data.txt"

# Read the csv file 
df = pd.read_csv(DATAFILE)
df.columns = df.columns.str.strip()   # Remove leading and trailing spaces from columns
# df[df['id'] == 5958769][['date retrieved', 'num listings', 'lowest price']]

# Convert string to datetime object
df['date retrieved'] = pd.to_datetime(df['date retrieved'])

df.set_index('date retrieved', inplace=True)
df_2 = df[df['id'] == 5958641]
import plotly.express as px
fig = px.line(data_frame=df_2.reset_index(),
                 x='date retrieved',
                 y=['num listings', 'lowest price', 'median price'],
                 title=df_2.iloc[0].title)
# fig.show()

# import plotly 
# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')})

# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')}, include_plotlyjs=False, output_type='div')
###################

options = []
for id in df.id.unique():
    row = df[df.id == id].iloc[0]
    label = row.title
    value = row.id
    search_str = row.type + '; '
    search_str += row['event datetime'] + '; '
    search_str += row.title + '; '
    search_str += row['performer names']
    options.append({'label': label, 'value': value, 'search': search_str})
print(f"Options:\n{options}")

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
    dcc.Graph(figure=fig)
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)


# Self hosting: 
# https://community.plotly.com/t/deploying-dash-app-as-self-hosted/8728/3
# https://dash.plotly.com/deployment
# Or maybe we can use iframes
# https://dash.plotly.com/integrating-dash
