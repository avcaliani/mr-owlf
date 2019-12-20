# Basic libraries
import numpy as np
import pandas as pd
from pandas import DataFrame

# Natural Language Processing
from sklearn.feature_extraction import stop_words
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Modeling
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix


#   ____ ____ ____  
#  / ___/ ___/ ___| 
# | |   \___ \___ \ 
# | |___ ___) |__) |
#  \____|____/____/ 

# Foreground
blue       = lambda v: f'\033[1;34;40m{v}\033[0m'
cyan       = lambda v: f'\033[1;36;40m{v}\033[0m'
gray       = lambda v: f'\033[1;30;40m{v}\033[0m'
green      = lambda v: f'\033[1;32;40m{v}\033[0m'
magenta    = lambda v: f'\033[1;35;40m{v}\033[0m'
red        = lambda v: f'\033[1;31;40m{v}\033[0m'
white      = lambda v: f'\033[1;37;40m{v}\033[0m'
yellow     = lambda v: f'\033[1;33;40m{v}\033[0m'

__the_onion     = lambda v: print(f'{green("r/The Onion    ")}\t{v}')
__not_the_onion = lambda v: print(f'{red("r/Not The Onion")  }\t{v}')
__both          = lambda v: print(f'{blue("[Both]")          }\t{v}')
__ai            = lambda v: print(f'{magenta("[AI]")         }\t{v}')
__me            = lambda v: print(f'{cyan("[Anthony]")       }\t{v}')



#  ____          _             _____                      _    _                    
# |  _ \   __ _ | |_   __ _   |  ___| _   _  _ __    ___ | |_ (_)  ___   _ __   ___ 
# | | | | / _` || __| / _` |  | |_   | | | || '_ \  / __|| __|| | / _ \ | '_ \ / __|
# | |_| || (_| || |_ | (_| |  |  _|  | |_| || | | || (__ | |_ | || (_) || | | |\__ \
# |____/  \__,_| \__| \__,_|  |_|     \__,_||_| |_| \___| \__||_| \___/ |_| |_||___/
#
def clean_data(dataframe):
    # Drop duplicate rows
    dataframe.drop_duplicates(subset='title', inplace=True)    
    # Remove punctation
    dataframe['title'] = dataframe['title'].str.replace('[^\w\s]',' ')
    # Remove numbers 
    dataframe['title'] = dataframe['title'].str.replace('[^A-Za-z]',' ')
    # Make sure any double-spaces are single 
    dataframe['title'] = dataframe['title'].str.replace('  ',' ')
    dataframe['title'] = dataframe['title'].str.replace('  ',' ')
    # Transform all text to lowercase
    dataframe['title'] = dataframe['title'].str.lower()
    
    print("New shape:", dataframe.shape)



print("""
          __               _    _    _                          _               
 _ __    / / _ __    ___  | |_ | |_ | |__    ___   ___   _ __  (_)  ___   _ __  
| '__|  / / | '_ \  / _ \ | __|| __|| '_ \  / _ \ / _ \ | '_ \ | | / _ \ | '_ \ 
| |    / /  | | | || (_) || |_ | |_ | | | ||  __/| (_) || | | || || (_) || | | |
|_|   /_/   |_| |_| \___/  \__| \__||_| |_| \___| \___/ |_| |_||_| \___/ |_| |_|
""")

df_not_onion: DataFrame = pd.read_csv('data/not-the-onion.csv')
__not_the_onion(f'shape: {df_not_onion.shape}')

clean_data(df_not_onion)
__not_the_onion(f'\n{df_not_onion.head()}\n...\n{df_not_onion.tail()}\n\n')



print("""
          __ _____  _             ___          _               
 _ __    / /|_   _|| |__    ___  / _ \  _ __  (_)  ___   _ __  
| '__|  / /   | |  | '_ \  / _ \| | | || '_ \ | | / _ \ | '_ \ 
| |    / /    | |  | | | ||  __/| |_| || | | || || (_) || | | |
|_|   /_/     |_|  |_| |_| \___| \___/ |_| |_||_| \___/ |_| |_|
""")

df_onion = pd.read_csv('data/the-onion.csv')
__the_onion(f'shape: {df_onion.shape}')

clean_data(df_onion)
__the_onion(f'\n{df_onion.head()}\n...\n{df_onion.tail()}\n\n')


# 
# (╯°□°）╯︵ ┻━┻
# Is there any null values?
#
__the_onion(f'(before) shape:\t{df_onion.shape}')
__not_the_onion(f'(before) shape:\t{df_not_onion.shape}')
DataFrame([df_onion.isnull().sum(), df_not_onion.isnull().sum()], index=["TheOnion","notheonion"]).T

# 
# Let's clean them up!
#
df_onion.dropna(inplace=True)
df_not_onion.dropna(inplace=True)
__the_onion(f'(after) shape:\t{df_onion.shape}')
__not_the_onion(f'(after) shape:\t{df_not_onion.shape}')
DataFrame([df_onion.isnull().sum(), df_not_onion.isnull().sum()], index=["TheOnion","notheonion"]).T



print("""
 .----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. |
| |  _________   | || |  ________    | || |      __      | |
| | |_   ___  |  | || | |_   ___ `.  | || |     /  \     | |
| |   | |_  \_|  | || |   | |   `. \ | || |    / /\ \    | |
| |   |  _|  _   | || |   | |    | | | || |   / ____ \   | |
| |  _| |___/ |  | || |  _| |___.' / | || | _/ /    \ \_ | |
| | |_________|  | || | |________.'  | || ||____|  |____|| |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'
                                   Exploratory Data Analysis
""")
# Convert Unix Timestamp to Datetime
df_onion['timestamp'] = pd.to_datetime(df_onion['timestamp'], unit='s')
df_not_onion['timestamp'] = pd.to_datetime(df_not_onion['timestamp'], unit='s')

# Show date-range of posts scraped from r/TheOnion and r/nottheonion
__the_onion(f"start date:\t{df_onion['timestamp'].min()}")
__the_onion(f"end date:\t{df_onion['timestamp'].max()}")
__not_the_onion(f"start date:\t{df_not_onion['timestamp'].min()}")
__not_the_onion(f"end date:\t{df_not_onion['timestamp'].max()}")



print("""
          __ _____  _             ___          _               
 _ __    / /|_   _|| |__    ___  / _ \  _ __  (_)  ___   _ __  
| '__|  / /   | |  | '_ \  / _ \| | | || '_ \ | | / _ \ | '_ \ 
| |    / /    | |  | | | ||  __/| |_| || | | || || (_) || | | |
|_|   /_/     |_|  |_| |_| \___| \___/ |_| |_||_| \___/ |_| |_|

------------------------------------------------------------------------------
 Most Active Authors
------------------------------------------------------------------------------
""")
# Set x values: # of posts 
df_onion_authors = df_onion['author'].value_counts() 
df_onion_authors: DataFrame = df_onion_authors[df_onion_authors > 100].sort_values(ascending=False)
__the_onion(f'Authors...\n{df_onion_authors.head()}\n...\n{df_onion_authors.tail()}\n\n')

  
print("""
------------------------------------------------------------------------------
 Most Referenced Domains
------------------------------------------------------------------------------
""")
# Set x values: # of posts
df_onion_domain = df_onion['domain'].value_counts() 
df_onion_domain = df_onion_domain.sort_values(ascending=False).head(5)
__the_onion(f'Domains...\n{df_onion_domain.head()}\n...\n{df_onion_domain.tail()}\n\n')



print("""
          __               _    _    _                          _               
 _ __    / / _ __    ___  | |_ | |_ | |__    ___   ___   _ __  (_)  ___   _ __  
| '__|  / / | '_ \  / _ \ | __|| __|| '_ \  / _ \ / _ \ | '_ \ | | / _ \ | '_ \ 
| |    / /  | | | || (_) || |_ | |_ | | | ||  __/| (_) || | | || || (_) || | | |
|_|   /_/   |_| |_| \___/  \__| \__||_| |_| \___| \___/ |_| |_||_| \___/ |_| |_|

------------------------------------------------------------------------------
 Most Active Authors
------------------------------------------------------------------------------
""")
# Set x values: # of posts
df_not_onion_authors = df_not_onion['author'].value_counts() 
df_not_onion_authors = df_not_onion_authors[df_not_onion_authors > 100].sort_values(ascending=False)
__not_the_onion(f'Authors...\n{df_not_onion_authors.head()}\n...\n{df_not_onion_authors.tail()}\n\n')


print("""
------------------------------------------------------------------------------
 Most Referenced Domains
------------------------------------------------------------------------------
""")
# Set x values: # of posts greater than 100
df_nonion_domain = df_not_onion['domain'].value_counts() 
df_nonion_domain = df_nonion_domain.sort_values(ascending=False).head(5)
__not_the_onion(f'Domains...\n{df_nonion_domain.head()}\n...\n{df_nonion_domain.tail()}\n\n')



print("""
 .-----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. |
| | ____  _____  | || |   _____      | || |   ______     | |
| ||_   \|_   _| | || |  |_   _|     | || |  |_   __ \   | |
| |  |   \ | |   | || |    | |       | || |    | |__) |  | |
| |  | |\ \| |   | || |    | |   _   | || |    |  ___/   | |
| | _| |_\   |_  | || |   _| |__/ |  | || |   _| |_      | |
| ||_____|\____| | || |  |________|  | || |  |_____|     | |
| |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'
                                 Natural Language Processing
""")
# Combine df_onion & df_not_onion with only 'subreddit' (target) and 'title' (predictor) columns
df = pd.concat([
  df_onion[['subreddit', 'title']],
  df_not_onion[['subreddit', 'title']]
], axis=0)
__both(f'Combined DF shape: {df.shape}')
__both(f'Combined DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}\n\n')

# Reset the index
df = df.reset_index(drop=True)
# Replace `TheOnion` with 1, `nottheonion` with 0
df["subreddit"] = df["subreddit"].map({"nottheonion": 0, "TheOnion": 1})
__both(f'Prepared DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}')



print("""
  ____                       _    __     __             _                 _            
 / ___|  ___   _   _  _ __  | |_  \ \   / /  ___   ___ | |_   ___   _ __ (_) ____  ___ 
| |     / _ \ | | | || '_ \ | __|  \ \ / /  / _ \ / __|| __| / _ \ | '__|| ||_  / / _ \\
| |___ | (_) || |_| || | | || |_    \ V /  |  __/| (__ | |_ | (_) || |   | | / / |  __/
 \____| \___/  \__,_||_| |_| \__|    \_/    \___| \___| \__| \___/ |_|   |_|/___| \___|
                          ngram_range = (1,1)

------------------------------------------------------------------------------
 TheOnion
------------------------------------------------------------------------------
""")
# Set variables to show TheOnion Titles
mask_on = df['subreddit'] == 1
df_onion_titles = df[mask_on]['title']

# Instantiate a CountVectorizer
cv1 = CountVectorizer(stop_words = 'english')

# Fit and transform the vectorizer on our corpus
onion_cvec = cv1.fit_transform(df_onion_titles)

# Convert onion_cvec into a DataFrame
onion_cvec_df = DataFrame(
    onion_cvec.toarray(),
    columns=cv1.get_feature_names()
)

# Inspect head of Onion Titles cvec
__the_onion(f'The Onion: {onion_cvec_df.shape}')


print("""
------------------------------------------------------------------------------
 NotTheOnion
------------------------------------------------------------------------------
""")
# Set variables to show NotTheOnion Titles
mask_no = df['subreddit'] == 0
df_not_onion_titles = df[mask_no]['title']

# Instantiate a CountVectorizer
cv2 = CountVectorizer(stop_words = 'english')

# Fit and transform the vectorizer on our corpus
not_onion_cvec = cv2.fit_transform(df_not_onion_titles)

# Convert onion_cvec into a DataFrame
not_onion_cvec_df = DataFrame(
    not_onion_cvec.toarray(),
    columns=cv2.get_feature_names()
)

# Inspect head of Not Onion Titles cvec
__not_the_onion(f'Not The Onion: {not_onion_cvec_df.shape}')



print("""
 _   _         _                                     
| | | | _ __  (_)  __ _  _ __   __ _  _ __ ___   ___ 
| | | || '_ \ | | / _` || '__| / _` || '_ ` _ \ / __|
| |_| || | | || || (_| || |   | (_| || | | | | |\__ \\
 \___/ |_| |_||_| \__, ||_|    \__,_||_| |_| |_||___/
                  |___/                              

------------------------------------------------------------------------------
 TheOnion
------------------------------------------------------------------------------
""")
# Set up variables to contain top 5 most used words in Onion
onion_wc = onion_cvec_df.sum(axis = 0)
onion_top_5 = onion_wc.sort_values(ascending=False).head(5)
__the_onion(onion_top_5)


print("""
------------------------------------------------------------------------------
 NotTheOnion
------------------------------------------------------------------------------
""")
# Set up variables to contain top 5 most used words in r/nottheonion
nonion_wc = not_onion_cvec_df.sum(axis = 0)
nonion_top_5 = nonion_wc.sort_values(ascending=False).head(5)
__not_the_onion(nonion_top_5)


print("""
------------------------------------------------------------------------------
 TheOnion x NotTheOnion
------------------------------------------------------------------------------
""")
# Top 5 Bigrams: Create list of unique words in top five
not_onion_5_set = set(nonion_top_5.index)
onion_5_set = set(onion_top_5.index)

# Return common words
common_unigrams = onion_5_set.intersection(not_onion_5_set)
__both(common_unigrams)



print("""
  ____                       _    __     __             _                 _            
 / ___|  ___   _   _  _ __  | |_  \ \   / /  ___   ___ | |_   ___   _ __ (_) ____  ___ 
| |     / _ \ | | | || '_ \ | __|  \ \ / /  / _ \ / __|| __| / _ \ | '__|| ||_  / / _ \\
| |___ | (_) || |_| || | | || |_    \ V /  |  __/| (__ | |_ | (_) || |   | | / / |  __/
 \____| \___/  \__,_||_| |_| \__|    \_/    \___| \___| \__| \___/ |_|   |_|/___| \___|
                          ngram_range = (2,2)

------------------------------------------------------------------------------
 TheOnion
------------------------------------------------------------------------------
""")
# Set variables to show TheOnion Titles
mask = df['subreddit'] == 1
df_onion_titles = df[mask]['title']

# Instantiate a CountVectorizer
cv = CountVectorizer(stop_words = 'english', ngram_range=(2,2))

# Fit and transform the vectorizer on our corpus
onion_cvec = cv.fit_transform(df_onion_titles)

# Convert onion_cvec into a DataFrame
onion_cvec_df = DataFrame(
    onion_cvec.toarray(),
    columns=cv.get_feature_names()
)

# Inspect head of Onion Titles cvec
__the_onion(onion_cvec_df.shape)


print("""
------------------------------------------------------------------------------
 NotTheOnion
------------------------------------------------------------------------------
""")
# Set variables to show NotTheOnion Titles
mask = df['subreddit'] == 0
df_not_onion_titles = df[mask]['title']

# Instantiate a CountVectorizer
cv = CountVectorizer(stop_words = 'english', ngram_range=(2,2))

# Fit and transform the vectorizer on our corpus
not_onion_cvec = cv.fit_transform(df_not_onion_titles)

# Convert onion_cvec into a DataFrame
not_onion_cvec_df = DataFrame(
    not_onion_cvec.toarray(),
    columns=cv.get_feature_names()
)

# Inspect head of Not Onion Titles cvec
__not_the_onion(not_onion_cvec_df.shape)



print("""
 ____   _                                     
| __ ) (_)  __ _  _ __   __ _  _ __ ___   ___ 
|  _ \ | | / _` || '__| / _` || '_ ` _ \ / __|
| |_) || || (_| || |   | (_| || | | | | |\__ \\
|____/ |_| \__, ||_|    \__,_||_| |_| |_||___/
           |___/

------------------------------------------------------------------------------
 TheOnion
------------------------------------------------------------------------------
""")
# Set up variables to contain top 5 most used bigrams in r/TheOnion
onion_wc = onion_cvec_df.sum(axis = 0)
onion_top_5 = onion_wc.sort_values(ascending=False).head(5)
__the_onion(onion_top_5)


print("""
------------------------------------------------------------------------------
 NotTheOnion
------------------------------------------------------------------------------
""")
# Set up variables to contain top 5 most used bigrams in r/nottheonion
nonion_wc = not_onion_cvec_df.sum(axis = 0)
nonion_top_5 = nonion_wc.sort_values(ascending=False).head(5)
__not_the_onion(nonion_top_5)


print("""
------------------------------------------------------------------------------
 TheOnion x NotTheOnion
------------------------------------------------------------------------------
""")
# Common Bigrams between Top 5 in r/TheOnion & r/nottheonion
not_onion_5_list = set(nonion_top_5.index)
onion_5_list = set(onion_top_5.index)

# Return common words
common_bigrams = onion_5_list.intersection(not_onion_5_list)
__both(common_bigrams)


# Take out {'man', 'new', 'old', 'people', 'say', 'trump', 'woman', 'year'}
# from dataset when modeling, since these words occur frequently in both subreddits.

print("""
 ____   _                  __        __                  _      
/ ___| | |_   ___   _ __   \ \      / /  ___   _ __   __| | ___ 
\___ \ | __| / _ \ | '_ \   \ \ /\ / /  / _ \ | '__| / _` |/ __|
 ___) || |_ | (_) || |_) |   \ V  V /  | (_) || |   | (_| |\__ \\
|____/  \__| \___/ | .__/     \_/\_/    \___/ |_|    \__,_||___/
                   |_|                                          
Create custom stop_words to include common frequent words
Referencing the common most-used words, add them to a customized stop_words list.
""")
# Create lists 
custom = stop_words.ENGLISH_STOP_WORDS
custom = list(custom)
common_unigrams = list(common_unigrams)
common_bigrams = list(common_bigrams)

# Append unigrams to list 
for i in common_unigrams:
    custom.append(i)

    
# Append bigrams to list 
for i in common_bigrams:
    split_words = i.split(" ")
    for word in split_words:
        custom.append(word)



print("""
 __  __             _        _  _               
|  \/  |  ___    __| |  ___ | |(_) _ __    __ _ 
| |\/| | / _ \  / _` | / _ \| || || '_ \  / _` |
| |  | || (_) || (_| ||  __/| || || | | || (_| |
|_|  |_| \___/  \__,_| \___||_||_||_| |_| \__, |
                                          |___/ 
Baseline score
""")
df['subreddit'].value_counts(normalize=True)
# I expect my model to be better than 54%.
# The majority class is 1, or, TheOnion.
# If the model is not better than 54%, I know the model is not performing well.

X = df['title']
y = df['subreddit']
# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, stratify=y)

#
# Model 1: CountVectorizer & Logistic Regression (Best Coefficient Interpretability)
#
# TODO: Study!
pipe = Pipeline([
  ('cvec', CountVectorizer()),    
  ('lr', LogisticRegression(solver='liblinear'))
])

# Tune GridSearchCV
pipe_params = {
  'cvec__stop_words': [None, 'english', custom],
  'cvec__ngram_range': [(1,1), (2,2), (1,3)],
  'lr__C': [0.01, 1]
}

gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
gs.fit(X_train, y_train)
print("\n")
__ai("Grid Search (CountVectorizer, LogisticRegression)")
__ai(f"Best score  : {gs.best_score_}")
__ai(f"Train score : {gs.score(X_train, y_train)}")
__ai(f"Test score  : {gs.score(X_test, y_test)}")

gs.best_params_
#
# Throughout my model testing, none of the stop_word lists were chosen as 
# a best parameter.
# So from here on out, I omit them from my parameter selection.
# Additionally, while the model is overfit, I am optimizing to get the 
# highest accuracy score in my test set.
#

#
# Model 2: TfidfVectorize & Logistic Regression
#
# TODO: Study!
pipe = Pipeline([
  ('tvect', TfidfVectorizer()),    
  ('lr', LogisticRegression(solver='liblinear'))
])

# Tune GridSearchCV
pipe_params = {
  'tvect__max_df': [.75, .98, 1.0],
  'tvect__min_df': [2, 3, 5],
  'tvect__ngram_range': [(1,1), (1,2), (1,3)],
  'lr__C': [1]
}

gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
gs.fit(X_train, y_train)
print("\n")
__ai("Grid Search (TfidfVectorizer, LogisticRegression)")
__ai(f"Best score  : {gs.best_score_}")
__ai(f"Train score : {gs.score(X_train, y_train)}")
__ai(f"Test score  : {gs.score(X_test, y_test)}")

gs.best_params_
# This model is also overfit.
# However, Model 1 performed with a better test score when comparing
# Logistic Regression models.

#
# Model 3: CountVectorizer & MultinomialNB (Best Accuracy Score)
#
# TODO: Study!
pipe = Pipeline([
  ('cvec', CountVectorizer()),    
  ('nb', MultinomialNB())
])

# Tune GridSearchCV
pipe_params = {
  'cvec__ngram_range': [(1,1),(1,3)],
  'nb__alpha': [.36, .6]
}

gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
gs.fit(X_train, y_train)
print("\n")
__ai("Grid Search (CountVectorizer, MultinomialNB)")
__ai(f"Best score  : {gs.best_score_}")
__ai(f"Train score : {gs.score(X_train, y_train)}")
__ai(f"Test score  : {gs.score(X_test, y_test)}")

gs.best_params_
# The model is overfit, but as I mentioned, I am optimizing for accuracy.
# I want to ensure that all predictions are correct.
# That is, all posts from r/TheOnion must be classified as being from the subreddit r/TheOnion,
# and all posts from r/nottheonion must be classified as being from the subreddit r/nottheonion.
# This model gave me my best test accuracy score.

#
# Model 4: TfidfVectorizer & MultinomialNB
#
# TODO: Study!
pipe = Pipeline([
  ('tvect', TfidfVectorizer()),    
  ('nb', MultinomialNB())
])

# Tune GridSearchCV
pipe_params = {
  'tvect__max_df': [.75, .98],
  'tvect__min_df': [4, 5],
  'tvect__ngram_range': [(1,2), (1,3)],
  'nb__alpha': [0.1, 1]
}

gs = GridSearchCV(pipe, param_grid=pipe_params, cv=5)
gs.fit(X_train, y_train)
print("\n")
__ai("Grid Search (TfidfVectorizer, MultinomialNB)")
__ai(f"Best score  : {gs.best_score_}")
__ai(f"Train score : {gs.score(X_train, y_train)}")
__ai(f"Test score  : {gs.score(X_test, y_test)}")

gs.best_params_
# This model is overfit.
# When comparing test scores of my MultinomialNB models, Model 3 performs better.

#
# Best Models
#
# In this section, I take my two optimal models and run them.
# The first model, CountVectorizer & MultinomialNB, will be used to convey a
# confusion matrix which will show all evaluation scores.
# The second model, CountVectorizer & Logistic Regression, will be used to 
# interpret my coefficients.

# TODO: Study!
#
# CountVectorizer & MultinomialNB: Best Score
#

#Instantiate the classifier and vectorizer
nb = MultinomialNB(alpha = 0.36)
cvec = CountVectorizer(ngram_range= (1, 3))

# Fit and transform the vectorizor
cvec.fit(X_train)

Xcvec_train = cvec.transform(X_train)
Xcvec_test = cvec.transform(X_test)

# Fit the classifier
nb.fit(Xcvec_train,y_train)

# Create the predictions for Y training data
preds = nb.predict(Xcvec_test)

print("\n")
__ai("MultinomialNB")
__ai(nb.score(Xcvec_test, y_test))

# Create a confusion matrix
cnf_matrix = metrics.confusion_matrix(y_test, preds)
print("\n")
__ai(f"Confusion Matrix\n{confusion_matrix}")

# Code from https://www.datacamp.com/community/tutorials/understanding-logistic-regression-python
# name  of classes
class_names=[0,1] 

cnf_matrix = np.array(cnf_matrix).tolist()

tn_fp, fn_tp = cnf_matrix

tn, fp = tn_fp
fn, tp = fn_tp

print("\n")
__ai("MultinomialNB")
__ai(f"Accuracy              : {round(metrics.accuracy_score(y_test, preds)*100, 2)}%")
__ai(f"Precision             : {round(metrics.precision_score(y_test, preds)*100, 2)}%")
__ai(f"Recall                : {round(metrics.recall_score(y_test, preds)*100, 2)}%")
__ai(f"Specificity           : {round((tn/(tn+fp))*100, 2)}%")
__ai(f"Misclassification Rate: {round((fp+fn)/(tn+fp+fn+tn)*100, 2)}%")

# TODO: Study!
#
# CountVectorizer & Logistic Regression: Best Coefficient Interpretability
#

# Customize stop_words to include `onion` so that it doesn't appear
# in coefficients 

stop_words_onion = stop_words.ENGLISH_STOP_WORDS
stop_words_onion = list(stop_words_onion)
stop_words_onion.append('onion')

#Instantiate the classifier and vectorizer
lr = LogisticRegression(C = 1.0, solver='liblinear')
cvec2 = CountVectorizer(stop_words = stop_words_onion)

# Fit and transform the vectorizor
cvec2.fit(X_train)

Xcvec2_train = cvec2.transform(X_train)
Xcvec2_test = cvec2.transform(X_test)

# Fit the classifier
lr.fit(Xcvec2_train,y_train)

# Create the predictions for Y training data
lr_preds = lr.predict(Xcvec2_test)

print("\n")
__ai("LogisticRegression")
__ai(lr.score(Xcvec2_test, y_test))

#
# Coefficient Analysis
# 
# Create list of logistic regression coefficients 
lr_coef = np.array(lr.coef_).tolist()
lr_coef = lr_coef[0]

# create dataframe from lasso coef
lr_coef = pd.DataFrame(np.round_(lr_coef, decimals=3), 
cvec2.get_feature_names(), columns = ["penalized_regression_coefficients"])

# sort the values from high to low
lr_coef = lr_coef.sort_values(by = 'penalized_regression_coefficients', ascending = False)

# Jasmine changing things up here on out! Top half not mine. 
# create best and worst performing lasso coef dataframes
df_head = lr_coef.head(10)
df_tail = lr_coef.tail(10)

# merge back together
df_merged = pd.concat([df_head, df_tail], axis=0)


print("\n")
__ai(f"The word that contributes the most positively to being from r/TheOnion is '{df_merged.index[0]}' followed by '{df_merged.index[1]}' and '{df_merged.index[2]}'.")
__ai("-----------------------------------")
__ai(f"The word that contributes the most positively to being from r/nottheonion is'{df_merged.index[-1]}' followed by '{df_merged.index[-2]}' and '{df_merged.index[-3]}'.")

# Show coefficients that affect r/TheOnion
df_merged_head = df_merged.head(10)
exp = df_merged_head['penalized_regression_coefficients'].apply(lambda x: np.exp(x))
df_merged_head.insert(1, 'exp', exp)
df_merged_head.sort_values('exp', ascending=False)

__ai(f"As occurences of '{df_merged_head.index[0]}' increase by 1 in a title, that title is '{round(df_merged_head['exp'][0],2)}' times as likely to be classified as r/TheOnion.")

# Show coefficients that affect r/nottheonion
df_merged_tail = df_merged.tail(10)
exp = df_merged_tail['penalized_regression_coefficients'].apply(lambda x: np.exp(x * -1))
df_merged_tail.insert(1, 'exp', exp)
df_merged_tail.sort_values('exp', ascending=False)

__ai(f"As occurences of '{df_merged_tail.index[-1]} increase by 1 in a title, that title is {round(df_merged_tail['exp'][-1],2)} times as likely to be classified as r/nottheonion.")

# Conclusions and Next-Steps
# The most model to optimize for accuracy in detecting fake news and absurd news
# uses CountVectorizer and MultinomialDB. The optimal parameters for this model 
# are where ngram_range = (1,3) and alpha = 0.36.

# Accuracy: 89.72%
# Precision: 90.87%
# Recall: 90.02%
# Specificity: 89.38%
# Misclassification Rate: 11.11%
# To interpret my coefficients, I used my CountVectorizer & Logistic Regression model.

# The word that contributes the most positively to being from r/TheOnion is 
# 'incredible' followed by 'questions' and 'heartbreaking'.
# As occurences of "incredible" increase by 1 in a title, that title is 10.32 times
# as likely to be classified as r/TheOnion.
# The word that contributes the most positively to being from r/nottheonion 
# is 'australia' followed by 'title' and 'florida'.
# As occurences of "australia" increase by 1 in a title, that title is 15.03 times 
# as likely to be classified as r/nottheonion.
# Natural Language Processing of text is one way to analyze fake news, but a 
# major gap exists: image & video analysis. For my next-steps, I am interested 
# in being able to interpret media (images and videos) and classify them as 
# authentic news, fake news, or none of the above (i.e., media for entertainment).

print("""
    _     _   _  _____  _   _   ___   _   _ __   __
   / \   | \ | ||_   _|| | | | / _ \ | \ | |\ \ / /
  / _ \  |  \| |  | |  | |_| || | | ||  \| | \ V / 
 / ___ \ | |\  |  | |  |  _  || |_| || |\  |  | |  
/_/   \_\|_| \_|  |_|  |_| |_| \___/ |_| \_|  |_|  
""")
__me("My Test")
_my_data = pd.DataFrame(
  [
      'San Diego backyard shed rents for $1,050 a month',
      'Are You The Whistleblower? Trump Boys Ask White House Janitor After Giving Him Serum Of All The Sodas Mixed Together',
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at diam ac orci pharetra scelerisque non sit amet turpis. Donec quis erat quam',
      '12356487984158641351568463213851684132168461'
  ], columns = ['title']
)
__me(_my_data.shape)

_my_data_cvec = cvec.transform(_my_data['title'])
__me(_my_data_cvec.shape)

_preds = nb.predict(_my_data_cvec)
_preds_prob = nb.predict_proba(_my_data_cvec)
__me(_preds)
__me(_preds_prob)

__me(f'+\tThe Onion\tNot The Onion')
for i in range(0, len(_preds_prob)):
  nto = '{0:.2f}'.format(_preds_prob[i][0])
  to = '{0:.2f}'.format(_preds_prob[i][1])
  __me(f'{i}\t{to}\t\t{ nto }')
