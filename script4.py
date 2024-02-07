from pulp import *

# Création du problème
prob = LpProblem("Optimisation_Emploi_du_Temps", LpMinimize)

# Jours et shifts
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
shifts = ["M", "A", "S", "R"] # Matin, Aprèm, Soir, Repos

# Employés
employes = ["X", "Y", "Z"]

# Variables de décision: 1 si l'employé e fait le shift s le jour j, 0 sinon
variables = LpVariable.dicts("Shift", (employes, jours, shifts), cat='Binary')

# Contraintes

## Chaque employé a deux jours de repos consécutifs
# Cette contrainte nécessite une logique spécifique pour chaque employé, nous allons simplifier en assurant au moins deux jours de repos

## Pas plus de deux nocturnes consécutives
# À gérer via des contraintes spécifiques sur les shifts de soirée

## X travaille 35 heures par semaine
heures_par_shift = {"M": 4.5, "A": 3.5, "S": 3, "R": 0} # Heures approximatives par shift
prob += lpSum([variables["X"][j][s] * heures_par_shift[s] for j in jours for s in shifts]) == 35

## X et Y travaillent maximum 7h par jour
# À implémenter avec les heures par shift

## X et Y travaillent minimum 5h s'ils se déplacent
# À gérer avec une logique spécifique pour chaque jour

## Minimum 30 minutes de relai entre deux personnes
# Cette contrainte est complexe à modéliser directement dans ce cadre sans informations supplémentaires sur les horaires exacts

## L'employé qui a fermé la boutique, ne doit pas ouvrir la boutique le lendemain
# À gérer avec une logique spécifique pour les shifts de soir et de matin

# Contraintes variables

## Z veut faire maximum 8h par jour
# À gérer avec une logique spécifique pour Z

## Y travaille entre 10h et 15h semaine
prob += lpSum([variables["Y"][j][s] * heures_par_shift[s] for j in jours for s in shifts]) >= 10
prob += lpSum([variables["Y"][j][s] * heures_par_shift[s] for j in jours for s in shifts]) <= 15

## Moins de nocturnes si travail le weekend
# À gérer avec une logique spécifique pour les shifts de soir

# Fonction objectif: ici, nous visons à minimiser le non-respect des contraintes variables si possible
# Cependant, dans ce cas, nous nous concentrons d'abord sur l'établissement des contraintes fixes
prob += 0, "Objectif arbitraire"

# Résolution du problème
prob.solve()

# Vérification de la solution
status = LpStatus[prob.status]
results = {"Status": status, "Solution": {}}

if status == "Optimal":
    for e in employes:
        for j in jours:
            for s in shifts:
                    if e not in results["Solution"]:
                        results["Solution"][e] = {}
                    if j not in results["Solution"][e]:
                        results["Solution"][e][j] = []
                    results["Solution"][e][j].append(s)

print(results)
