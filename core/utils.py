def normalize(series):
    return (series - series.mean()) / series.std()
