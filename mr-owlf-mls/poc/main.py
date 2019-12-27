import pandas as pd
from pandas import DataFrame

import service.data.utils as data
import service.ai.utils as ai
import service.ai.modeling as modeling


THE_ONION     = f'\033[1;32;40m[r/The Onion]\033[0m'
NOT_THE_ONION = f'\033[1;31;40m[r/Not The Onion]\033[0m'
AI            = f'\033[1;35;40m[AI]\033[0m'
ME            = f'\033[1;36;40m[ANTHONY]\033[0m'


# Not The Onion
print(f'\n{NOT_THE_ONION}')
df_not_onion: DataFrame = data.read('data/not-the-onion.csv')
data.clean_data(df_not_onion)
data.show_statistics(df_not_onion)

# The Onion
print(f'\n{THE_ONION}')
df_onion: DataFrame = data.read('data/the-onion.csv')
data.clean_data(df_onion)
data.show_statistics(df_onion)

# Combine df_onion & df_not_onion with only 'subreddit' (target) and 'title' (predictor) columns
print(f'\n{THE_ONION} {NOT_THE_ONION} {"[Natural Language Processing]"}')

df = pd.concat([ df_onion[['subreddit', 'title']], df_not_onion[['subreddit', 'title']] ], axis=0)
print(f'Combined DF shape: {df.shape}\n')
print(f'Combined DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}\n\n')

df = df.reset_index(drop=True) # Reset the index
df["subreddit"] = df["subreddit"].map({"nottheonion": 0, "TheOnion": 1})
print(f'Prepared DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}')



# Count Vectorize - ngram_range = (1,1)
print(f'\n{THE_ONION}')
onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=1)

print(f'\n{NOT_THE_ONION}')
not_onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=0)

# Unigrams
print(f'\n{THE_ONION} {NOT_THE_ONION}')
common_unigrams = list(ai.unigrams(onion_cvec_df, not_onion_cvec_df))



# Count Vectorize - ngram_range = (2,2)
print(f'\n{THE_ONION}')
onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=1, ngram_range=(2, 2))

print(f'\n{NOT_THE_ONION}')
not_onion_cvec_df: DataFrame = ai.count_vectorizer(df, filter_value=0, ngram_range=(2, 2))

# Bigrams
print(f'\n{THE_ONION} {NOT_THE_ONION}')
common_bigrams = list(ai.unigrams(onion_cvec_df, not_onion_cvec_df))



# Stop Words
# ------------------
# Take out {'man', 'new', 'old', 'people', 'say', 'trump', 'woman', 'year'}
# from dataset when modeling, since these words occur frequently in both subreddits.
print(f'\n{THE_ONION} {NOT_THE_ONION}')
custom = ai.get_stop_words(common_unigrams, common_bigrams)


print(f'\n{THE_ONION} {NOT_THE_ONION} [Starting try out...]')
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

print(f'\n{THE_ONION} {NOT_THE_ONION}')
clf_nb, cv_nb = modeling.naive_bayes(df, custom)

print(f'\n{THE_ONION} {NOT_THE_ONION}')
clf_lr, cv_lr = modeling.logistic_regression(df, custom)

# # TODO: Split it up
# # Coefficient Analysis
# # 
# # Create list of logistic regression coefficients 
# lr_coef = np.array(lr.coef_).tolist()
# lr_coef = lr_coef[0]

# # create dataframe from lasso coef
# lr_coef = pd.DataFrame(np.round_(lr_coef, decimals=3), 
# cvec2.get_feature_names(), columns = ["penalized_regression_coefficients"])

# # sort the values from high to low
# lr_coef = lr_coef.sort_values(by = 'penalized_regression_coefficients', ascending = False)

# # Jasmine changing things up here on out! Top half not mine. 
# # create best and worst performing lasso coef dataframes
# df_head = lr_coef.head(10)
# df_tail = lr_coef.tail(10)

# # merge back together
# df_merged = pd.concat([df_head, df_tail], axis=0)


# print("\n")
# __ai(f"The word that contributes the most positively to being from r/TheOnion is '{df_merged.index[0]}' followed by '{df_merged.index[1]}' and '{df_merged.index[2]}'.")
# __ai("-----------------------------------")
# __ai(f"The word that contributes the most positively to being from r/nottheonion is'{df_merged.index[-1]}' followed by '{df_merged.index[-2]}' and '{df_merged.index[-3]}'.")

# # Show coefficients that affect r/TheOnion
# df_merged_head = df_merged.head(10)
# exp = df_merged_head['penalized_regression_coefficients'].apply(lambda x: np.exp(x))
# df_merged_head.insert(1, 'exp', exp)
# df_merged_head.sort_values('exp', ascending=False)

# __ai(f"As occurences of '{df_merged_head.index[0]}' increase by 1 in a title, that title is '{round(df_merged_head['exp'][0],2)}' times as likely to be classified as r/TheOnion.")

# # Show coefficients that affect r/nottheonion
# df_merged_tail = df_merged.tail(10)
# exp = df_merged_tail['penalized_regression_coefficients'].apply(lambda x: np.exp(x * -1))
# df_merged_tail.insert(1, 'exp', exp)
# df_merged_tail.sort_values('exp', ascending=False)

# __ai(f"As occurences of '{df_merged_tail.index[-1]} increase by 1 in a title, that title is {round(df_merged_tail['exp'][-1],2)} times as likely to be classified as r/nottheonion.")

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

# TODO: Split it up too
print(f'\n{ME}')
_my_data = DataFrame(
  [
      'San Diego backyard shed rents for $1,050 a month',
      'Are You The Whistleblower? Trump Boys Ask White House Janitor After Giving Him Serum Of All The Sodas Mixed Together',
      'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at diam ac orci pharetra scelerisque non sit amet turpis. Donec quis erat quam',
      '12356487984158641351568463213851684132168461'
  ], columns = ['title']
)
print(f'Shape: {_my_data.shape}')

_my_data_cvec = cv_nb.transform(_my_data['title'])
print(f'Shape: {_my_data_cvec.shape}')

_preds = clf_nb.predict(_my_data_cvec)
_preds_prob = clf_nb.predict_proba(_my_data_cvec)
print(_preds)
print(_preds_prob)

print(f'+\tThe Onion\tNot The Onion')
for i in range(0, len(_preds_prob)):
  nto = '{0:.2f}'.format(_preds_prob[i][0])
  to = '{0:.2f}'.format(_preds_prob[i][1])
  print(f'{i}\t{to}\t\t{ nto }')

# TODO: Future - Read data from Mongo
# TODO: Future - Create translator
# TODO: Future - Create score