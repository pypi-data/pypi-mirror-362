import marimo

__generated_with = "0.14.10"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import polars.selectors as cs
    return (pl,)


@app.cell
def _(pl):
    _df = pl.DataFrame(
        {
            "index": ["index1", "index2", None, "i3", "i4"],
            "item": [
                {"name": "AB", "type": "t1", "other": "jfiosd"},
                {"name": "BC", "type": "t2", "other": "asdfi"},
                {"name": "DC", "type": "t3", "other": "asdf8"},
                {"name": "DC", "type": "t3", "other": "nkl"},
                {"name": "DC", "other": "fhdsu"},
            ],
            "value": [
                {"zz": [9, 8], "xx": "fjdi"},
                {"zz": [7, 6]},
                {"zz": [], "xx": "mikd"},
                {},
                {"xx": "abc"},
            ],
        },
        schema={
            "item": pl.Struct(
                {"name": pl.String, "type": pl.String, "other": pl.String}
            ),
            "value": pl.Struct({"zz": pl.List(pl.Int32), "xx": pl.String}),
            "index": pl.String,
        },
    )
    _df.pivot(on="item", values="value")
    return


if __name__ == "__main__":
    app.run()
