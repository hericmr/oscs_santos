import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

def apply_academic_chart_style(fig):
    """
    Apply strict academic styling to Plotly figures.
    """
    fig.update_layout(
        template="plotly_white",
        font=dict(
            family="Times New Roman",
            size=14,
            color="black"
        ),
        title_font=dict(
            family="Times New Roman",
            size=18,
            color="black",
            weight="bold"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            showline=True,
            linewidth=2,
            linecolor='black',
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            tickfont=dict(color='black')
        ),
        legend=dict(
            font=dict(color="black"),
            bgcolor="rgba(0,0,0,0)"
        )
    )
    return fig

def plot_bar_chart(df, x_col, y_col=None, title="", color_col=None, orientation='v'):
    """
    Gera gráfico de barras (contagem ou valor).
    """
    if y_col is None:
        data = df[x_col].value_counts().reset_index()
        data.columns = [x_col, 'Quantidade']
        y_col = 'Quantidade'
        fig = px.bar(data, x=x_col, y=y_col, title=title, color=color_col if color_col else x_col, orientation=orientation)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title, color=color_col, orientation=orientation)
    
    return apply_academic_chart_style(fig)

def plot_pie_chart(df, col, title=""):
    """
    Gera gráfico de pizza.
    """
    data = df[col].value_counts().reset_index()
    data.columns = [col, 'Quantidade']
    fig = px.pie(data, names=col, values='Quantidade', title=title)
    
    # Pie charts handle styling a bit differently for traces
    fig.update_traces(textfont_size=14, textfont_color="black")
    return apply_academic_chart_style(fig)

def plot_time_series(df, date_col, title="", cumulative=False):
    """
    Gera gráfico de linha temporal.
    """
    data = df[date_col].value_counts().sort_index().reset_index()
    data.columns = ['Ano', 'Quantidade']
    if cumulative:
        data['Quantidade'] = data['Quantidade'].cumsum()
        title = f"{title} (Acumulado)"
    fig = px.line(data, x='Ano', y='Quantidade', title=title, markers=True)
    
    return apply_academic_chart_style(fig)

def plot_map(df, lat_col='latitude', lon_col='longitude', tooltip_cols=None, hover_name_col='tx_razao_social_osc'):
    """
    Gera mapa Folium com pontos individuais (sem clusterização).
    tooltip_cols pode ser uma lista de colunas ou um dict {coluna: label}.
    """
    # Filtrar dados com coordenadas válidas
    df_map = df.dropna(subset=[lat_col, lon_col])
    
    if df_map.empty:
        return None

    center_lat = df_map[lat_col].mean()
    center_lon = df_map[lon_col].mean()
    
    # Use a cleaner tile if possible, or default
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="CartoDB positron") 
    color = '#3186cc' 

    for idx, row in df_map.iterrows():
        # Determine color
        # 3301 = Organização Social (OS) -> Red
        is_os = row.get('cd_natureza_juridica_osc') == 3301
        marker_color = '#d62728' if is_os else '#3186cc'

        # Construir conteúdo do Popup
        popup_html = "<div style='font-family:Times New Roman; color:black; font-size:12px;'>"
        popup_html += f"<b>{row.get('tx_nome_fantasia_osc', 'OSC')}</b><br><br>"
        
        if tooltip_cols:
            iterable = tooltip_cols.items() if isinstance(tooltip_cols, dict) else [(c, c) for c in tooltip_cols]
            
            for col, label in iterable:
                if col in df.columns:
                    val = row[col]
                    # Formatar se for data (e.g. timestamp)
                    if isinstance(val, pd.Timestamp):
                        val = val.strftime('%d/%m/%Y')
                    
                    popup_html += f"<b>{label}:</b> {val}<br>"
        
        popup_html += "</div>"
        
        hover_text = str(row.get(hover_name_col, 'Sem Nome'))
        
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=6 if is_os else 5, # Slightly larger for importance? Or same. Let's make it consistent.
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=hover_text,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7
        ).add_to(m)
        
    return m

def plot_heatmap(df, x_col, y_col, title=""):
    """
    Heatmap de contagem.
    """
    data = df.groupby([x_col, y_col]).size().reset_index(name='Contagem')
    fig = px.density_heatmap(data, x=x_col, y=y_col, z='Contagem', title=title, text_auto=True)
    return apply_academic_chart_style(fig)
