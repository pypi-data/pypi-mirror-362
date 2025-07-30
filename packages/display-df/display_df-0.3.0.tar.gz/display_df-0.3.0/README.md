# Display Df: A pip-installable, interactive, Pandas DataFrame viewer that enables better-than-notepad viewing abilities in normal Python files 👀

The tool enables viewing and searching of a pandas DataFrame in a UI.
- View multi-million line DataFrames interactively
- It's faster than viewing a .csv in Excel
- It can display a nearly unlimited number of lines
- You can search all or just a subset of columns
- It can act as a breakpoint in your code which helps with debugging of DataFrames in normal Python code preventing the need for endless cells in notebooks
- It has a window_title field which allows you to have multiple calls to the display_df without losing track of which step you're on

## Installation

```bash
pip install display_df
```

## Usage

```python
import pandas as pd
from display_df import display_df

df1 = pd.DataFrame({...})
display_df(df_=df1, window_title="This is a title of your df window, for debugging purposes")
```

## Features
- Interactive search by column or all columns
- View multi-million line DataFrames interactively
- PyQt5 GUI

## License
MIT 
