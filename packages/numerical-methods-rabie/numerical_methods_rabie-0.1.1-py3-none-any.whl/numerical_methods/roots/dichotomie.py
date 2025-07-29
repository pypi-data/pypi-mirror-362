def dichotomie(a, b, e, f, verbose=True):
    """
    Méthode de dichotomie pour trouver une racine de f dans [a, b].

    Paramètres:
    - a, b: bornes de l'intervalle (a < b et f(a)*f(b) < 0)
    - e: tolérance (Erreur)
    - f: fonction continue
    - verbose: afficher les étapes si True

    Retourne:
    - m: approximation de la racine
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La condition f(a)*f(b) < 0 n'est pas satisfaite.")
    
    iterations = []
    
    while (b - a) > e:
        m = (a + b) / 2
        if verbose:
            print(f"[Dichotomie] a = {a:.6f}, b = {b:.6f}, m = {m:.6f}")
        iterations.append((a, b, m))
        if f(m) * f(a) < 0:
            b = m
        else:
            a = m

    return m, iterations
