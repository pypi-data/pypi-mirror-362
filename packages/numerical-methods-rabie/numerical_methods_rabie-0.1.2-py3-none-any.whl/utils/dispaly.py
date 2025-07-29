from tabulate import tabulate

def print_iterations(iterations, headers):
    print(tabulate(iterations,headers=headers,tablefmt="fancy_grid"))