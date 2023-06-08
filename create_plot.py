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
fig.show()

# import plotly 
# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')})

# plotly.offline.plot({'data': px.scatter(df_2.reset_index(), x='date retrieved', y='num listings')}, include_plotlyjs=False, output_type='div')

