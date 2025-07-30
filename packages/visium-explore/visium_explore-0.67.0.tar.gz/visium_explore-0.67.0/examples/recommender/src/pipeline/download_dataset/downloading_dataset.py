"""Download dataset and save it as parquet file."""

import pathlib

import pandas as pd
import typer


def main(
    input_dir: pathlib.Path = typer.Option(...),
    output_dir: pathlib.Path = typer.Option(...),
) -> None:
    """Download datasets and save them as parquet file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    data_tr = pd.read_csv(input_dir / "ua_base.csv")
    data_te = pd.read_csv(input_dir / "ua_test.csv")
    df_genre = pd.read_csv(input_dir / "u_genre.csv")
    df_movies = pd.read_csv(input_dir / "u_item.csv")
    df_users = pd.read_csv(input_dir / "u_user.csv")

    data_tr.to_parquet(output_dir / "data_tr.parquet")
    data_te.to_parquet(output_dir / "data_te.parquet")
    df_genre.to_parquet(output_dir / "df_genre.parquet")
    df_movies.to_parquet(output_dir / "df_movies.parquet")
    df_users.to_parquet(output_dir / "df_users.parquet")


if __name__ == "__main__":
    typer.run(main)
