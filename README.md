# Problème d'optimisation d'emploi du temps

Le but est d'avoir la/les semaine(s) type d'emploi du temps en respectant le maximum des contraintes possibles pour 3 employés d'une entreprise. Le résultat attendu est d'avoir une seule semaine d'emploi du temps qui pourrait toujours être utilisée comme semaine type pour les 3 employés. On ne tient pas compte de jours fériés, ni des congés, ni des absences par maladie ou autres exceptions de date (années bissextile, fuseaux horaires, etc).

## Contraintes

### Contraites Fixes

- Il ya a au total 3 employés: X, Y, Z
- Tout le monde, mais surtout X, a deux jours de repos consécutifs par semaine
- Un employé ne doit pas faire plus de deux nocturnes (travail après 18h) d'affilé
- X travaille 35 heures par semaine
- X et Y travaillent maximum 7h par jour
- X et Y travaillent minimum 5h s'ils se déplacent au travail
- Il faut minimum 30 minutes de relai entre deux personnes (e.g si X fini ses heures et Y commence ses heures après X, il faut que X et Y soient ensembles pendant minimum 30 minutes)
- L'employé qui a fermé la boutique, ne dois pas ouvrir la boutique le lendemain

### Contraintes Variables

- Z veut au possible faire maximum 8h par jour
- Y travaille entre 10h et 15h semaine
- Quand un employé travaille le weekend, il fait moins de nocturnes


## Horaires d'ouverture de la boutique

- Lundi : 10h à 19h15 (9.25h)
- Mardi : 10h à 21h45 (11.75h)
- Mercredi : 10h à 21h45 (11.75h)
- Jeudi : 10h à 21h45 (11.75h)
- Vendredi : 10h à 19h15 (9.25h)
- Samedi : 10h30 à 18h15 (7.75h)
- Dimanche :  13h à 18h15 (5.25h)

Total par semaine : 66.75h

## Shifts Possibles

```text
 M => Matin/Midi (Ouverture - 14h30) 4h-4h30
 A => Aprèm (14h - 17h30) 3h30
 S => Soir (17h - Fermeture) 1h15 - 4h45
 R => Repos Toute la journée
 ```


```text
M => Matin/Midi (Ouverture - 13h)
A => Aprèm (12h30 - 17h30) 3h30
S => Soir (17h - Fermeture) 1h15 - 4h45
R => Repos Toute la journée
```

### Autres Informations

- Qu'est-ce qu'il se passe les jours fériés ? Ils travaillent comme d'habitude. Les horaires de chaque jours sont respectés.
- Comment fonctionnent les jours de repos ? Ils ne sont pas pris en compte.

## Liens interessants de programmation par contraintes

- <https://developers.google.com/optimization/introduction/overview>
- <https://developers.google.com/optimization/cp>
- <https://github.com/google/or-tools/blob/master/examples/dotnet/ShiftSchedulingSat.cs>
- <https://developers.google.com/optimization/scheduling/employee_scheduling>
- <https://www.optaplanner.org/learn/useCases/employeeRostering.html>

## Autres questions à explorer

- La semaine type (approche statique) est-elle vraiment la meilleure approche pour établir l'emploi du temps des salariés ?
  - À analyser pours/contres face à un système dynamique ? Système dynamique = un système temps réel, qui tient compte des jours feriés, congés, maladies, fuseaux horaires, etc. mais qui changerait constamments)
  - Possiblité de pondre les deux (statique et dynamique) via les algorithmes de contraintes ?

## Installation de libraries Python Optimisation

Un solveur d'optimisation linéaire mixte est sûrement nécessaire pour accomplir cette opti

- [Google OR Tools](https://developers.google.com/optimization/install)
  - `python -m pip install --upgrade --user ortools`
- [PuLP](https://pypi.org/project/PuLP/)
  - `pip install pulp`
- [gurobipy](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python)
  - `python -m pip install gurobipy`
- [cplex](https://pypi.org/project/cplex/)