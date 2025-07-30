"""Read and write data."""

import pandas as pd


def save_sparse_matrix_as_parquet(sparse_matrix, output_dir, name):
    """Converts the sparse data to a dataframe and stores it as a parquet file."""
    df_sparse_matrix = pd.DataFrame(sparse_matrix.todense())
    df_sparse_matrix.to_parquet(output_dir / name)
