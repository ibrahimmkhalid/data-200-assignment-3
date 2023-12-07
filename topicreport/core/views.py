from django.shortcuts import render
from django.http import HttpResponse
import core.backend as backend

def index(request):
    
    # list of graphs to display
    # each graph has a title, text, and id
    # the id is used to determine which graph to display from backend.py
    graphs = [
        {
            "title": "Yearly releases",
            "text": """From the graph, we can very clearly see an increase in the 
                    number of video games released over the last 40 years. This can be attributed to
                    the increase in gaming popularity and the rise of demand for video games. We can
                    also use linear regression to see the trendline of the graph, and using that to 
                    extrapolate the number of games released in the future.""",
            "id": 0
        },
        {
            "title": "Trends within the year",
            "text": """While the previous graph showed the yearly trend, this graph
                    shows the trend of games released within a year. We can see two spikes in the graph.
                    The first spike is in February to March, corresponding to the release of games for
                    the spring season, leading into summer break. The second spike is in September to
                    November, corresponding to the release of games for the holiday season.""",
            "id": 1
        },
        {
            "title": "Top 15 genres",
            "text": """This graph shows the number of games released in each genre.
                    We can see that the most popular genre is "Adventure", followed by "RPG", then
                    "Shooter". Some genres have made recent jumps in popularity, such as "Indie",
                    and "Visual Novel". These jumps in popularity can be attributed to the rise of
                    small development teams in gaming and the rise of japanese media in the west.""",
            "id": 2
        },
        {
            "title": "Times listed vs. Rating vs. Number of playing",
            "text": """This graph shows the relationship between the number of times
                    a game is listed, the rating of the game, and the number of people playing the game 
                    (marker size). From the graph, we can see that the more a game is listed, the higher
                    it is rated. The log scale allows us to see this more clearly. It is interesting to note
                    that some games have a very high number of people playing, but are not rated very highly.
                    For instance, "Genshin Impact", has a rating of 2.6, but 2700 concurrent players.""",
            "id": 3
        },
    ]

    # wordcloud data
    # defined separately from graphs because it is a special interactive element
    wordcloud = {
        "title": "Reviews for top games",
        "text": """This wordcloud shows the most common words used in the reviews of 
                the top 100 games. The reviews for the top 100 games mostly refer to 'Story' and 'time'.
                By increasing the number of games, we can see more words such as 'fun', get emphasized,
                while 'story' gets deemphasized. Take a look by using the selector below.""",
        "values": [100, 300, 500, 1000]
    }

    # context is a dictionary that is passed to the html file
    context = {
        "graphs": graphs,
        "wordcloud": wordcloud
        }
    return render(request, 'index.html', context=context )

def basic_graph(request):
    params = request.GET.dict()
    
    # get graph id from params as defined above
    graph = int(params.get('graph'))

    # get figure from backend and convert to html
    fig = backend.get_data(graph).to_html(include_plotlyjs='cdn',
                                          full_html=False,
                                          config={
                                              'displayModeBar': False
                                              }
                                          )
    return HttpResponse(fig)

def wordcloud(request):
    params = request.GET.dict()

    # get number of games from params
    game_count = int(params.get('game_count'))

    # get figure from backend and convert to html
    fig = backend.get_wordcloud(game_count).to_html(include_plotlyjs='cdn', 
                                                    full_html=False,
                                                    config={
                                                        'displayModeBar': False, 
                                                        'staticPlot': True
                                                        },
                                                    )
    
    return HttpResponse(fig)