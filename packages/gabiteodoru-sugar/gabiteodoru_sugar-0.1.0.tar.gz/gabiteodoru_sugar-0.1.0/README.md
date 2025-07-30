# Sugar: Python Syntactic Sugar

A lightweight utility package that provides syntactic sugar and data manipulation tools to make Python code more concise and expressive.

## Installation

```bash
pip install git+https://github.com/gabiteodoru/sugar.git
```

Dependencies:
- pandas
- more_itertools

## Features

### Core Functions

- **Mapping Functions**: 
  - `imap`: List version of `map()`
  - `timap`: Tuple version of `map()`
  - `izip`: List version of `zip()`
  - `ifilter`: List version of `filter()`
  - `dmap`: Apply function to dictionary values
  - `dfilter`: Filter dictionary keys based on values
  - `flatten`: Flatten nested lists
  - `unique`: Return unique values from a list
- **Function Wrappers**: Operations using subtraction syntax
- **Smart String Splitting**: Handle nested brackets, quotes and special characters
- **Data Structure Manipulation**: Functions for dictionaries, lists and pandas DataFrames
- **Concise Data Access**: Simplified syntax for common operations

### Examples

```python
from sugar import *

# List operations
imap(lambda x: x+2, [2, 3, 4])  # [4, 5, 6]
timap(lambda x: x+2, [2, 3, 4])  # (4, 5, 6)
izip([1, 2], ['a', 'b'])        # [(1, 'a'), (2, 'b')]
ifilter(lambda x: x > 2, [1, 2, 3, 4])  # [3, 4]
flatten([[1, 2], [3, 4]])       # [1, 2, 3, 4]
unique([1, 2, 2, 3, 3])         # [1, 2, 3]

# Dictionary operations
dmap(lambda x: x*2, {'a': 1, 'b': 2})  # {'a': 2, 'b': 4}
dfilter(lambda x: x > 1, {'a': 1, 'b': 2, 'c': 3})  # ['b', 'c']

# String splitting
'a, b, c'-spl                   # ['a', 'b', 'c']
'a b c'-spls                    # ['a', 'b', 'c']
'a>b>c'-splon('>')              # ['a', 'b', 'c']
'a b c'-spls-first              # 'a'
'a b c'-spls-last               # 'c'

# Dictionary operations
'a:x, b:y, c:z'-spld            # {'a': 'x', 'b': 'y', 'c': 'z'}
'a:x, b:y, c:z'-spld-flipDict   # {'x': 'a', 'y': 'b', 'z': 'c'}

# Condition building
'a==1, b==2'-spland             # '(a==1)&(b==2)'

# DataFrame operations
df = pd.DataFrame({'x':'a, a, b'-spl, 'y':'c, d, d'-spl, 'z':[1, 2, 3]})
isUnique(df)                    # True
qselect(df,'y, colX:x')         # DataFrame with columns 'y' and 'colX' (renamed from 'x')
frontCols(df, 'y, z')           # DataFrame with columns reordered as ['y', 'z', 'x']
```

### Advanced Features

#### Script Execution

Run Python scripts in the current namespace:

```python
# Execute a script in the current namespace
eval(runpy)('script.py')
```

#### Function Application Syntax

Replace verbose function definitions with concise string expressions:

```python
# Traditional approach
def f(x):
    d = {}
    d['v'] = x.v.sum()
    d['dv'] = (x.v*x.c).sum()
    return pd.Series(d, index=['v', 'dv'])

rawData.groupby('s').apply(f)

# With sugar
rawData.groupby('s').apply('v: x.v.sum(), dv: (x.v*x.c).sum()'-fapply)
```

#### Data Classes

- `FriendlyDataClass`: Base class with dictionary-like access
- `Obj`: Enhanced dictionary with attribute access

#### Nested Structure Creation

```python
createNestedStruct('a, b, c', 'x, y', init=[1, 2, 3])
# Creates nested dictionary structure with leaf nodes [1, 2, 3]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Documentation

Documentation generated with assistance from Claude (Anthropic).