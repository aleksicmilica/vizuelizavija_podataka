from dash import Dash, html, dash_table, dcc, callback, Output, Input,State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import layout

from  data_management import DataClass
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')



external_stylesheets = [dbc.themes.MINTY]


data_obj = DataClass("netflix_titles.csv","country_continet.csv")
#radio_button_type_cat
@callback([Output("tab_content", "children"),
           Output("slider_actors", 'value'),
           Output("dropdown_region_actors", 'value'),
           Output('dropdown_region', 'value'), 
           Output('radio_button_type', 'value'),
           Output('radio_button_type_cat', 'value'),
           Output('group-sel-cat', 'value')], 
          [Input("tabs", "active_tab")])
def render_tab_content(active_tab):
    value_list=['International', 'Dramas', 'Comedies', 'Action', 'Documentaries',
                                          'Romantic', 'Thrillers']
    if active_tab is not None:
        if active_tab == "tab_general":
            return (dcc.Markdown(),5,"World","World","Movie","Movie",value_list)
        elif active_tab == "tab_actors":
            return (dcc.Markdown(),5,"World","World","Movie","Movie",value_list)
        elif active_tab == "tab_maps":
            return  (dcc.Markdown(),5,"World","World","Movie","Movie",value_list)
        elif active_tab == "tab_content_type":
            return  (dcc.Markdown(),5,"World","World","Movie","Movie",value_list)
        elif active_tab == "tab_content_cat":
            return  (dcc.Markdown(),5,"World","World","Movie","Movie",value_list)
        
        else:
            return "no tab selected"


@callback(
    Output('choropleth-map', 'figure'),
    [Input('dropdown_region', 'value')]  
)
def update_map(selected_region):
    
    data = data_obj.get_number_per_country(selected_region)
    if data.empty:
        fig = px.choropleth(data_frame=data,locations="country",locationmode='country names',color_continuous_scale='blues',projection='natural earth')
    else:    
        fig = px.choropleth(data_frame=data,locations="country",locationmode='country names',color="count",hover_name='country',scope=selected_region.lower(),color_continuous_scale='darkmint',projection='natural earth')
    
    return fig

@callback(
    Output('hist_actors','figure'),
    [Input('dropdown_region_actors','value'),Input('slider_actors','value')]

)
def update_histogram_actors(region,num):
    data = data_obj.get_number_per_actors(region)
    # print(data)
    data = data[:num]
    fig = px.histogram(data, x="cast", y='count', color_discrete_sequence=["rgb(37,161,142)"])
    fig.update_layout(
        xaxis =dict(
            title = 'Actor',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ), 
            yaxis =dict(
            title = 'Count',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ),
        font=dict(
            size=16  
        ),
        legend=dict(font=dict(size=16)))
    
    fig.update_traces(
        customdata=data[['country']].values,
        hovertemplate='<b>Actor</b>: %{x}<br><b>Count</b>: %{y}<br><b>Country</b>: %{customdata[0]}'
    )

    return fig

@callback(
    Output('line-graph-type','figure'),
    Input('radio_button_type','value')
)
def update_line_chart_types(type_value):
    data = data_obj.get_data_type_per_year()
    average_data = data.groupby(['type',"release_year"])["num_duration"].mean().reset_index()
    average_data.rename(columns={'num_duration': 'average_duration'}, inplace=True)
    average_data = average_data[average_data["type"]==type_value]
    fig = px.line(average_data, x="release_year", y='average_duration',color_discrete_sequence=["rgb(37,161,142)"])
    if type_value=="Movie":
        fig.update_layout(xaxis =dict(
            title = 'Year',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ), 
            yaxis =dict(
            title = 'Minutes',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ),
        font=dict(
            size=16  
        ),)
    else:
        fig.update_layout(xaxis =dict(
            title = 'Year',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ), 
            yaxis =dict(
            title = 'Seasons',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ),
        font=dict(
            size=16  
        ),)

    return fig

@callback(
    Output('stream-graph-cat', 'figure'),
    [Input('radio_button_type_cat','value'),Input('group-sel-cat', 'value')]
)
def update_streamgraph(type,selected_categories):
    data = data_obj.get_per_type_cat(type=type,cat=selected_categories
                                     )
    # print(selected_categories)
    # print(data)
    # if data.empty:
    #     return px.area()
    # fig = px.area(data, x='release_year', y='counts', color='category', line_group='category', 
    #               labels={'release_year': 'Year', 'counts': 'Value', 'category': 'Category'},
    #               )
    # fig.update_traces(mode='lines')
    if data.empty:
        return px.bar()  
    fig = px.bar(data, x='release_year', y='counts', color='category', labels={'release_year': 'Year', 'counts': 'Value', 'category': 'Category'}, 
                 barmode='stack',  # Set barmode to 'stack' for a stacked bar chart
                )
    fig.update_layout(
        font=dict(
            size=16  
        ),
        xaxis =dict(
            title = 'Year',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ), 
            yaxis =dict(
            title = 'Value',    
            titlefont=dict(size=16),  
            tickfont=dict(size=16)    
        ),

        legend=dict(font=dict(size=16))
    )
    return fig

@callback(
    [Output('hist_cat_movie','figure'),Output('hist_cat_show','figure')],
    Input('slider_cat','value')

)
def update_charts_cat(value):
    data_1,data_2 = data_obj.get_most_popular_genre()
    
    data_1 =data_1.head(value)
    data_2 =data_2.head(value)
    

    fig_1 = px.histogram(data_frame=data_1, y='listed_in', x='counts', orientation='h', labels={'listed_in':'Genre','counts':'Count'}, color_discrete_sequence=["rgb(37,161,142)"])
    fig_1.update_layout(
        xaxis =dict(
        title = 'Genre',    
        titlefont=dict(size=16),  
        tickfont=dict(size=16)    
    ), 
        yaxis =dict(
        title = 'Count',    
        titlefont=dict(size=16),  
        tickfont=dict(size=16)    
    ),legend=dict(font=dict(size=16))
    ) 
    fig_1.update_traces(hovertemplate='<b>Genre</b>: %{y}<br><b>Count</b>: %{x}')
    fig_2 = px.histogram(data_frame=data_2, y='listed_in', x='counts', orientation='h', labels={'listed_in':'Genre','counts':'Count'}, color_discrete_sequence=["rgb(37,161,142)"])
    fig_2.update_layout(
        xaxis =dict(
        title = 'Genre',    
        titlefont=dict(size=16),  
        tickfont=dict(size=16)    
    ), 
        yaxis =dict(
        title = 'Count',    
        titlefont=dict(size=16),  
        tickfont=dict(size=16)    
    )

    )
    fig_2.update_traces(hovertemplate='<b>Genre</b>: %{y}<br><b>Count</b>: %{x}')
    return [fig_1,fig_2]



@callback(Output('selected-edge-info', 'children'),
          [Input('network_graph', 'tapEdgeData')])
def display_selected_edge_info(tap_edge_data):
    # print("Tap Edge Data:", tap_edge_data)
    if tap_edge_data:
        source = tap_edge_data['source']
        target = tap_edge_data['target']
        label = tap_edge_data['label']
        return f"{source} starred in : {label}, directed by {target}"
    return ""

@callback(Output('selected-node-info', 'children'),
          [Input('network_graph', 'tapNodeData')])
def display_selected_node_info(tap_node_data):
    # print("Tap Edge Data:", tap_edge_data)
    if tap_node_data:
        
        additional_label = tap_node_data["additional_label"][0]
        classes = tap_node_data["type"]
        label = tap_node_data['label']
        if classes=="actor":
            return f"{label} starred in : {additional_label}"
        else:
            return f"{label} directred : {additional_label}"
    return ""





if __name__ == "__main__":
    
    # data = data_obj.test()
    # print(data)
    app = Dash(external_stylesheets=external_stylesheets)
    app.layout = layout.create_layout(data_obj)
    

    app.run(debug=True)
