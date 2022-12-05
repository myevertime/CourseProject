import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import operator
import pickle # for create pickle file

"""
####################################### Read and process the original file before creating the pickle file
output = pd.read_csv('output.csv')
ratings = pd.read_csv('ratings.csv')
output.head()
ratings.head()


# null = 0
ratings.rating.replace({0 : np.nan}, regex = True, inplace = True)

# rating ratio
ratings.groupby("rating").count().iloc[:, :1] / ratings.count().userId * 100

# output + ratings
output_ratings = ratings.merge(output, left_on = 'movieId', right_on = 'movieId')
output_ratings.head()

# making match_df for movieId - title matching
match_df = output_ratings[['movieId', 'title']]
match_df.drop_duplicates(inplace = True)
match_df.head()

# making input for pivoting
pivot_input = output_ratings[['userId', 'movieId', 'rating']]
pivot_input = pivot_input[pivot_input.userId <= 6500]  # processing error with file size

######################################## Create pickle file for github upload (< 25MB file size)
with open("pivot_input.pickle", "wb") as w:
    pickle.dump(pivot_input, w)
with open("match_df.pickle", "wb") as w2:
    pickle.dump(match_df, w2)
"""
 
with open("pivot_input.pickle", "rb") as r:
    pivot_input = pickle.load(r)
with open("match_df.pickle", "rb") as r2:
    match_df = pickle.load(r2)    

pivot = pivot_input.pivot_table(index = ['userId'], columns = ['movieId'], values = 'rating')

norm_pivot = pivot.apply(lambda x : (x - np.min(x)) / (np.max(x) - np.min(x)), axis = 1)
norm_pivot.fillna(0, inplace = True)
norm_pivot = norm_pivot.T
norm_pivot = norm_pivot.loc[:, (norm_pivot != 0).any(axis = 0)]

sparse_pivot = csr_matrix(norm_pivot.values)

item_similarity = cosine_similarity(sparse_pivot)
user_similarity = cosine_similarity(sparse_pivot.T)

is_df = pd.DataFrame(item_similarity, index = norm_pivot.index, columns = norm_pivot.index)
us_df = pd.DataFrame(user_similarity, index = norm_pivot.columns, columns = norm_pivot.columns)

def find_id(title):
    id = int(match_df[match_df['title'] == title].movieId)
    return id

def find_title(id):
    title = match_df[match_df['movieId'] == id].title.values[0]
    return title

def similar_5movies(id):
    if type(id) != int:
        id = find_id(id)
    title = find_title(id)
    movie_list = []
    top_five = is_df[id].sort_values(ascending = False)[1:6] #[0] = movie
    for item, score in top_five.items():
        movie_list.append(item)
    print(f'Similar 5 movies to \'id({id}) = {title}\' : {movie_list}\n')
    return movie_list

def similar_5movies_print(title):
    movie = find_id(title)
    num = 1
    print(f'Similar 5 movies to \'{title}\' :\n')
    top_five = is_df[movie].sort_values(ascending = False)[1:6] #[0] = movie
    print('top5', top_five)
    print('datatype', type(top_five))
    for item, score in top_five.items():
        title = find_title(item)
        print(f'No.{num} : \'{title}\' (Similarity score : {score})')
        num += 1

def similar_5users(user):
    if user not in norm_pivot.columns:
        return('No data of user {}'.format(user))
    print('Most 5 similar users : \n')
    top_five = us_df.sort_values(by = user, ascending = False).loc[:, user][1:6]

    for user, similarity in top_five.items():
        print(f'UserId : {user} => Similarity : {similarity}')

def recom_5movie(user):
    similar_30users = us_df.sort_values(by = user, ascending = False).index[1:31]
    movie_list = []
    recom = {}
    num = 0
    
    for i in similar_30users:
        movies = norm_pivot.loc[:, i][(norm_pivot.loc[:, user] == 0)].sort_values(ascending = False).index[:5]
        movie_list.append(movies.tolist())
    
    for i in range(len(movie_list)):
        for j in movie_list[i]:
            if j in recom:
                num += 1
            else:
                num = 1
            recom[j] = num
    five_movies = sorted(recom.items(), key = lambda x:x[1], reverse = True)[:5]
    return list(dict(five_movies)) # [movieId1, movieId2, ...]
        
        
def recom_5movie_print(user):
    similar_30users = us_df.sort_values(by = user, ascending = False).index[1:31]
    movie_list = []
    recom = {}
    num = 0
    
    for i in similar_30users:
        movies = norm_pivot.loc[:, i][(norm_pivot.loc[:, user] == 0)].sort_values(ascending = False).index[:5]
        movie_list.append(movies.tolist())
    
    for i in range(len(movie_list)):
        for j in movie_list[i]:
            if j in recom:
                num += 1
            else:
                num = 1
            recom[j] = num
    five_movies = sorted(recom.items(), key = lambda x:x[1], reverse = True)[:5]
    for i in five_movies:
        print('The movie \'{}\' (No. of recommenders : {})'.format(find_title(int(i[0])), i[1]))

if __name__ == '__main__':
    similar_5movies('Dirty Dancing (1987)')
