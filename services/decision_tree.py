from sklearn.externals import joblib


def predict_crime(precinct):
    dt = joblib.load('dt_model.pkl')
    offenseEncoder = joblib.load('offenseEncoder.pkl')
    precinctEncoder = joblib.load('precinctEncoder.pkl')

    print dt

    return offenseEncoder.inverse_transform(dt.predict([precinctEncoder.transform([precinct])]))[0]
