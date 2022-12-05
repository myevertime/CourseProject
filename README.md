# UIUC CS410 Course Project
## Team ACT
> Hyeonjae Cho, hc53@illinois.edu
> 
> Xi Chen, xi12@illinois.edu
> 
> Sean Kan, clkan2@illinois.edu
> 
> Danwoo Park, danwoop2@illinois.edu
> 
> Kihyuk Song, kihyuks2@illinois.edu

#### What is the project about?
Our team built a movie recommendation system that gets input on any queries and returns a list of relevant films, along with their corresponding keywords and taglines. The user can then go through the results, pick films that spark their interest, and get a list of recommendations that are similar to what they like.

The movie recommendation system is built using publicly available data from the following websites:
- MovieLens 25M datasets for movie titles, genres, tags, and user ratings
-- https://grouplens.org/datasets/movielens/25m/
- IMDB for cast and director names
-- https://www.imdb.com/interfaces/
- WikiData for creating a knowledge graph that describes real-world entities and captures the relationships between them.
-- https://query.wikidata.org/

The reason why our team chose a recommendation system is that as the lecture says, future intelligent information systems are expected to be highly personalized and alleviate users’ effort to perform a task. The recommendation system is the way the information system desires to be. In addition, this project would be influential in that we are trying to utilize the WikiData Knowledge Graph algorithm, which is a state-of-the-art recommendation algorithm.

#### Data
Data files are available in https://drive.google.com/drive/folders/1NUS5DCtIsa8MZn0Hd-yRoCGbEbWlKWaT?usp=sharing.

Above link is only accessible with Google Apps@Illinois.

- File list:
1) corpus.txt : A list of movies along with information such as tags, genres, and names of cast and directors for our BM25 model
2) output.csv : Additional movie info for the collaborative filtering system
3) ratings.csv : User ratings for the collaborative filtering system 
