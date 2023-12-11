import pickle
import re

with open('lg_tv.pickle', 'rb') as f:
    tfidf_vzer, lg_clf = pickle.load(f)
# class MovieViewSet(viewsets.ReadOnlyModelViewSet):

#     serializer_class = MovieSerializer
#     queryset = Movie.objects.all()

def regex_time(text):
    review = re.sub("(@[A-Za-z0-9]+)", ' ', text)
    review = re.sub("(https?://[A-Za-z0-9./]+)", ' ', review)
    review = re.sub("(http\S+)", ' ', review)
    review = re.sub("([^a-zA-Z.!?])", ' ',review)
    review = re.sub("( +)", ' ', review)
    return review


def sentiment_predictor(review):
    pred = lg_clf.predict(tfidf_vzer.transform([regex_time(review)]))
    
    if pred == [1]:
        return 'Positive'
    else:
        return 'Negative'
    
def get_probabilities(review):
    probas = lg_clf.predict_proba(tfidf_vzer.transform([regex_time(review)]))

    return probas