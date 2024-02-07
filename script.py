from ortools.sat.python import cp_model

# Modèle
model = cp_model.CpModel()

# Jours de la semaine pour les shifts
jours = list(range(7))  # 0: Lundi, 1: Mardi, ..., 6: Dimanche

# Shifts possibles
shifts = {
    'M': 0,  # Matin/Midi
    'A': 1,  # Après-midi
    'S': 2,  # Soir
    'R': 3   # Repos
}

# Nombre d'heures par shift, approximatif pour simplification
heures_shift = {
    'M': 4.5,  # Moyenne entre 4h et 4h30
    'A': 3.5,
    'S': 3,    # Moyenne des possibilités
    'R': 0
}

# Employés
employes = ['X', 'Y', 'Z']

# Variable de décision : shift[employé, jour]
shift = {}
for employe in employes:
    for jour in jours:
        shift[(employe, jour)] = model.NewIntVar(0, len(shifts) - 1, f'shift_{employe}_{jour}')

# Contraintes
# 1. X travaille 35 heures par semaine
model.Add(sum(heures_shift[shift] for jour in jours for shift in shifts if shift[(employe, jour)] == shifts['M'] or shift[(employe, jour)] == shifts['A'] or shift[(employe, jour)] == shifts['S']) == 35 for employe in employes if employe == 'X')

# 2. X et Y travaillent max 7h et min 5h par jour (s'ils travaillent)
for employe in ['X', 'Y']:
    for jour in jours:
        model.Add(sum(heures_shift[shift] for shift in shifts if shift[(employe, jour)] != shifts['R']) <= 7)
        # Ajout de la condition de minimum 5h si déplacement (implique au moins un shift qui n'est pas R)
        model.Add(sum(heures_shift[shift] for shift in shifts if shift[(employe, jour)] != shifts['R']) >= 5)

# 3. Deux jours de repos consécutifs
for employe in employes:
    for jour in range(5):  # Jusqu'à vendredi pour assurer deux jours consécutifs
        model.Add(shift[(employe, jour)] == shifts['R']).OnlyEnforceIf(shift[(employe, jour+1)] == shifts['R'])
        model.Add(shift[(employe, jour)] == shifts['R']).OnlyEnforceIf(shift[(employe, jour+2)] == shifts['R'])

# 4. Pas plus de deux nocturnes d'affilé
for employe in employes:
    for jour in range(5):  # Jusqu'à vendredi
        model.Add(shift[(employe, jour)] != shifts['S']).Or(shift[(employe, jour+1)] != shifts['S']).Or(shift[(employe, jour+2)] != shifts['S'])

# Plus d'autres contraintes nécessaires...

# Solution printer
class ShiftsSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""
    def __init__(self, shift, jours, employes, shifts):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shift = shift
        self._jours = jours
        self._employes = employes
        self._shifts = shifts
        self._solution_count = 0

    def OnSolutionCallback(self):
        self._solution_count += 1
        for jour in self._jours:
            print(f'Jour {jour}:')
            for employe in self._employes:
                shift_name = [name for name, code in self._shifts.items() if code == self.Value(self._shift[(employe, jour)])][0]
                print(f'  {employe}: {shift_name}')
        print()

# Résolution
solver = cp_model.CpSolver()
solution_printer = ShiftsSolutionPrinter(shift, jours, employes, shifts)
status = solver.SearchForAllSolutions(model, solution_printer)

# Vérification du statut de la solution
if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    print("Solution trouvée.")
else:
    print("Pas de solution trouvée ou problème de modèle.")

