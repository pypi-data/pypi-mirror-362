# 🐦 birddata

A beginner-friendly dataset for bird classification – inspired by the classic `load_iris`, but with a fresh and fun twist!

---

## 📌 Description

If you're learning Machine Learning and want a clean, ready-to-use dataset to practice classification, `birddata` is for you!

Just like `load_iris`, it returns a pandas DataFrame – but instead of flowers, it's about **birds** 🐥.

Designed specifically for beginners, this dataset helps you practice:

- Binary & multi-class classification
- Feature encoding
- Data scaling
- Building models using `scikit-learn`

---

## 🔍 Features

| Feature      | Type         | Description                          |
| ------------ | ------------ | ------------------------------------ |
| Wing_Span    | Numerical    | Wingspan of the bird (in cm)         |
| Beak_Length  | Numerical    | Length of the beak (in cm)           |
| Can_Fly      | Binary (0/1) | Can the bird fly?                    |
| Is_Nocturnal | Binary (0/1) | Is the bird active at night?         |
| Habitat_Type | Categorical  | Encoded as numbers (e.g., forest)    |
| Bird_Type    | Categorical  | Target variable (Sparrow, Eagle etc) |

---

## 🚀 Installation

```bash
pip install birddata
```

from birddata import load_bird
import pandas as pd

df = load_bird()
print(df.head())

## 🙌 Acknowledgements

- Inspired by the classic `load_iris` dataset from the `scikit-learn` library
- Thanks to the amazing open-source Python community 💙
- Special thanks to [scikit-learn](https://scikit-learn.org/) and the Python Software Foundation
