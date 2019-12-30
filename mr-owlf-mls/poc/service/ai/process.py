from pandas import DataFrame


def run(clf: any, vectorizer: any, sentence: str) -> any:
    
    data = DataFrame([sentence], columns=['title'])
    data_cvec = vectorizer.transform(data['title'])
    preds_prob = clf.predict_proba(data_cvec)

    fake     = '{0:.2f}'.format(preds_prob[0][0])
    not_fake = '{0:.2f}'.format(preds_prob[0][1])

    print(f'Sentence => "{sentence}"')
    print(f'Prob. to be Fake "{fake}" / Not Fake "{not_fake}"')
    return not_fake
