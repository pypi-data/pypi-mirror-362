import pandas as pd
import plotly.express as px

def generate_pie_chart(data, value_col, name_col, title):

    df = pd.DataFrame(data)
    if df.empty:
        return "<p>No data available to display.</p>"

    fig = px.pie(df, values=value_col, names=name_col, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
