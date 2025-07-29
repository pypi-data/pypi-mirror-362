def point_fixe(e, g, x0=1, max_iter=1000, verbose=True):
    """
    Méthode du point fixe.

    Paramètres:
    - e: tolérance
    - g: fonction g(x) = x
    - x0: point initial
    - max_iter: itérations max pour éviter boucle infinie
    - verbose: afficher les étapes

    Retourne:
    - x: valeur approchée du point fixe
    """
    i = 1
    iterations = []
    while i <= max_iter:
        x = g(x0)
        iterations.append((i,x0,x))
        if verbose:
            print(f"[Point Fixe] Iteration {i}: x0 = {x0:.6f}, x = {x:.6f}")
        if abs(x - x0) < e:
            return x
        x0 = x
        i += 1
    
    raise RuntimeError("Nombre d'itérations max atteint.")
