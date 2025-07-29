import pandas as pd
from speak2py.file_reader import load_data

def test_csv(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("a,b\n1,2\n3,4")
    df = load_data(str(file))
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)

# You can add similar tests for .json and .xlsx once you have sample files.
