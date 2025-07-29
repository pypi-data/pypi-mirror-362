import pandas as pd
import os

def load_bird():
    path = os.path.join(os.path.dirname(__file__), 'bird_dataset.csv')
    df = pd.read_csv(path)
    return df
