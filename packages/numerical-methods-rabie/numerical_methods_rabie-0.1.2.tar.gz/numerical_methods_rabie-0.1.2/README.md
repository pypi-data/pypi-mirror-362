# numerical-methods-rabie

Ce package Python contient des méthodes numériques classiques enseignées dans les cours universitaires.

## 📚 Méthodes incluses (v0.1.0)

- 🔍 **Méthodes de recherche de racines :**
  - Méthode de dichotomie
  - Méthode de Newton-Raphson
  - Méthode du point fixe

## 📦 Installation

```bash
pip install numerical-methods-rabie

🚀 Exemple d’utilisation

from numerical_methods.roots.dichotomie import dichotomie

    f = lambda x: x**2 - 2
    res, _ = dichotomie(1, 2, 1e-6, f)
    print(res)

📌 Modules à venir

Intégration numérique (trapeze, Simpson…)

Interpolation polynomiale

Résolution de systèmes linéaires

👤 Auteur
Développé par Rabie Oudghiri, pour partager les connaissances apprises en analyse numérique.
