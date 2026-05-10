The program generates an initial solution using the nearest neighbor algorithm, then uses simulated annealing to find better solutions. After, it plots the convergence rate and compares the initial and final routes. 

To run the program, enter: 

`python .\main.py --input=inputs/input.csv` or `python .\main.py -i=inputs/input.csv`

where `input` is tiny, small, medium, or large.

This program supports a few flags specifying the perturbation type and distance type. To specify perturbation type use:

`-r=reverse` or `-r=swap`

To specify distance type use: 

`-d=euclidean` or `-r=manhattan`

By default, the program will use euclidean distance and reverse.
