import pandas as pd
import numpy as np
import re

def extract_duration(duration):
        
        match = re.match(r'(\d+)', str(duration))
        if match:
            return int(match.group(1))
        return None

def matching_strings(search_string,my_list):

    matching_elements = [element.lower() for element in my_list if element.lower() in search_string.lower()]
    
    return matching_elements[0]


def transform_category(cat):
    hashmap={
    'Documentaries':"documentaries",
    'Comedies':"comedies",
    'Dramas':'drama',
    'International Movies':'international',
    'Thrillers':'thrillers',
    'Action & Adventure':"action",
    'Music & Musicals':"music",
    'Sports Movies':"sport",
    'Independent Movies':"international",
    'Children & Family Movies':"children",
    'Horror Movies':"horror",
    'Romantic Movies':"romantic",
    'Sci-Fi & Fantasy':"sci-fi",
    'Anime Features':'anime',
    'Docuseries':'documentaries',
    'LGBTQ Movies':'LGBTQ',
    'Cult Movies':'cult',
    'International TV Shows':'international',
    'TV Dramas':'dramas',
    'Teen TV Shows':'teen',
    'Faith & Spirituality':'cult',
    'Classic Movies':'classic',
    'Reality TV':'reality',
    'Spanish-Language TV Shows':'Spanish-Language',
    'Stand-Up Comedy':'stand-up comedy',
    'Korean TV Shows':"korean",
    'Stand-Up Comedy & Talk Shows':'stand-up comedy',
    'Crime TV Shows':"crime",
    'TV Action & Adventure':"action",
    'Romantic TV Shows':'romantic',
    'TV Comedies':'comedies',
    'British TV Shows':'british',
    'Anime Series':'anime',
    "Kids' TV":'children',
    'TV Horror':'horor',
    'TV Shows':'shows',
    'TV Mysteries':'mysteries',
    'Classic & Cult TV':'classic',
    'TV Sci-Fi & Fantasy':'sci-fi',
    'Movies':'movies',
    'TV Thrillers':'thrillers',
    'Science & Nature TV':'science',
    'Sci-fi':'sci-fi',
    'Horror':'horror',
    'Action':'action',
    'Drama':'drama',
    'Romance':'romantic',
    'Thriller':'thriller'
    }
    return hashmap[cat]
def map_to_category(rating):
    if rating in ['G', 'TV-Y',  'TV-G']:
        return 'Children'
    elif rating in ['TV-PG','TV-Y7','TV-Y7-FV']:
        return 'Older children'
    elif rating in ['PG-13','PG','TV-14']:
        return 'Teen'
    elif rating in [ 'R', 'NC-17', 'TV-MA','A']:
        return 'Adults'
    else:
        return 'Unrated'

class DataClass():
    def __init__(self,path_1,path_2):
        self.data = pd.read_csv(path_1,encoding = 'latin-1')
        # self.data["type"] = self.data["type"].replace({'Movie':'Film','TV Show':'TV Serija'})
        self.data = self.data.iloc[:,:12]
        
        self.country_continet = pd.read_csv(path_2)
        merged_df = self.data.copy()
        merged_df['country'] = merged_df['country'].str.split(', ')
        merged_df = merged_df.explode('country') 
        merged_df = pd.merge(merged_df,self.country_continet,left_on="country",right_on="Country",how="left")
        merged_df.drop(columns=["Country"],inplace=True)
        merged_df.rename(columns={"Continent":"region"},inplace=True)
        self.country_data = merged_df.copy()
        self.country_data['cast'] = self.country_data['cast'].str.split(",")
        self.country_data = self.country_data.explode('cast') 
    def get_data(self):
        return self.data

    def get_type_count(self):
        types = self.data.groupby("type").size().reset_index(name="count")
        sum_counts = types[types["type"].isin(["Movie", "TV Show"])]["count"].sum()
        types["part"] = types["count"]/sum_counts*100
        return types
    
    def get_type_count_years(self):
        types = self.data.groupby(["type",'release_year']).size().reset_index(name="count")
        sum_counts = types[types["type"].isin(["Movie", "TV Show"])]["count"].sum()
        types["part"] = types["count"]/sum_counts*100
        return types
    
    
    def get_data_type_per_year(self):
        
        data = self.data[["release_year","duration","type"]].copy()
        data.dropna(inplace=True)
        data["num_duration"] = data["duration"].apply(extract_duration)
        return data
    
    

    def get_number_per_country(self,region):
        
        if region=="World":
            country_counts = self.country_data.groupby(["country","region"]).size().reset_index(name="count")
        else:
            country_counts = self.country_data[self.country_data["region"]==region].reset_index(drop=True).groupby(["country","region"]).size().reset_index(name="count")
        return country_counts
    
    def get_number_per_actors(self,region):
        
        if region=="World":
            actors_counts = self.country_data.groupby(["cast","country"]).size().reset_index(name="count")
        else:
            actors_counts = self.country_data[self.country_data["region"]==region].reset_index(drop=True).groupby(["cast","country"]).size().reset_index(name="count")
        
        actors_counts = actors_counts.sort_values(by="count", ascending=False)
        return actors_counts
    
    def get_per_type_cat(self, type="", cat=""):
        data = self.data.copy()
        data['listed_in'] = data['listed_in'].str.split(', ')
        data = data.explode('listed_in') 
        
        filtered_data = data[data["type"] == type]
        if cat:
        
            pattern = '|'.join(cat)
            filtered_data = filtered_data[filtered_data["listed_in"].str.lower().str.contains(pattern.lower())]
            data_result = filtered_data.groupby(["type", "listed_in", "release_year"]).size().reset_index(name="counts")
            data_result["category"] = data_result["listed_in"].apply(matching_strings, args=(cat,)) 
        else:
            data_result = pd.DataFrame()
        return data_result
    

    def get_corr_genre_rating_year(self):
        data = self.data.copy()
        data['listed_in'] = data['listed_in'].str.split(', ')
        data = data.explode('listed_in') 
        cat = ['International','Dramas','Comedies','Action','Documentaries','Romantic','Thrillers']
        
        
        filtered_data = data.copy()
        if cat:
            pattern = '|'.join(cat)
            filtered_data = filtered_data[filtered_data["listed_in"].str.lower().str.contains(pattern.lower())]
            data_result = filtered_data.groupby(["type", "listed_in", "release_year","rating"]).size().reset_index(name="counts")
            data_result["category"] = data_result["listed_in"].apply(matching_strings, args=(cat,)) 
            data_result["rating_category"] = data_result["rating"].apply(map_to_category)
        data_result_1 = data_result.groupby(["category","rating_category"]).size().reset_index(name="counts")
        
        return data_result_1    
    
    def get_most_popular_genre(self):
        data = self.data.copy()
        data["listed_in"]=data["listed_in"].str.split(', ')
        data = data.explode('listed_in')
        data["listed_in"] = data["listed_in"].apply(transform_category)
        data_counts = data.groupby(['listed_in','type']).size().reset_index(name='counts')
        data_1 = data_counts[data_counts["type"]=="Movie"]
        data_2 = data_counts[data_counts["type"]=="TV Show"]
        
        data_1.sort_values(by="counts", ascending=False,inplace=True)
        data_2.sort_values(by="counts", ascending=False,inplace=True)

        return (data_1,data_2)
    
    def get_linked_actors_director(self):
        data = self.data.copy()
        
        data["director"] = data["director"].str.split(', ')
        data = data.explode('director')
        data["cast"] = data["cast"].str.split(', ')
        data = data.explode('cast')
        top_actors = data.groupby('cast').size().reset_index(name='counts').sort_values(by='counts',ascending=False).head(50)['cast'].values
        
        top_directors = data.groupby('director').size().reset_index(name='counts').sort_values(by='counts',ascending=False).head(10)['director'].values
        result_1 = pd.DataFrame()
        for director in top_directors:
            for actor in top_actors:
                if not(data[(data["director"]==director) & (data["cast"]==actor)].empty):
                    new_row=pd.DataFrame({
                        "title":data[(data["director"]==director) & (data["cast"]==actor)]["title"],
                        "director":director,
                        "actor":actor
                    })
                    result_1 = pd.concat([result_1,new_row],ignore_index=True)
        
        result_1.drop_duplicates(inplace=True)
        result_1 = result_1.groupby(["director", "actor"])["title"].agg(lambda x: ', '.join(x)).reset_index()
        
        result_2 = pd.DataFrame()
        for director in top_directors:
            if not(data[(data["director"]==director)].empty):
                    new_row=pd.DataFrame({
                        "director":director,
                        "title":data[(data["director"]==director)]["title"]
                        
                    })
                    result_2 = pd.concat([result_2,new_row],ignore_index=True)
        
        result_2.drop_duplicates(inplace=True)
        result_2 = result_2.groupby(["director"])["title"].agg(lambda x: ', '.join(x)).reset_index()
        
        result_3 = pd.DataFrame()
        for actor in top_actors:
            if not(data[(data["cast"]==actor)].empty):
                    new_row=pd.DataFrame({
                        "actor":actor,
                        "title":data[(data["cast"]==actor)]["title"]
                        
                    })
                    result_3 = pd.concat([result_3,new_row],ignore_index=True)
        
        result_3.drop_duplicates(inplace=True)
        result_3 = result_3.groupby(["actor"])["title"].agg(lambda x: ', '.join(x)).reset_index()
        
        return [result_1,result_2,result_3]

    def get_country_genre_type_data(self):
        data = self.country_data.copy() 
        columns_for_grouping = data.columns.tolist()
        columns_for_grouping.remove('cast')
        data = data.groupby(columns_for_grouping)["cast"].agg(lambda x: ', '.join(str(v) for v in x)).reset_index()
        data["listed_in"]=data["listed_in"].str.split(', ')
        data = data.explode('listed_in')
        # print(data["listed_in"].unique())
        data['listed_in'] = data['listed_in'].apply(transform_category)
        # print(data["listed_in"].unique())
        data = data.groupby(["region","country","listed_in"]).size().reset_index(name="count")
        return data
    def test(self):
        

            # data = data.dropna(subset=['director']) 
        # print(len(data))
        # data["director"]=data["director"].str.split(', ')
        # data = data.explode('director')
        # data["cast"]=data["cast"].str.split(', ')
        # data = data.explode('cast')
        # data = data.dropna(subset=['cast','director']) 
        # print(len(data['director'].unique()))
        # print(len(data["cast"].unique()))
        
        
        return