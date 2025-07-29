# Python Tools for Applications of Interval Design

## Requirements

Python 3.11+

## Installation

```sh
pip install interval-tools
```

Or if you want to use
[ObjectId](https://www.mongodb.com/docs/manual/reference/bson-types/#objectid)
as a unique identifier for `Entity` or `Aggregate`, run

```sh
pip install "interval-tools[objectid]"
```

## Quickstart

```pycon
>>> from interval.utils import batched
>>> for batch in batched('ABCDEFG', 3):
...     print(batch)
...
('A', 'B', 'C')
('D', 'E', 'F')
('G',)
```
