import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    from pathlib import Path
    return Path, pl


@app.cell
def _(Path, pl):
    _df = pl.read_csv(Path("data/db_exp_test/studentdatabase.csv"))
    _df
    return


if __name__ == "__main__":
    app.run()
