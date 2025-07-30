# Frenet System Creator

Utilities for converting between Cartesian and Frenet frames. The package
provides a simple `FrenetSystem` class for projecting points onto a path
and performing coordinate conversions.

## Installation

```bash
pip install frenet-system-creator
```

## Usage

```python
from frenet_system_creator import FrenetSystem

path = [(0, 0), (1, 1), (2, 0)]
fs = FrenetSystem(path)

# Convert Cartesian to [d, s]
ds, _ = fs.cartesian2ds_frame((1.5, 1.0))

# Convert back to Cartesian
xy = fs.ds_frame2cartesian(ds)
```
