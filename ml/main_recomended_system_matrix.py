import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


# pivot ratings into movie features
ratings = pd.read_csv("dataset.csv", delimiter=";")[:250000]
unique_ids = ratings['product'].unique()

# product_encoder = LabelEncoder()
# related_product_encoder = LabelEncoder()
# ratings['product'] = product_encoder.fit_transform(ratings['product'])
# ratings['related_product'] = related_product_encoder.fit_transform(ratings['related_product'])
rating_crosstab = ratings.pivot_table(index='product',
                                      columns='related_product',
                                      values='correlation',
                                      fill_value=0)

SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(rating_crosstab.T)
corr_mat = np.corrcoef(resultant_matrix)
for unique_id in unique_ids:
    try:
        corr_specific = corr_mat[rating_crosstab.columns.get_loc(unique_id)]
        df = pd.DataFrame({'corr_specific': corr_specific,
                           'Recomends': rating_crosstab.columns}).sort_values('corr_specific',
                                                                                ascending=False).head(10000)
        df = df.reset_index(level=0, drop=True)
        pd.DataFrame(df).to_csv(f"{unique_id}.csv",
                                index=False,
                                sep=";",
                                encoding="utf-8")
    except:
        pass
    quit()
