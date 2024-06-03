from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from data_management import DataClass
import geopandas as gpd
import cartopy.crs as ccrs
import dash_cytoscape as cyto
import random
import math


custom_styles = {
    'h1': {
           'padding': '2cm', 
           'background-color': '#25a18e',
           'color':'white','width':'100%',
           'box-sizing': 'border-box',
            'margin': '0',
            'padding': '15px'},
    'options':{'color':"black"},
    'dropdown-menu-css':{'background-color':'white', 'color':'black', 'margin':"5px"},
    'slider-actors-css':{'color':'salmon', 'margin':"5px"},
    'dropdown-region-css': {'color': 'white'},  
    'map': {'background-color': 'white','border':'5px'},
    'cell_style':{'font-family':'Arial','text-align':'left'},
    'tabs': {
        'background-color': 'rgb(220, 220, 220)',  
        'margin-bottom': '20px',  
        'width': '100%',
        'fill':'True',
        'font-size':'20px'

    },
    'basic-container': {
        'height':'100%',
        'width':' 100%',
        
    },
    'main-container': {
        'border': '1px solid rgba(255, 255, 255, 0.5)',
        'padding': '20px',
        'margin':'20px auto',
        'width':' 100%',
        'box-shadow':' 0 0 10px rgba(0, 0, 0, 0.1)',
        'background-color': 'rgba(255, 255, 255, 0.8)',
        'border-radius': '10px',
    },
    'body': {
        'margin': '0',
        'padding': '0',
        'fontFamily': 'Arial, sans-serif',
        'height':'100%',
        'background-size':'cover',
        'background-color': '#e9ecef',
        'color':'#FFFFFF'
    },
    "h2":{
        'background-color': '#25a18e','color':'white','font-size':'20px','border-radius': '10px','display': 'block','padding-top': '0.5cm',
    'padding-bottom': '0.5cm',"width":"100%","fill":'True','margin-bottom': '15px',  
    'padding': '0.5cm',  
        
    },
    'response':{
            'padding': '0.5cm', 'background-color': '#ffffff','color':'black','font-size':'16px','border-radius': '10px','box-shadow':' 0 0 10px rgba(0, 0, 0, 0.1)',
    },
    'slider-general':{
        'background-color': 'rgb(220, 220, 220)',
        'padding':'5px',
        'color':'rgb(0,0,0)',
        'font-size':'15px',
        'border-radius': '10px',
    },
    
    'radio-button':{
            'color':'black',
            'font-size':'16px',
            'margin':'5px'
    },
    'check-button':{
            'color':'black',
            'font-size':'16px',
            'margin':'5px',
            'margin-bottom':'30px',
            'margin-left':'20px'
    }
    
}
data_style = [
        {
            'if': {'row_index': 'odd'},  
            'backgroundColor': 'rgb(248, 248, 248)',
            'color':'black'
            
        },
        {
            'if': {'row_index': 'even'},  
            'backgroundColor': 'rgb(220, 220, 220)',
            'color':'black'  
        }
    ]

def create_table(data_obj,type):
    data = data_obj.get_data()
    
    data = data[data['type']==type]
    data = data[['title']]
    return dash_table.DataTable(
        id='table-general-'+type,
        # columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_current=0,
        page_size=10,
        style_cell=custom_styles['cell_style'],
        style_data_conditional=data_style,
        columns=[{
            "name":type,
            "id":"title",
            
        }],
        style_header={
            'backgroundColor': 'rgb(37,161,142)',  # Set background color of header to blue
            'color': 'white',  # Set font color of header to white
            'fontWeight': 'bold',  # Make the header text bold
        },

    )
    

def create_map(data_obj):

    fig = px.choropleth(data_frame=data_obj.get_number_per_country("World"),locations="country",locationmode='country names',color="count",color_continuous_scale='oryel',projection='natural earth')
    fig.update_layout(
        autosize=False,
        width=800,
        height = 600,
        coloraxis_colorbar=dict(
            title = "Count",
            
        ),
        

    )
    return dbc.Container([dbc.Row([
        dbc.Col(
        dcc.Graph(id="choropleth-map",figure = fig, style={'width': '800px', 'height': '600px'}, config={'scrollZoom': False, 'displayModeBar': False},className='map' )
            ,style = custom_styles["map"]),
        dbc.Col(
        dcc.Dropdown(
            id="dropdown_region",
            options = [
                {'label':'Europe','value':'Europe'},
                {'label':'North America','value':'North America'},
                {'label':'South America','value':'South America'},
                {'label':'Asia','value':'Asia'},
                {'label':'Ocenia','value':'Ocenia'},
                {'label':'World','value':'World'}
            ],
            value="World",
            className="dropdowm-region-css",
            style = custom_styles["dropdown-menu-css"]
           
        )),
    ],
    )])

def create_hist_actors():

    return html.Div([dcc.Graph(id="hist_actors")])



def create_tab_maps(data):
    return dbc.Tab(label="Maps",
                    children=dbc.Container([
                        html.H2("Number of content from each country",style=custom_styles['h2']),
                        create_map(data)
                    ],style = custom_styles['main-container']),
                    tab_id="tab_maps")

def create_chart_cat_counts():
    return html.Div([dbc.Row([dbc.Col(dcc.Graph(id="hist_cat_movie")),dbc.Col(dcc.Graph(id="hist_cat_show"))])])

def create_treemap(data_obj):
    data = data_obj.get_country_genre_type_data()
    fig = px.treemap(
        data,
        path=[px.Constant("World"),"region",'country','listed_in'],
        values = 'count',
        color = 'count',
        color_continuous_scale='darkmint',
        
    )
    
    fig.update_layout(
    margin=dict(t=50, l=50, r=50, b=50),  
    font=dict(family='Arial', size=12),  
    hoverlabel=dict(font_size=14),  
    # treemapcolorway=[
    #         '#eff3ff', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6',
    #         '#2171b5', '#08519c', '#08306b'
    #     ] 
    
    

    )
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
    )

    
    return html.Div([
        dcc.Graph(
            id = 'treemap-country-genre',
            figure=fig
        )
    ])




def create_tab_actors():
    return  dbc.Tab(label="Actors",
                    children=dbc.Container([
                        html.H2("Most popular actors by region",style=custom_styles['h2']),
                        dbc.Col([
                                 dcc.Dropdown(
                                    id="dropdown_region_actors",
                                    options = [
                                        
                                        {'label':'Europe','value':'Europe'},
                                        {'label':'North America','value':'North America'},
                                        {'label':'South America','value':'South America'},
                                        {'label':'Asia','value':'Asia'},
                                        {'label':'Ocenia','value':'Ocenia'},
                                        {'label':'World','value':'World'}
                                    ],
                                    value="World",
                                    className="dropdowm-region-css",
                                    style = custom_styles["dropdown-menu-css"]
           
                                ),
                                html.Div([
                                html.Label('Top:', style={'font-size': '15px','margins':'15px'}),
                                dcc.Slider(
                                    
                                    id='slider_actors',
                                    min=1,
                                    max=25,
                                    step=1,
                                    value=5,
                                    marks={i: str(i) for i in range(26)},
                                
                                    ),
                                    ],
                                    style = custom_styles["slider-general"]
                                ),
                                create_hist_actors()
                                
                            ])
                        ],style = custom_styles['main-container']),
                    tab_id="tab_actors")
                    


def create_pie_type(data_boj):
    data = data_boj.get_type_count()
    fig = px.pie(
        data,
        names='type',
        values='part',
        hover_data=['count'],
        labels={'count':'Count',"part":"Percentage","type":"Type"},
        color='type',
        color_discrete_map={"Movie":'rgb(122,229,130)','Tv Show':'rgb(159,255,203)'}
    )
    fig.update_layout(
        legend=dict(font=dict(size=16))
    )
    fig.update_traces(
        customdata=data[['count']].values,
        hovertemplate="<b>%{label}</b><br>Count: %{customdata[0]}<br>Percentage: %{value:.2f}%",
        hoverlabel=dict(font_size=16),  
        
    )
    return dcc.Graph(
        id='pie-chart-type',
        figure=fig
    )

def create_area_type(data_obj):
    data = data_obj.get_type_count_years()
    data = data[data["release_year"]>1970]
    fig = px.area(
        data,
        x='release_year',
        y = 'part',
        color = 'type',
        line_group='type',
        labels={"part":"Percentage",'release_year':'Year'},
        
        color_discrete_map={"Movie":'rgb(122,229,130)','Tv Show':'rgb(159,255,203)'}
    )
    fig.update_layout(
        legend=dict(font=dict(size=16))
    )
    fig.update_traces(
        customdata=data[['count',"type"]].values,

        hovertemplate="<b>%{customdata[1]}</b><br>Count: %{customdata[0]}<br>Percentage: %{y:.2f}%",
        hoverlabel=dict(font_size=14),  
    )
    return dcc.Graph(
        id='area-chart-type',
        figure=fig
    )

def create_line_duration():
    return dcc.Graph(
        id='line-graph-type'
    )


# def create_tab_content_type(data_obj):
#     return  dbc.Tab(label="Content type",
#                     children=dbc.Container([
                        
#                         dbc.Row([
#                             dbc.Col([
#                                 html.H3("Movies vs TV Shows",style = custom_styles["h2"]),
#                                 create_pie_type(data_obj)]
#                             ),
#                             dbc.Col([
#                                 html.H3("Movies vs TV Shows over years",style = custom_styles["h2"]),
#                                 create_area_type(data_obj)
#                         ])
#                         ]),
#                         dbc.Row([
#                         dbc.Col([
#                             html.H2("Average duration over years",style = custom_styles["h2"]),
                            
#                                 dbc.RadioItems(
#                                      id='radio_button_type',
#                                      options=[
#                                          {'label':'Movie','value':'Movie'},
#                                          {'label':'TV Show','value':'TV Show'}                        
#                                      ],
#                                      value='Movie'
#                                  ),create_line_duration()]),
                                
                        
#                     ]),]),
#                     tab_id="tab_content_type")
def create_tab_content_type(data_obj):
    return dbc.Tab(label="Content type",
                   children=dbc.Container([
                       dbc.Row([
                           dbc.Col([
                               html.H3("Movies vs TV Shows", style=custom_styles["h2"]),
                               create_pie_type(data_obj)
                           ],style=custom_styles["main-container"]),
                           dbc.Col([
                               html.H3("Movies vs TV Shows over years", style=custom_styles["h2"]),
                               create_area_type(data_obj)
                           ],style=custom_styles["main-container"])
                       ]),
                       
                           dbc.Col([
                               html.H2("Average duration over years", style=custom_styles["h2"]),
                               dbc.RadioItems(
                                   id='radio_button_type',
                                   options=[
                                       {'label': 'Movie', 'value': 'Movie'},
                                       {'label': 'TV Show', 'value': 'TV Show'}
                                   ],
                                   value='Movie',
                                   style=custom_styles['radio-button']
                               ),
                               dbc.Col(create_line_duration())
                           ],style=custom_styles["main-container"]),
                           
                       
                   ]),
                   tab_id="tab_content_type")


def create_stream_graph():
    return html.Div(
        dcc.Graph(
        id='stream-graph-cat'
    )
    )
def create_content_structure_by_genre(data_obj):
    data = data_obj
    values=['International','Dramas','Comedies','Action','Documentaries','Romantic','Thrillers']
    data_movies = data.get_per_type_cat("Movie",values)
    data_movies=data_movies[data_movies['release_year']>2010]
    data_shows = data.get_per_type_cat("TV Show",values)
    data_shows = data_shows[data_shows['release_year']>2010]
    data_movies['source']  ='Movie'
    data_shows['source']  ='TV Show'
    combined_df = pd.concat([data_movies,data_shows])
    fig = px.bar(combined_df,x='release_year',y='counts',color='source', barmode='group',
                       labels={'release_year':'Years','counts':'Count','source':"Source"}, color_discrete_map={"Movie":'rgb(122,229,130)','Tv Show':'rgb(159,255,203)'})
    fig.update_layout(
        bargap=0.2,  # Gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # Gap between bars of the same location coordinate.
        xaxis=dict(tickmode='linear'),  # Ensure x-axis ticks are linear to avoid overlaps.
        yaxis=dict(showgrid=False),
        font = dict(size=14)
    )
    fig.update_traces(
        
        hoverlabel=dict(font_size=14),  
    )
   
    return html.Div(dcc.Graph(id='histogram-cat'
                               ,figure=fig))

def create_content_structure_by_rating(data_obj):
    data = data_obj.get_corr_genre_rating_year()
    fig = px.scatter(data, x='rating_category', y='category', size='counts', color='category')
    fig.update_layout(font = dict(size=18),     
        xaxis =dict(
            title = 'Rating category',    
            titlefont=dict(size=18),  
            tickfont=dict(size=16)    
        ), 
            yaxis =dict(
            title = 'Category',    
            titlefont=dict(size=18),  
            tickfont=dict(size=1)    
        ),
        legend=dict(font=dict(size=16),title="Rating category"))
    return html.Div([dcc.Graph(id='bubble-cat-rat'
                               ,figure=fig),
                    ])

# def create_tab_content_cat(data_obj):
#     return  dbc.Tab(label="Content category",
#                     children=dbc.Container([
#                         dbc.Col([
#                             dbc.Row([
#                                 dbc.Col(
#                                     dcc.Checklist(
#                                         id='group-sel-cat',
#                                         options=[
#                                             {'label': 'International', 'value': 'International'},
#                                             {'label': 'Dramas', 'value': 'Dramas'},
#                                             {'label': 'Comedies', 'value': 'Comedies'},
#                                             {'label': 'Action', 'value': 'Action'},
#                                             {'label': 'Documentaries', 'value': 'Documentaries'},
#                                             {'label': 'Romantic', 'value': 'Romantic'},
#                                             {'label': 'Thrillers', 'value': 'Thrillers'},
#                                         ],
#                                         value=['International','Dramas','Comedies','Action','Documentaries','Romantic','Thrillers'],
#                                         labelStyle={'display': 'block'}
#                                     ), 
#                                 ),
#                                 dbc.Col([
#                                     dbc.RadioItems(
#                                      id='radio_button_type_cat',
#                                      options=[
#                                          {'label':'Movie','value':'Movie'},
#                                          {'label':'TV Show','value':'TV Show'}                        
#                                      ],
#                                      value='Movie'
#                                 ),
#                                 ])]),
#                                 dbc.Col([
                                    
#                                     create_stream_graph()]
                                    
#                                 )
#                             ]),
#                             dbc.Row([
#                                 create_content_structure_by_rating(data_obj),
#                                 # create_content_structure_by_genre(data_obj)
#                             ]),
#                         ]),
                    
#                     tab_id="tab_content_cat")

def create_tab_content_cat(data_obj):
    return dbc.Tab(label="Content category",
                   children=dbc.Container([
                       
                       dbc.Row([
                        html.H2("Genres popularity over years",style=custom_styles["h2"]),
                           dbc.Col([
                               dcc.Checklist(
                                   id='group-sel-cat',
                                   options=[
                                       {'label': 'International', 'value': 'International'},
                                       {'label': 'Dramas', 'value': 'Dramas'},
                                       {'label': 'Comedies', 'value': 'Comedies'},
                                       {'label': 'Action', 'value': 'Action'},
                                       {'label': 'Documentaries', 'value': 'Documentaries'},
                                       {'label': 'Romantic', 'value': 'Romantic'},
                                       {'label': 'Thrillers', 'value': 'Thrillers'},
                                   ],
                                   value=['International', 'Dramas', 'Comedies', 'Action', 'Documentaries',
                                          'Romantic', 'Thrillers'],
                                   labelStyle={'display': 'block'},
                                   style=custom_styles["check-button"]
                               ),
                           ]),
                           dbc.Col([
                               dbc.RadioItems(
                                   id='radio_button_type_cat',
                                   options=[
                                       {'label': 'Movie', 'value': 'Movie'},
                                       {'label': 'TV Show', 'value': 'TV Show'}
                                   ],
                                   value='Movie',
                                   style=custom_styles['radio-button']
                               ),
                           ]),
                           dbc.Col([
                               create_stream_graph()
                           ])
                       ],style=custom_styles["main-container"]),
                       dbc.Row([
                           html.H2("Correlation between genre and rating category",style=custom_styles["h2"]),
                           dbc.Col([
                               create_content_structure_by_rating(data_obj)
                           ]),
                        #    dbc.Col([
                        #     #    create_content_structure_by_genre(data_obj)
                        #    ])
                       ],style=custom_styles["main-container"])
                   ]),
                   tab_id="tab_content_cat")

def create_network_graph(data_obj):

    data,data_d,data_a = data_obj.get_linked_actors_director()
    
    actors = data['actor'].unique()
    directors = data['director'].unique()
   
   
    num_actors = len(actors)
    num_directors = len(directors)

    outer_radius = 2000
    inner_radius = outer_radius / 4  

    
    angle_increment_actors = 2 * math.pi / num_actors
    angle_increment_directors = 2 * math.pi / num_directors

    
    nodes_actors = []
    for i, actor in enumerate(actors):
        angle = i * angle_increment_actors
        x = outer_radius * math.cos(angle)
        y = outer_radius * math.sin(angle)
        nodes_actors.append({'data': {'id': actor, 'label': actor,"additional_label":data_a[data_a["actor"]==actor]["title"],'type':'actor'}, 'position': {'x': x, 'y': y}, 'classes': 'actor'})

    
    nodes_directors = []
    for i, director in enumerate(directors):
        angle = i * angle_increment_directors
        x = inner_radius * math.cos(angle)
        y = inner_radius * math.sin(angle)
        nodes_directors.append({'data': {'id': director, 'label': director,"additional_label":data_d[data_d["director"]==director]["title"],'type':'director'}, 'position': {'x': x, 'y': y}, 'classes': 'director'})

    
    nodes = nodes_actors + nodes_directors
    edges = [{
        'data':{
            'source':row['actor'],
            'target':row['director'],
            'label':row['title']
        }
    }
    for _,row in data.iterrows()
    ]
    return html.Div([cyto.Cytoscape(
        id="network_graph",
        layout={'name':'preset'},
        style = {'width':"100%",'height':'800px'},
        userZoomingEnabled=False,
        userPanningEnabled=True,
        elements=nodes+edges,
        stylesheet = [
    {
        'selector': 'node',
        'style': {
            
            'label': 'data(label)',
            'color': 'black',
            'font-size': '90px',
            'text-wrap': 'wrap',  
            'text-max-width': '80px',  
            'text-valign': 'center',  
            'text-halign': 'center',  
            'width': '200px',
            'height': '200px'
        }
    },
    {
        'selector': '.actor',
        'style': {
            'background-color': 'rgb(220,220,220)'
        }
    },
    {
        'selector': '.director',
        'style': {
            'background-color': 'rgb(37,161,142)'
        }
    },
    {
        'selector': 'edge',
        'style': {
            'width': 2,
            'line-color': 'black',
            'curve-style': 'bezier',
            'target-arrow-color': 'black',
            'target-arrow-shape': 'triangle',
            'label':"",
            'color': 'black',
            'font-size': '80px',
            'text-background-color': 'white',
            'text-background-opacity': 1,
            'text-background-padding': '3px',
            'text-rotation': 'autorotate'
        }
    },
    
    ],
    
    

    ),    
    
    html.P(id='selected-edge-info',style=custom_styles['response']),
    html.P(id='selected-node-info',style=custom_styles['response'])
    ])

    
def create_tab_general(data):
    return  dbc.Tab(label="General",
                    children=dbc.Container([
                        
                        html.Div(id='output-container'),
                        
                        dbc.Row([
                            dbc.Col(create_table(data,'Movie')),
                            dbc.Col(create_table(data,'TV Show'))
                        ],style =custom_styles["main-container"]),
                        dbc.Container([
                            html.H2("The most popular genres",style=custom_styles['h2']),
                            html.Div([
                                html.Label('Top:', style={'font-size': '15px','margins':'15px'}),
                                dcc.Slider(
                                        id='slider_cat',
                                        min=5,
                                        max=20,
                                        step=1,
                                        value=5,
                                        marks={i: str(i) for i in range(21)},
                                    
                                    )], style = custom_styles['slider-general']),
                                    dbc.Row([
                                        create_chart_cat_counts(),
                                    ]),], 
                                                            
                        style = custom_styles['main-container']),
                        dbc.Container(
                            [html.H2("Genres ordering per coutnries and continents",style=custom_styles["h2"]),
                            create_treemap(data),],
                            style = custom_styles['main-container']),
                        dbc.Container([ 
                            html.H2("Relation between most popular actors and directors",style=custom_styles["h2"]),
                            create_network_graph(data)],style = custom_styles['main-container'])]),
                        tab_id="tab_general")
                        
                    
def create_layout(data):
    return html.Div([
        html.H1("Netflix content analysis", className="heading",style=custom_styles['h1']),
        dbc.Container(
            dbc.Tabs([
                create_tab_general(data),
                create_tab_actors(),
                create_tab_maps(data),
                create_tab_content_type(data),
                create_tab_content_cat(data)
            ], id='tabs',active_tab="tab_general",style=custom_styles["tabs"]),
            fluid = True,
            style = custom_styles['basic-container']
        ),
        dbc.Spinner([
            dcc.Store(id="store"),
            html.Div(id="tab_content",className="p-4"),
        ],
        delay_show=100,
        ),
    ],style=custom_styles['body'])
    