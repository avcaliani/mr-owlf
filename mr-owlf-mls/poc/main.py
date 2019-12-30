import pandas as pd
from pandas import DataFrame

import service.data.utils as data
import service.ai.utils as ai
import service.ai.modeling as modeling


THE_ONION = f'\033[1;32;40m[r/The Onion]\033[0m'
NOT_THE_ONION = f'\033[1;31;40m[r/Not The Onion]\033[0m'
AI = f'\033[1;35;40m[AI]\033[0m'
ME = f'\033[1;36;40m[ANTHONY]\033[0m'


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

df = pd.concat([df_onion[['subreddit', 'title']],
                df_not_onion[['subreddit', 'title']]], axis=0)
print(f'Combined DF shape: {df.shape}\n')
print(f'Combined DF Sample...\n{df.head(2)}\n...\n{df.tail(2)}\n\n')

df = df.reset_index(drop=True)  # Reset the index
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
onion_cvec_df: DataFrame = ai.count_vectorizer(
    df, filter_value=1, ngram_range=(2, 2))

print(f'\n{NOT_THE_ONION}')
not_onion_cvec_df: DataFrame = ai.count_vectorizer(
    df, filter_value=0, ngram_range=(2, 2))

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
    ], columns=['title']
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
