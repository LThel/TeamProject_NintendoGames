import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import plotly.graph_objects as go
import plotly.express as px




#Import data
df_sales=pd.read_csv("df_top.csv")
df_sales = df_sales[['Names', 'total_shipped_clean']]
df = pd.read_csv("data.csv")
Nintendodb = df

#getting my code right(gabriel)
#Adjust the dataframe
#Adjust the columns of the data set (main_genre and year)
df['year'] = df['date'].str.split(',').str[1].str.strip()
df['genres'] = df['genres'].apply(lambda x : "[]" if type(x) != str else x)\
    .apply(lambda x : eval(x))

#droping nan values when they are in both meta_score and user_score columns
nintendo1 = Nintendodb.dropna(how="all",subset=("meta_score","user_score")).drop(labels="esrb_rating", axis=1)
#there are values with "TBA" in date column, therefore we need to change it to nan
# replace 'TBA' with NaN
nintendo1['date'] = nintendo1['date'].replace('TBA', np.nan)
# convert the 'date_column' to datetime type
nintendo1['date'] = pd.to_datetime(nintendo1['date'], format='%b %d, %Y')



#Create a main genre
top16 = df['genres']\
        .explode().value_counts().index[0:16]
def grab_the_most_produced(genre_list, top_list):
#turn into set and intersect !!!     
    crossing_genres = np.intersect1d(np.array(genre_list), np.array(top_list))
    output = []
    if len(crossing_genres)>0:
        for item in top_list:
            if item in crossing_genres:
                output.append(item)
        return output[0]
    elif 'Simulation' in genre_list:
        return 'Simulation'
    elif 'Driving' in genre_list:
        return 'Driving'
    else :    
        return 'Other'
df['main_genre'] = df['genres'].apply(grab_the_most_produced, top_list = top16)
        
#Streamlite
st.set_page_config(
    page_title="Project 3 - Video Games Analysis",
    page_icon=":smiley:",
    layout="wide",
)

dash = st.sidebar.radio(
    "What dashboard do you want to see ?",
    ('What happened to games?', 'Clash & Platforms', 'Tips for your game', "What about Sales?"))

if dash == "What happened to the games ?":
    st.header("What Happened to games?")
    st.subheader("Are games getting worst as years go by?")
    st.header("")
    col1, col2 = st.columns(2)
    with col2:
        st.subheader("Do the experts agree?")
        st.header("")
        fig, ax = plt.subplots(1,1)
        viz_bar1 = sns.scatterplot(data=nintendo1, x="date", y="meta_score")
        plt.xticks(rotation=45)
        plt.title('Customer Evaluation vs Meta score, per year')
        st.pyplot((viz_bar1.figure))
    with col1:
        st.subheader("Do you notice how as we approach to more recent years, people enjoy the games less and less?")
        fig, ax = plt.subplots(1,1)
        viz_bar1 = sns.scatterplot(data=nintendo1, x="date", y="user_score")
        plt.xticks(rotation=45)
        plt.title('Customer Evaluation per year')
        st.pyplot((viz_bar1.figure))
    st.subheader("As we can see even there are differences between how experts(meta_score) and customers rate the game.")
    col3, col4 = st.columns(2)    
    with col3:
        st.subheader("this raises the question: how different are experts rating the games relative to customers?" )
        fig, ax = plt.subplots(1,1)
        viz_bar2 = sns.scatterplot(data=nintendo1, x="date", y="user_score", hue="meta_score")
        plt.xticks(rotation=45)
        plt.title('Customer Evaluation per year')
        st.pyplot((viz_bar2.figure))
        st.write("the max rated game by the users over this years was:")
        st.write(nintendo1[["title", "user_score"]].max())

    with col4:
        st.subheader("Are games for new platforms worst than the games for old platforms?")
        fig, ax = plt.subplots(1,1)
        viz_bar3=sns.histplot(data = nintendo1, x="platform", y="meta_score")
        plt.xticks(rotation=45)
        plt.title('Customer Score per platform')
        st.pyplot((viz_bar3.figure))

elif dash == 'Clash & Platforms':
    # Define the colors to use for the charts
    colors = ['orange', 'blue', 'green', 'red', 'purple', 'gray', 'cyan', 'magenta', 'yellow', 'brown']
    # Create a Streamlit app
    st.title('Clash & Platforms Dashboard')
    # Add a chart showing the number of games per platform as a pie chart
    platform_counts = df['platform'].value_counts().sort_values(ascending=False)
    fig_pie = go.Figure(go.Pie(
        labels=platform_counts.index,
        values=platform_counts.values,
        marker=dict(colors=colors[:len(platform_counts)])
    ))
    fig_pie.update_layout(
        title='Number of Games per Platform (Pie Chart)',
    )
    st.plotly_chart(fig_pie)
    # Add a chart showing the number of games per platform as a bar chart
    fig_bar, ax = plt.subplots(figsize = (3, 1.5))
    fig_bar = go.Figure(go.Bar(
        x=platform_counts.index,
        y=platform_counts.values,
        marker_color=colors[:len(platform_counts)],
        text=platform_counts.values,
        textposition='inside',
    ))
    fig_bar.update_layout(
        title='Number of Games per Platform (Bar Chart)',
        xaxis_title='Platform',
        yaxis_title='Number of Games')
    
    st.plotly_chart(fig_bar)

    # Create separate DataFrames for Super Mario and Pokemon games
    mario_df = df[df['title'].str.contains('Mario')]
    pokemon_df = df[df['title'].str.contains('Pokemon')]
    # Compare the number of games released for each franchise
    mario_count = len(mario_df)
    pokemon_count = len(pokemon_df)
    st.write(f'Super Mario: {mario_count} games')
    st.write(f'Pokemon: {pokemon_count} games')
    # Compare the average user ratings for each franchise
    mario_rating = mario_df['user_score'].mean()
    pokemon_rating = pokemon_df['user_score'].mean()
    st.write(f'Super Mario: {mario_rating:.2f} average rating')
    st.write(f'Pokemon: {pokemon_rating:.2f} average rating')
    # Create a bar chart of the number of games released for each franchise
    fig, ax = plt.subplots()
    ax.bar(['Super Mario', 'Pokemon'], [mario_count, pokemon_count])
    ax.set_title('Number of Games Released')
    ax.set_ylabel('Count')
    st.pyplot(fig)
    # Create a new DataFrame with the relevant columns for the box plot
    boxplot_df = pd.concat([mario_df[['title', 'user_score']].assign(Franchise='Super Mario'),
                            pokemon_df[['title', 'user_score']].assign(Franchise='Pokemon')])
    # Create a box plot comparing the user ratings distribution
    fig_box = px.box(boxplot_df, x='Franchise', y='user_score', color='Franchise',
                 title='User Ratings Distribution for Super Mario and Pokemon Games',
                 labels={'Franchise': 'Game Franchise', 'user_score': 'User Rating (out of 10)'})
    st.plotly_chart(fig_box)
    
elif dash == 'Tips for your game':
    start_year = st.slider('What is the first year do you want to consider ?', 1996, 2020, 2015)
    df['year'] = df['year'].apply(lambda x : float(x))
    df_tempo = df[df['year']>start_year]
    #The most active competitors
    st.subheader('Top 10 well rated genres (user score in red and meta score in blue)')
    df_tempo_bis = pd.DataFrame()
    df_tempo_bis['main_genre'] = df_tempo['main_genre'].value_counts().sort_index().index
    df_tempo_bis['number_of_games'] = df_tempo['main_genre'].value_counts().sort_index().values
    df_tempo_bis['avg_user_score'] = df_tempo['user_score'].groupby(by = df_tempo['main_genre']).mean().sort_index().values
    df_tempo_bis['avg_meta_score'] = df_tempo['meta_score'].groupby(by = df_tempo['main_genre']).mean().sort_index().values
    df_tempo_user_10_bis = df_tempo_bis.sort_values(by = 'avg_user_score', ascending = False)[0:10]
    df_tempo_meta_10_bis = df_tempo_bis.sort_values(by = 'avg_meta_score', ascending = False)[0:10]

    fig_1_3, ax = plt.subplots(1,2, figsize=(3, 1.5))
    #sns.barplot(x = df_tempo_bis['main_genre'], y = df_tempo_bis['avg_user_score'], hue= df_tempo_bis['number_of_games'].apply(lambda x:int(x)))
    my_cmap1 = plt.get_cmap("Reds")
    ax[0].bar(x=  df_tempo_user_10_bis['main_genre'],
            height = df_tempo_user_10_bis['avg_user_score'],
            color=my_cmap1(df_tempo_user_10_bis['number_of_games']), label = True)
    my_cmap2 = plt.get_cmap("Blues")
    ax[0].tick_params('x', labelrotation=90, labelsize = 7)
    ax[0].set_ylabel("Score")
    ax[1].bar(x=  df_tempo_meta_10_bis['main_genre'],
            height = df_tempo_meta_10_bis['avg_meta_score']/10,
            color=my_cmap2(df_tempo_meta_10_bis['number_of_games']), label = True)
    ax[1].set_ylabel("")
    ax[1].set_yticks([], [])
    plt.xticks(rotation = 90, fontsize = 7)
    st.pyplot(fig_1_3)
    
    #The platform to target
    st.subheader('The platform to target : Average rating per platform')
    #The most active competitors
    df['year'] = df['year'].apply(lambda x : float(x))
    df_tempo = df[df['year']>start_year]
    df_tempo_bis = pd.DataFrame()
    df_tempo_bis['platform'] = df_tempo['platform'].value_counts().sort_index().index
    df_tempo_bis['number_of_games'] = df_tempo['platform'].value_counts().sort_index().values
    df_tempo_bis['avg_user_score'] = df_tempo['user_score'].groupby(by = df_tempo['platform']).mean().sort_index().values
    df_tempo_bis['avg_meta_score'] = df_tempo['meta_score'].groupby(by = df_tempo['platform']).mean().sort_index().values
    df_tempo_user_10_bis = df_tempo_bis.sort_values(by = 'avg_user_score', ascending = False)[0:10]
    df_tempo_meta_10_bis = df_tempo_bis.sort_values(by = 'avg_meta_score', ascending = False)[0:10]

    fig2_3, ax = plt.subplots(1,2, figsize=(3, 1.5))
    my_cmap1 = plt.get_cmap("Reds")
    ax[0].bar(x=  df_tempo_user_10_bis['platform'],
            height = df_tempo_user_10_bis['avg_user_score'],
            color=my_cmap1(df_tempo_user_10_bis['number_of_games']), label = True)
    my_cmap2 = plt.get_cmap("Blues")
    ax[0].tick_params('x', labelrotation=90, labelsize = 7)
    ax[0].set_ylabel("Score")
    ax[1].bar(x=  df_tempo_meta_10_bis['platform'],
            height = df_tempo_meta_10_bis['avg_meta_score']/10,
            color=my_cmap2(df_tempo_meta_10_bis['number_of_games']), label = True)
    ax[1].set_ylabel("")
    ax[1].set_yticks([], [])
    plt.xticks(rotation = 90, fontsize = 7)
    st.pyplot(fig2_3)
    
    st.subheader('The most active competitors : Are they loved by the users ?')
    #Study the competitors - run only once
    df['developers'] = df['developers'].apply(lambda x : "[]" if type(x) != str else x).apply(lambda x : x.strip())\
    .apply(lambda x : eval(x))
    
    #The most active competitors
    df['year'] = df['year'].apply(lambda x : float(x))
    df_tempo = df[df['year']>start_year].explode('developers')
    df_tempo_bis = pd.DataFrame()
    df_tempo_bis['developers'] = df_tempo['developers'].value_counts().sort_index().index
    df_tempo_bis['number_of_games'] = df_tempo['developers'].value_counts().sort_index().values
    df_tempo_bis['avg_user_score'] = df_tempo['user_score'].groupby(by = df_tempo['developers']).mean().sort_index().values
    df_tempo_10_bis = df_tempo_bis.sort_values(by = 'number_of_games', ascending = False)[0:10]

    fig3_3, ax = plt.subplots(1, figsize=(3, 1.5))
    sns.scatterplot(x = df_tempo_10_bis['developers'], y = df_tempo_10_bis['avg_user_score'], size= df_tempo_10_bis['number_of_games'], legend=False, sizes=(5, 500), color = 'red')
    plt.xticks(rotation = 90, fontsize = 5)
    plt.ylabel('Average user score', size = 7)
    plt.xlabel('')
    plt.yticks(fontsize = 5)
    plt.ylim((0, 10))
    st.pyplot(fig3_3)
    
    st.subheader('What about a collaboration ?')
#Extracted from Webscrapping on vgchartz
elif dash == "What about Sales?":
    st.header("What are the 10 best and 10 worst games ever from Nintendo?")
    st.subheader('Top 10 worst games')
    st.table(df_sales.head(10))
    
    st.subheader('Top 10 best games')
    st.table(df_sales.tail(10).iloc[::-1])
    
    viz_bar4=sns.barplot(data=df_sales.tail(10), x="Names", y= "total_shipped_clean", color = 'red')
    plt.xticks(rotation=90)
    plt.title('Top 10 Sales')
    st.pyplot((viz_bar4.figure))
