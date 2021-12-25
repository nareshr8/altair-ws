from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import altair as alt
from random import randint
import json

from toolz.dicttoolz import valfilter
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

df=pd.read_csv('./hurricanes.csv')
df=df.melt(id_vars=df.columns[:2], var_name='Year')
ordered_months=['May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec']


@app.get("/")
def get_chart():
    selection = alt.selection_multi(fields=['Year'], bind='legend')
    opacity = alt.condition(selection, alt.value(1.0), alt.value(0.1))

    chart=alt.Chart(df).mark_line(point=True).encode(
            x=alt.X('Month:N',sort=ordered_months),
            y='value:N',
            opacity=opacity,
            color=alt.Color('Year',legend=alt.Legend(columns=2, symbolFillColor='blue')),
            tooltip=['Month', 'value', 'Year']).properties(width=1000,height=250).add_selection(selection)
    chart_json = json.loads(chart.to_json())
    return chart_json
