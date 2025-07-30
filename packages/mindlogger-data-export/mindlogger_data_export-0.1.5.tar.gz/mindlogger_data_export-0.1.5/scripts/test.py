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
    _df = pl.read_parquet(Path("data/hbn_ods/output/APQ_Short_P.parquet"))
    _df
    return


if __name__ == "__main__":
    app.run()
