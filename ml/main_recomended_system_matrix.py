import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder

# pivot ratings into movie features
ratings = pd.read_csv("dataset.csv", delimiter=";")[:1000000]
# product_encoder = LabelEncoder()
# related_product_encoder = LabelEncoder()
# ratings['product'] = product_encoder.fit_transform(ratings['product'])
# ratings['related_product'] = related_product_encoder.fit_transform(ratings['related_product'])
rating_crosstab = ratings.pivot_table(index='product',
                                           columns='related_product',
                                           values='correlation',
                                           fill_value=0)

print(rating_crosstab.head())
X = rating_crosstab.T
SVD = TruncatedSVD(n_components=12, random_state=5)
resultant_matrix = SVD.fit_transform(X)
print(resultant_matrix.shape)
corr_mat = np.corrcoef(resultant_matrix)
print(corr_mat.shape)
col_idx = rating_crosstab.columns.get_loc(1251411)
corr_specific = corr_mat[col_idx]
print(pd.DataFrame({'corr_specific': corr_specific,
                    'Movies': rating_crosstab.columns}).sort_values('corr_specific', ascending=False).head(1000))
quit()