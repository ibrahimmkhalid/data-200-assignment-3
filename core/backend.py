# import pandas as pd
# import plotly.graph_objects as go
# import ast
# from wordcloud import WordCloud, STOPWORDS
import os
from django.conf import settings

def get_data(graph):
    # get the path of the data file
    data_file_path = os.path.join(settings.BASE_DIR, 'core/data/scrubbed.csv')

    # reading data
    df = pd.read_csv(data_file_path)
    fig = None

    if graph == 0:
        # yearly trend graph
        yearly_count = df.groupby("year").count().reset_index()[["year", "Title"]]
        yearly_count = yearly_count[:-1]
        fig = go.Figure(data=go.Scatter(
            x=yearly_count["year"], 
            y=yearly_count["Title"],
            mode='lines',
            marker=dict(color='#2979b9'),
            hovertemplate="Number of Releases: %{y}",
            name="Original Data"))
        
        # only import these if we need them
        # from sklearn.linear_model import LinearRegression
        # from sklearn.preprocessing import PolynomialFeatures

        # perform polynomial regression
        lr = LinearRegression()
        poly = PolynomialFeatures(degree=2)

        # transform data to fit into polynomial regression
        X = poly.fit_transform(yearly_count["year"].values.reshape(-1, 1))
        # fit data to polynomial regression
        lr.fit(X, yearly_count["Title"].values.reshape(-1, 1))

        # plot trendline
        x = [x for x in range(1980, 2022)]
        y = lr.predict(poly.fit_transform(pd.Series(x).values.reshape(-1, 1)))
        fig.add_trace(go.Scatter(x=x, y=y.flatten(), name="Trendline", line=dict(color='#0E5A99', dash='dash')))

        # plot prediction
        x = [x for x in range(2022, 2031)]
        y = lr.predict(poly.fit_transform(pd.Series(x).values.reshape(-1, 1)))
        fig.add_trace(go.Scatter(x=x, y=y.flatten(), name="Prediction", line=dict(color='#1588E6', dash='dash')))

        # update layout with desired settings for this specific graph
        fig.update_layout(
            hovermode="x",
            xaxis=dict(title='Year'),
            yaxis=dict(title='Number of Releases'),
            xaxis_tickvals=[x for x in range(1980, 2031, 5)],
            yaxis_tickvals=[x for x in range(0, 101, 20)],
            showlegend=True,
            legend=dict(x=0, y=1.0, bgcolor='rgba(0,0,0,0)'),
        )
    elif graph == 1:

        # monthly trend graph
        fig = go.Figure(data=go.Histogram(
            x=df["month"], 
            nbinsx=13, 
            marker=dict(color='#2979b9', line=dict(color='black', width=1)),
            hovertemplate="Number of Releases: %{y}", 
            name=""))

        # update layout with desired settings for this specific graph
        fig.update_layout(
            hovermode="x",
            xaxis=dict(title='Month'),
            yaxis=dict(title='Number of Releases'),
            xaxis_tickvals=[x for x in range(1, 13)],
            xaxis_ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            bargap=0.1
        )
    elif graph == 2:

        # convert genres from string to list
        df["Genres"] = df["Genres"].apply(ast.literal_eval)

        # explode comma separated genres into separate rows
        genres = df.explode('Genres').groupby('Genres').count().reset_index()[["Genres", "Title"]].sort_values(by="Title")

        # only show top 15 genres
        genres = genres[-15:]

        # plot bar graph for genres
        fig = go.Figure(data=go.Bar(
            x=genres["Title"],
            y=genres["Genres"],
            orientation='h',
            marker=dict(color='#2979b9', line=dict(color='black', width=1)),
            hovertemplate="Number of Releases: %{x}",
            name=""
        ))

        # update layout with desired settings for this specific graph
        fig.update_layout(
            hovermode="y",
            yaxis=dict(title='Genre'),
            yaxis_tickvals=genres["Genres"],
            xaxis=dict(title='Number of Releases'),
            bargap=0.1
        )
    elif graph == 3:
        # create scatter plot for times listed vs rating
        fig = go.Figure(data=go.Scatter(
            x=df["Times Listed"],
            y=df["Rating"], 
            mode='markers', 
            # adding player count information to marker size
            marker=dict(
                size=df["Playing"],
                sizemode='area',
                sizeref=2.0 * max(df["Playing"])/(30.**2),
                sizemin=2,
                color='#2979b9',
            ),
            opacity=0.90,
            text=df["Title"], 
            hovertemplate="Rating: %{y}<br>Times Listed: %{x}<br>Title: %{text}<br>Player count: %{marker.size}", 
            name=""))

        # update layout with desired settings for this specific graph
        fig.update_layout(
            xaxis=dict(title='Times Listed (log scale)', type='log'),
            yaxis=dict(title='Rating'),
        )
    else:
        # should never get here
        fig = go.Figure()

    # update layout with desired settings for all graphs
    fig.update_layout(
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
        font_family="Rockwell",
        font_size=16,
        # remove background color to blend better with website background
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # magic numbers for margins
        margin=dict(l=15, r=15, t=75, b=115)
    )

    return fig

def get_wordcloud(n):

    # get the path of the data file
    data_file_path = os.path.join(settings.BASE_DIR, 'core/data/scrubbed.csv')

    # reading data
    df = pd.read_csv(data_file_path)

    # sort by score and pick top n games
    df = df.sort_values(by="score", ascending=False)[:n]

    # join all reviews into one string
    wordcloud_str = ' '.join(df[df['Reviews'] != 'nan']['Reviews'])

    # add custom stopwords
    custom_stopwords = ["really", "n", "s", "one", "good", "game", "games", "still"]

    stopwords = set(STOPWORDS)
    stopwords.update(custom_stopwords)

    # generate wordcloud
    wordcloud = WordCloud(
        stopwords=stopwords,
        background_color="#f3f4f6", # color corresponds to tailwindcss color bg-gray-100
        width=1440,
        height=720,
    ).generate(wordcloud_str)

    # plot wordcloud as image
    fig = go.Figure()
    fig.add_trace(go.Image(z=wordcloud))

    # update layout with desired settings for wordcloud
    fig.update_layout(
        hovermode=False,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        # remove background color to blend better with website background
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # more magic numbers for margins
        margin=dict(l=15, r=15, t=78, b=78),
    )
    return fig
