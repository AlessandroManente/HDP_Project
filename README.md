# HDP_Project

Repository for the High Dimensional Probability project, for the Master Degree in Data Science

What to test for each type of graph:

- Erdos-Renyi:

  - ~~giant component (its presence going from $d<1$ to $d>1$)~~
  - number of triangles ( *I don't think it should be done for the project* )
  - ~~nodes degree distributions~~

## Requirements

Just run the code:

```
pip install -r requirements.txt
```

## Usage Example

Let's say we want to fully analyse the Erdos-Renyi model with default arguments, then we just have to call:

```
python main.py
```

If one wants to modify the parameter $d$, then:

```
python main.py --d 1.6
```

