from ortools.linear_solver import pywraplp

def solve_schedule():
    # Créer le solveur
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        return None

    # Définir les variables
    # Pour simplifier, nous utilisons une variable pour représenter le nombre d'heures travaillées par jour pour chaque employé
    # X[0] à X[6] pour les jours de la semaine, de même pour Y et Z
    days = range(7) # 0: Lundi, ..., 6: Dimanche
    X = [solver.IntVar(0, 7, f'X[{d}]') for d in days] # X travaille max 7h par jour, min 5h certains jours
    Y = [solver.IntVar(0, 7, f'Y[{d}]') for d in days] # Y travaille entre 10h et 15h par semaine
    Z = [solver.IntVar(0, 8, f'Z[{d}]') for d in days] # Z veut max 8h par jour

    # Contraintes

    # X travaille 35h par semaine
    solver.Add(solver.Sum(X[d] for d in days) == 35)

    # Y travaille entre 10h et 15h par semaine
    solver.Add(solver.Sum(Y[d] for d in days) >= 10)
    solver.Add(solver.Sum(Y[d] for d in days) <= 15)

    # Pour simplifier, nous ne modélisons pas toutes les contraintes ici, comme les jours de repos consécutifs
    
    # Objectif: Maximiser le chevauchement des horaires de travail pour favoriser le relai
    # (Ceci est une simplification; ajuster selon le besoin réel d'optimisation)
    solver.Maximize(solver.Sum(X[d] + Y[d] + Z[d] for d in days))

    # Résoudre le problème
    status = solver.Solve()

    # Vérifier si une solution a été trouvée
    if status == pywraplp.Solver.OPTIMAL:
        print("Solution trouvée :")
        for d in days:
            print(f"Jour {d}: Stagaire = {X[d].SolutionValue()}, Clémence = {Y[d].SolutionValue()}, Sarah = {Z[d].SolutionValue()}")
    else:
        print("Pas de solution optimale trouvée.")

if __name__ == "__main__":
    solve_schedule()
