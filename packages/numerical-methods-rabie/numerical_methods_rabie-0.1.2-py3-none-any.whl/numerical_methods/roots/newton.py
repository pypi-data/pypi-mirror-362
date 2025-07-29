def newton(e, f, fprime, x0=1, max_iter=1000, verbose=True):
    """
    Méthode de Newton.

    Paramètres:
    - e: tolérance
    - f: fonction f(x)
    - fprime: dérivée f'(x)
    - x0: valeur initiale
    - max_iter: itérations max
    - verbose: afficher les étapes

    Retourne:
    - x: valeur approchée de la racine
    """
    i = 1
    iteration = []
    while i <= max_iter:
        f_x0 = f(x0)
        fprime_x0 = fprime(x0)
        if fprime_x0 == 0:
            raise ZeroDivisionError("f'(x0) est nul.")
        
        x = x0 - f_x0 / fprime_x0
        iteration.append((i,x0,x))
        if verbose:
            print(f"[Newton] Iteration {i}: x0 = {x0:.6f}, x = {x:.6f}")
        if abs(x - x0) < e:
            return x, iteration
        x0 = x
        i += 1
    
    raise RuntimeError("Nombre d'itérations max atteint.")
