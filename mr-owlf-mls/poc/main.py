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

import services.commons as commons
import ai
import ai_modeling as modeling


# Foreground
blue       = lambda v: f'\033[1;34;40m{v}\033[0m'
cyan       = lambda v: f'\033[1;36;40m{v}\033[0m'
gray       = lambda v: f'\033[1;30;40m{v}\033[0m'
green      = lambda v: f'\033[1;32;40m{v}\033[0m'
magenta    = lambda v: f'\033[1;35;40m{v}\033[0m'
red        = lambda v: f'\033[1;31;40m{v}\033[0m'
white      = lambda v: f'\033[1;37;40m{v}\033[0m'
yellow     = lambda v: f'\033[1;33;40m{v}\033[0m'


THE_ONION     = green("[r/The Onion]")
NOT_THE_ONION = red("[r/Not The Onion]")
AI            = magenta("[AI]")
ME            = cyan("[ANTHONY]")


# Not The Onion
print(f'\n{NOT_THE_ONION}')
df_not_onion: DataFrame = commons.read('data/not-the-onion.csv')
commons.clean_data(df_not_onion)
commons.show_statistics(df_not_onion)


# The Onion
print(f'\n{THE_ONION}')
df_onion: DataFrame = commons.read('data/the-onion.csv')
commons.clean_data(df_onion)
commons.show_statistics(df_onion)


# Join Data Frames
print(f'\n{THE_ONION} {NOT_THE_ONION} {yellow("[Natural Language Processing]")}')

# Combine df_onion & df_not_onion with only 'subreddit' (target) and 'title' (predictor) columns
df = pd.concat([
  df_onion[['subreddit', 'title']],
  df_not_onion[['subreddit', 'title']]
], axis=0)
print(f'Combined DF shape: {df.shape}')
print(f'Combined DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}\n\n')

# Reset the index
df = df.reset_index(drop=True)
# Replace `TheOnion` with 1, `nottheonion` with 0
df["subreddit"] = df["subreddit"].map({"nottheonion": 0, "TheOnion": 1})
print(f'Prepared DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}')



# Count Vectorize - ngram_range = (1,1)
print(f'\n{THE_ONION}')
onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=1)

print(f'\n{NOT_THE_ONION}')
not_onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=0)



# Unigrams
print(f'\n{THE_ONION} {NOT_THE_ONION}')
common_unigrams = ai.unigrams(onion_cvec_df, not_onion_cvec_df)



# Count Vectorize - ngram_range = (2,2)
print(f'\n{THE_ONION}')
onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=1, ngram_range=(2, 2))

print(f'\n{NOT_THE_ONION}')
not_onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=0, ngram_range=(2, 2))



# Bigrams
print(f'\n{THE_ONION} {NOT_THE_ONION}')
common_bigrams = ai.unigrams(onion_cvec_df, not_onion_cvec_df)



# Stop Words
# ------------------
# Take out {'man', 'new', 'old', 'people', 'say', 'trump', 'woman', 'year'}
# from dataset when modeling, since these words occur frequently in both subreddits.
print(f'\n{THE_ONION} {NOT_THE_ONION}')
custom = ai.get_stop_words(common_unigrams, common_bigrams)


# Modeling
modeling.try_out(df, custom)

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
