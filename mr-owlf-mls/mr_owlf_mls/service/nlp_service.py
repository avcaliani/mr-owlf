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

__author__ = 'Anthony Vilarim Caliani'
__contact__ = 'https://github.com/avcaliani'
__license__ = 'MIT'


class NLPService:

    def __init__(self):
        pass

    def exec(self, df: DataFrame) -> None:
        #   ____                       _    __     __             _                 _
        #  / ___|  ___   _   _  _ __  | |_  \ \   / /  ___   ___ | |_   ___   _ __ (_) ____  ___
        # | |     / _ \ | | | || '_ \ | __|  \ \ / /  / _ \ / __|| __| / _ \ | '__|| ||_  / / _ \
        # | |___ | (_) || |_| || | | || |_    \ V /  |  __/| (__ | |_ | (_) || |   | | / / |  __/
        #  \____| \___/  \__,_||_| |_| \__|    \_/    \___| \___| \__| \___/ |_|   |_|/___| \___|
        #                           ngram_range = (1,1)
        #
        # TODO: Study This!

        # ------------------------------------------------------------------------------
        #  TheOnion
        # ------------------------------------------------------------------------------
        # Set variables to show TheOnion Titles
        mask_on = df['classification'] == 1
        df_onion_titles = df[mask_on]['title']

        # Instantiate a CountVectorizer
        cv1 = CountVectorizer(stop_words='english')

        # Fit and transform the vectorizer on our corpus
        onion_cvec = cv1.fit_transform(df_onion_titles)

        # Convert onion_cvec into a DataFrame
        onion_cvec_df = DataFrame(
            onion_cvec.toarray(),
            columns=cv1.get_feature_names()
        )

        # Inspect head of Onion Titles cvec
        print(f'The Onion: {onion_cvec_df.shape}')

        # ------------------------------------------------------------------------------
        #  NotTheOnion
        # ------------------------------------------------------------------------------
        # Set variables to show NotTheOnion Titles
        mask_no = df['classification'] == 0
        df_not_onion_titles = df[mask_no]['title']

        # Instantiate a CountVectorizer
        cv2 = CountVectorizer(stop_words='english')

        # Fit and transform the vectorizer on our corpus
        not_onion_cvec = cv2.fit_transform(df_not_onion_titles)

        # Convert onion_cvec into a DataFrame
        not_onion_cvec_df = DataFrame(
            not_onion_cvec.toarray(),
            columns=cv2.get_feature_names()
        )

        # Inspect head of Not Onion Titles cvec
        print(f'Not The Onion: {not_onion_cvec_df.shape}')

        #  _   _         _
        # | | | | _ __  (_)  __ _  _ __   __ _  _ __ ___   ___
        # | | | || '_ \ | | / _` || '__| / _` || '_ ` _ \ / __|
        # | |_| || | | || || (_| || |   | (_| || | | | | |\__ \
        #  \___/ |_| |_||_| \__, ||_|    \__,_||_| |_| |_||___/
        #                   |___/
        # TODO: Study This!

        # ------------------------------------------------------------------------------
        #  TheOnion
        # ------------------------------------------------------------------------------
        # Set up variables to contain top 5 most used words in Onion
        onion_wc = onion_cvec_df.sum(axis=0)
        onion_top_5 = onion_wc.sort_values(ascending=False).head(5)

        # ------------------------------------------------------------------------------
        #  NotTheOnion
        # ------------------------------------------------------------------------------
        # Set up variables to contain top 5 most used words in r/nottheonion
        nonion_wc = not_onion_cvec_df.sum(axis=0)
        nonion_top_5 = nonion_wc.sort_values(ascending=False).head(5)

        # ------------------------------------------------------------------------------
        #  TheOnion x NotTheOnion
        # ------------------------------------------------------------------------------
        # Top 5 Bigrams: Create list of unique words in top five
        not_onion_5_set = set(nonion_top_5.index)
        onion_5_set = set(onion_top_5.index)

        # Return common words
        common_unigrams = onion_5_set.intersection(not_onion_5_set)
        print(common_unigrams.head())

        #   ____                       _    __     __             _                 _
        #  / ___|  ___   _   _  _ __  | |_  \ \   / /  ___   ___ | |_   ___   _ __ (_) ____  ___
        # | |     / _ \ | | | || '_ \ | __|  \ \ / /  / _ \ / __|| __| / _ \ | '__|| ||_  / / _ \
        # | |___ | (_) || |_| || | | || |_    \ V /  |  __/| (__ | |_ | (_) || |   | | / / |  __/
        #  \____| \___/  \__,_||_| |_| \__|    \_/    \___| \___| \__| \___/ |_|   |_|/___| \___|
        #                           ngram_range = (2,2)
        #
        # TODO: Study This!

        # ------------------------------------------------------------------------------
        #  TheOnion
        # ------------------------------------------------------------------------------
        # Set variables to show TheOnion Titles
        mask = df['classification'] == 1
        df_onion_titles = df[mask]['title']

        # Instantiate a CountVectorizer
        cv = CountVectorizer(stop_words='english', ngram_range=(2, 2))

        # Fit and transform the vectorizer on our corpus
        onion_cvec = cv.fit_transform(df_onion_titles)

        # Convert onion_cvec into a DataFrame
        onion_cvec_df = DataFrame(
            onion_cvec.toarray(),
            columns=cv.get_feature_names()
        )

        # Inspect head of Onion Titles cvec
        print(f'The Onion: {onion_cvec_df.shape}')

        # ------------------------------------------------------------------------------
        #  NotTheOnion
        # ------------------------------------------------------------------------------
        # Set variables to show NotTheOnion Titles
        mask = df['classification'] == 0
        df_not_onion_titles = df[mask]['title']

        # Instantiate a CountVectorizer
        cv = CountVectorizer(stop_words='english', ngram_range=(2, 2))

        # Fit and transform the vectorizer on our corpus
        not_onion_cvec = cv.fit_transform(df_not_onion_titles)

        # Convert onion_cvec into a DataFrame
        not_onion_cvec_df = DataFrame(
            not_onion_cvec.toarray(),
            columns=cv.get_feature_names()
        )

        # Inspect head of Not Onion Titles cvec
        print(f'Not The Onion: {not_onion_cvec_df.shape}')

        #  ____   _
        # | __ ) (_)  __ _  _ __   __ _  _ __ ___   ___
        # |  _ \ | | / _` || '__| / _` || '_ ` _ \ / __|
        # | |_) || || (_| || |   | (_| || | | | | |\__ \
        # |____/ |_| \__, ||_|    \__,_||_| |_| |_||___/
        #            |___/
        # TODO: Study This!

        # ------------------------------------------------------------------------------
        #  TheOnion
        # ------------------------------------------------------------------------------
        # Set up variables to contain top 5 most used bigrams in r/TheOnion
        onion_wc = onion_cvec_df.sum(axis=0)
        onion_top_5 = onion_wc.sort_values(ascending=False).head(5)
        print(onion_top_5.head())

        # ------------------------------------------------------------------------------
        #  NotTheOnion
        # ------------------------------------------------------------------------------
        # Set up variables to contain top 5 most used bigrams in r/nottheonion
        nonion_wc = not_onion_cvec_df.sum(axis=0)
        nonion_top_5 = nonion_wc.sort_values(ascending=False).head(5)
        print(nonion_top_5.head())

        # ------------------------------------------------------------------------------
        #  TheOnion x NotTheOnion
        # ------------------------------------------------------------------------------
        # Common Bigrams between Top 5 in r/TheOnion & r/nottheonion
        not_onion_5_list = set(nonion_top_5.index)
        onion_5_list = set(onion_top_5.index)

        # Return common words
        common_bigrams = onion_5_list.intersection(not_onion_5_list)
        print(common_bigrams.head())

        # Take out {'man', 'new', 'old', 'people', 'say', 'trump', 'woman', 'year'}
        # from dataset when modeling, since these words occur frequently in both classifications.

        #  ____   _                  __        __                  _
        # / ___| | |_   ___   _ __   \ \      / /  ___   _ __   __| | ___
        # \___ \ | __| / _ \ | '_ \   \ \ /\ / /  / _ \ | '__| / _` |/ __|
        #  ___) || |_ | (_) || |_) |   \ V  V /  | (_) || |   | (_| |\__ \
        # |____/  \__| \___/ | .__/     \_/\_/    \___/ |_|    \__,_||___/
        #                    |_|
        # Create custom stop_words to include common frequent words
        # Referencing the common most-used words, add them to a customized stop_words list.

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

        #  __  __             _        _  _
        # |  \/  |  ___    __| |  ___ | |(_) _ __    __ _
        # | |\/| | / _ \  / _` | / _ \| || || '_ \  / _` |
        # | |  | || (_) || (_| ||  __/| || || | | || (_| |
        # |_|  |_| \___/  \__,_| \___||_||_||_| |_| \__, |
        #                                           |___/
        # Baseline score
        # TODO: What is this?
        df['classification'].value_counts(normalize=True)
        # I expect my model to be better than 54%.
        # The majority class is 1, or, TheOnion.
        # If the model is not better than 54%, I know the model is not performing well.

        X = df['title']
        y = df['classification']
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
            'cvec__ngram_range': [(1, 1), (2, 2), (1, 3)],
            'lr__C': [0.01, 1]
        }

        gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
        gs.fit(X_train, y_train);
        print("Best score:", gs.best_score_)
        print("Train score", gs.score(X_train, y_train))
        print("Test score", gs.score(X_test, y_test))

        print(gs.best_params_)
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
            'tvect__ngram_range': [(1, 1), (1, 2), (1, 3)],
            'lr__C': [1]
        }

        gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
        gs.fit(X_train, y_train);
        print("Best score:", gs.best_score_)
        print("Train score", gs.score(X_train, y_train))
        print("Test score", gs.score(X_test, y_test))

        print(gs.best_params_)
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
            'cvec__ngram_range': [(1, 1), (1, 3)],
            'nb__alpha': [.36, .6]
        }

        gs = GridSearchCV(pipe, param_grid=pipe_params, cv=3)
        gs.fit(X_train, y_train);
        print("Best score:", gs.best_score_)
        print("Train score", gs.score(X_train, y_train))
        print("Test score", gs.score(X_test, y_test))

        print(gs.best_params_)
        # The model is overfit, but as I mentioned, I am optimizing for accuracy.
        # I want to ensure that all predictions are correct.
        # That is, all posts from r/TheOnion must be classified as being from the classification r/TheOnion,
        # and all posts from r/nottheonion must be classified as being from the classification r/nottheonion.
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
            'tvect__ngram_range': [(1, 2), (1, 3)],
            'nb__alpha': [0.1, 1]
        }

        gs = GridSearchCV(pipe, param_grid=pipe_params, cv=5)
        gs.fit(X_train, y_train);
        print("Best score:", gs.best_score_)
        print("Train score", gs.score(X_train, y_train))
        print("Test score", gs.score(X_test, y_test))

        print(gs.best_params_)
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

        # Instantiate the classifier and vectorizer
        nb = MultinomialNB(alpha=0.36)
        cvec = CountVectorizer(ngram_range=(1, 3))

        # Fit and transform the vectorizor
        cvec.fit(X_train)

        Xcvec_train = cvec.transform(X_train)
        Xcvec_test = cvec.transform(X_test)

        # Fit the classifier
        nb.fit(Xcvec_train, y_train)

        # Create the predictions for Y training data
        preds = nb.predict(Xcvec_test)

        print(nb.score(Xcvec_test, y_test))

        # Create a confusion matrix
        cnf_matrix = metrics.confusion_matrix(y_test, preds)
        print(confusion_matrix)

        # Code from https://www.datacamp.com/community/tutorials/understanding-logistic-regression-python
        # name  of classes
        class_names = [0, 1]

        cnf_matrix = np.array(cnf_matrix).tolist()
        tn_fp, fn_tp = cnf_matrix
        tn, fp = tn_fp
        fn, tp = fn_tp

        print("Accuracy:", round(metrics.accuracy_score(y_test, preds) * 100, 2), '%')
        print("Precision:", round(metrics.precision_score(y_test, preds) * 100, 2), '%')
        print("Recall:", round(metrics.recall_score(y_test, preds) * 100, 2), '%')
        print("Specificity:", round((tn / (tn + fp)) * 100, 2), '%')
        print("Misclassification Rate:", round((fp + fn) / (tn + fp + fn + tn) * 100, 2), '%')

        # TODO: Study!
        #
        # CountVectorizer & Logistic Regression: Best Coefficient Interpretability
        #

        # Customize stop_words to include `onion` so that it doesn't appear
        # in coefficients

        stop_words_onion = stop_words.ENGLISH_STOP_WORDS
        stop_words_onion = list(stop_words_onion)
        stop_words_onion.append('onion')

        # Instantiate the classifier and vectorizer
        lr = LogisticRegression(C=1.0, solver='liblinear')
        cvec2 = CountVectorizer(stop_words=stop_words_onion)

        # Fit and transform the vectorizor
        cvec2.fit(X_train)

        Xcvec2_train = cvec2.transform(X_train)
        Xcvec2_test = cvec2.transform(X_test)

        # Fit the classifier
        lr.fit(Xcvec2_train, y_train)

        # Create the predictions for Y training data
        lr_preds = lr.predict(Xcvec2_test)

        print(lr.score(Xcvec2_test, y_test))

        #
        # Coefficient Analysis
        #
        # Create list of logistic regression coefficients
        lr_coef = np.array(lr.coef_).tolist()
        lr_coef = lr_coef[0]

        # create dataframe from lasso coef
        lr_coef = pd.DataFrame(np.round_(lr_coef, decimals=3),
                               cvec2.get_feature_names(), columns=["penalized_regression_coefficients"])

        # sort the values from high to low
        lr_coef = lr_coef.sort_values(by='penalized_regression_coefficients',
                                      ascending=False)

        # Jasmine changing things up here on out! Top half not mine.
        # create best and worst performing lasso coef dataframes
        df_head = lr_coef.head(10)
        df_tail = lr_coef.tail(10)

        # merge back together
        df_merged = pd.concat([df_head, df_tail], axis=0)

        print("The word that contributes the most positively to being from r/TheOnion is '",
              df_merged.index[0], "' followed by '",
              df_merged.index[1], "' and '",
              df_merged.index[2], "'.")

        print("-----------------------------------")

        print("The word that contributes the most positively to being from r/nottheonion is' ",
              df_merged.index[-1], "' followed by '",
              df_merged.index[-2], "' and '",
              df_merged.index[-3], "'.")

        # Show coefficients that affect r/TheOnion
        df_merged_head = df_merged.head(10)
        exp = df_merged_head['penalized_regression_coefficients'].apply(lambda x: np.exp(x))
        df_merged_head.insert(1, 'exp', exp)
        df_merged_head.sort_values('exp', ascending=False)

        print("As occurences of '", df_merged_head.index[0], "' increase by 1 in a title, that title is '",
              round(df_merged_head['exp'][0], 2), "' times as likely to be classified as r/TheOnion.")

        # Show coefficients that affect r/nottheonion
        df_merged_tail = df_merged.tail(10)
        exp = df_merged_tail['penalized_regression_coefficients'].apply(lambda x: np.exp(x * -1))
        df_merged_tail.insert(1, 'exp', exp)
        df_merged_tail.sort_values('exp', ascending=False)

        print("As occurences of", df_merged_tail.index[-1], "increase by 1 in a title, that title is",
              round(df_merged_tail['exp'][-1], 2), "times as likely to be classified as r/nottheonion.")

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

        #     _     _   _  _____  _   _   ___   _   _ __   __
        #    / \   | \ | ||_   _|| | | | / _ \ | \ | |\ \ / /
        #   / _ \  |  \| |  | |  | |_| || | | ||  \| | \ V /
        #  / ___ \ | |\  |  | |  |  _  || |_| || |\  |  | |
        # /_/   \_\|_| \_|  |_|  |_| |_| \___/ |_| \_|  |_|
        #
        # _my_data = pd.DataFrame(
        #     [
        #         'San Diego backyard shed rents for $1,050 a month',
        #         'Are You The Whistleblower? Trump Boys Ask White House Janitor After Giving Him Serum Of All The Sodas Mixed Together',
        #         'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at diam ac orci pharetra scelerisque non sit amet turpis. Donec quis erat quam',
        #         '12356487984158641351568463213851684132168461'
        #     ], columns=['title']
        # )
        # print(_my_data.shape)
        #
        # _my_data_cvec = cvec.transform(_my_data['title'])
        # print(_my_data_cvec.shape)
        #
        # _preds = nb.predict(_my_data_cvec)
        # _preds_prob = nb.predict_proba(_my_data_cvec)
        # print(_preds)
        # print(_preds_prob)
        #
        # print(f'+\tThe Onion\tNot The Onion')
        # for i in range(0, len(_preds_prob)):
        #     nto = '{0:.2f}'.format(_preds_prob[i][0])
        #     to = '{0:.2f}'.format(_preds_prob[i][1])
        #     print(f'{i}\t{to}\t\t{nto}')

        # print(X_train.shape)
        # print(">>>>>>#>>>")
        # print(Xcvec_train.shape)
