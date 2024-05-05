import streamlit as st
import pandas as pd
import plotly.graph_objects as go


CSV_PATH = 'https://raw.githubusercontent.com/afifather/ws/main/output.csv'


def enhanced_interactive_plot(df):
    initial_column = df.columns[1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df[initial_column], mode='lines+markers', name=initial_column))
    fig.update_layout(
        title='Factor Returns',
        xaxis_title='Date',
        yaxis_title='Value',
        template='plotly_white',
        hovermode='x unified',
        xaxis=dict(
            showline=True, showgrid=True, showticklabels=True,
            linecolor='rgb(204, 204, 204)', linewidth=2, ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)'),
        ),
        yaxis=dict(
            showgrid=True, zeroline=False, showline=False, showticklabels=True,
        ),
        autosize=True,
        margin=dict(autoexpand=True, l=100, r=20, t=110),
        showlegend=True
    )
    buttons = []
    for col in df.columns[1:]:
        buttons.append(dict(method='update',
                            label=col,
                            args=[{'y': [df[col]], 'x': [df['Date']]},
                                  {'yaxis': {'title': col}}]))
    fig.update_layout(
        updatemenus=[{
            'buttons': buttons,
            'direction': 'down',
            'pad': {'r': 10, 't': 10},
            'showactive': True,
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }]
    )
    st.plotly_chart(fig)


st.title("Factor Returns")


try:
    data = pd.read_csv(CSV_PATH)
    data['Date'] = pd.to_datetime(data['Date'])
    enhanced_interactive_plot(data)
except FileNotFoundError:
    st.error(f"File not found at the specified path: {CSV_PATH}")
