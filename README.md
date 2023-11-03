# Content-Based-Recommendation-System
In the era of information overload, users often face difficulty in finding relevant content. In such a scenario, recommender systems play a crucial role in providing personalized recommendations. With the increasing availability of user data, the need for advanced recommender systems has become more important than ever. The aim of this project is to build a content-based recommender system for music and podcasts that utilizes the NYTimes, Penguin, and Spotify APIs to collect user engagement data and provide personalized recommendations.
The project utilizes the power of natural language processing (NLP) and machine learning techniques to analyze the textual content of NYTimes articles, Spotify songs, and Penguin podcasts. By applying vectorization to the textual data, similarities between articles and songs/podcasts of similar flavor are calculated. This approach enables the system to make personalized recommendations based on user engagement history and the similarity of their interests.


## The Data:
1. NewYorkTimes:
New York Times data was extracted from the nytimes api, three features were selected to be included in the model:
● ‘title’ is the string type input that stores the title of the article.
● ‘caption’ is the string type input that stores the subheading.
● ‘abstract’ is the string type input that stores the article summary.
2. Spotify:
Spotify data was extracted from Spotify’s api: https://developer.spotify.com/documentation/web-api/, and 16 features were selected to be included in the model:
The fields includes:
      artist, album, track_name, track_id, danceability, energy, key,
      loudness, mode, speechiness, instrumentalness, liveness, valence, tempo,
      duration_ms, time_signature
     
  3. Penguin:
The data was from https://developer.penguinrandomhouse.com/io-docs. We used requests package to get json string then read and process the data.
The fields includes:
      title, author, onsale (which is the date which it gets on sale),
language, praises, authorBio, aboutTheBook, keynote, categories
  
  The Analytical Goals:
The primary analytical goal of this project is to develop a content-based recommender system for music that utilizes NYTimes, Penguin, and Spotify APIs to collect user engagement data and provide personalized recommendations.
The system's analytical goals are to:
1. Collectuserengagementdata:Thesystemcollectsuserengagementdata from NYTimes, Penguin, and Spotify APIs to understand user preferences and behavior. This data includes the articles read, songs played, and podcasts listened to by the user.
 
2. Analyzetextualcontent:ThesystemusesNLPtechniquestoanalyzethe textual content of the articles, songs, and podcasts to extract relevant features and create vectors.
3. Calculatesimilarities:Thesystemcalculatesthesimilaritybetweenthe vectors of the articles and the songs/podcasts to identify articles and songs/podcasts of similar flavor.
4. Providepersonalizedrecommendations:Thesystemprovidespersonalized recommendations based on the user's engagement history and the similarity of their interests.
The analytical goals of this project are aligned with the objective of building a content-based recommender system that provides personalized recommendations for music and podcasts. By achieving these goals, the system can provide relevant content to users, enhance the content discovery experience, and offer insights into user engagement behavior for content providers.
4. The Data Pipeline:
The goal is to build an Automated Scalable ML Pipeline.The data from three APIs are downloaded into my machine as json objects. These json objects are uploaded to my google cloud clusters right after. After this, the data is downloaded as raw data from gcs, then we process the data in my local machine into a list of jsons. After this, the aggregates are uploaded into mongodb where each json file in the list as a document. Next, the data is downloaded from mongodb to databricks and converted into dataframe to build the model.
