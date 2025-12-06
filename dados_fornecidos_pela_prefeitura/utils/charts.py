
import plotly.express as px
import pandas as pd

def plot_evolution_by_year(df):
    """
    Plots the total 'valor_repasse' per year.
    """
    if df.empty:
        return None
    
    yearly_sum = df.groupby('ano')['valor_repasse'].sum().reset_index()
    fig = px.line(yearly_sum, x='ano', y='valor_repasse', 
                  title='Evolução do Valor de Repasse por Ano',
                  markers=True)
    fig.update_layout(xaxis_title='Ano', yaxis_title='Total Repassado (R$)')
    return fig

def plot_top_beneficiaries(df, top_n=10):
    """
    Plots the top N beneficiaries by total 'valor_repasse'.
    """
    if df.empty:
        return None

    top_oscs = df.groupby('beneficiaria_nome')['valor_repasse'].sum().reset_index()
    top_oscs = top_oscs.sort_values('valor_repasse', ascending=False).head(top_n)
    
    fig = px.bar(top_oscs, x='valor_repasse', y='beneficiaria_nome', 
                 orientation='h',
                 title=f'Top {top_n} OSCs por Valor Recebido')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, 
                      xaxis_title='Total Recebido (R$)', yaxis_title='OSC')
    return fig

def plot_by_secretariat(df):
    """
    Plots the distribution of 'valor_repasse' by secretariat.
    """
    if df.empty:
        return None

    sec_sum = df.groupby('secretaria_sigla')['valor_repasse'].sum().reset_index()
    
    fig = px.pie(sec_sum, values='valor_repasse', names='secretaria_sigla', 
                 title='Distribuição de Recursos por Secretaria')
    return fig
