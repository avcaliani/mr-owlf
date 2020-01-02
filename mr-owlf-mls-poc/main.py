import pandas as pd
from pandas import DataFrame

import service.ai.modeling as modeling
from service.process import Process
import service.ai.utils as ai
import service.data.utils as data

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

df = pd.concat([df_onion[['subreddit', 'title']], df_not_onion[['subreddit', 'title']]], axis=0)
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


print(f'\n{THE_ONION} {NOT_THE_ONION}')
clf, vectorizer = modeling.get_model(df, custom)

sentences = [
    'San Diego backyard shed rents for $1,050 a month',
    'Are You The Whistleblower? Trump Boys Ask White House Janitor After Giving Him Serum Of All The Sodas Mixed Together',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at diam ac orci pharetra scelerisque non sit amet turpis. Donec quis erat quam',
    '12356487984158641351568463213851684132168461'
]

process = Process(clf, vectorizer)
for sentence in sentences:
    print(f'\n{ME}')
    process.run(sentence)

# TODO: Future - Read data from Mongo
# TODO: Future - Create translator
# TODO: Future - Create score
