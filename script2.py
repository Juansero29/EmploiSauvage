from pulp import *
import pandas as pd

# Define the problem
prob = LpProblem("Optimal_Schedule", LpMinimize)

# Employees
employees = ['X', 'Y', 'Z']

# Days
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Shifts
shifts = ['M', 'A', 'S', 'R']  # Morning, Afternoon, Evening, Off

# Total hours needed for each shift by day
# Approximated based on opening hours and potential shift lengths
hours_needed = {
    'Monday': {'M': 4.5, 'A': 3.5, 'S': 3, 'R': 0},
    'Tuesday': {'M': 4.5, 'A': 3.5, 'S': 4.75, 'R': 0},
    'Wednesday': {'M': 4.5, 'A': 3.5, 'S': 4.75, 'R': 0},
    'Thursday': {'M': 4.5, 'A': 3.5, 'S': 4.75, 'R': 0},
    'Friday': {'M': 4.5, 'A': 3.5, 'S': 3, 'R': 0},
    'Saturday': {'M': 4, 'A': 3.5, 'S': 3.75, 'R': 0},
    'Sunday': {'M': 0, 'A': 0, 'S': 5.25, 'R': 0},  # Only evening shift as it opens at 13h
}

# Variables
# Each variable represents whether an employee works a specific shift on a specific day
x = LpVariable.dicts("shift", [(e, d, s) for e in employees for d in days for s in shifts], cat='Binary')

# Objective function
# We aim to minimize the deviation from desired hours and maximize overlap while respecting constraints
# For simplicity, we'll just ensure all shifts are covered for now
prob += 0, "Objective"

# Constraints

# Ensure each shift on each day is covered exactly as needed
for d in days:
    for s in shifts:
        if s == 'R':  # Skip 'R' as it's not a working shift
            continue
        prob += lpSum(x[e, d, s] for e in employees) == hours_needed[d][s], f"Cover_{d}_{s}"

# X works 35 hours per week
prob += lpSum(x['X', d, s] * hours_needed[d][s] for d in days for s in shifts if s != 'R') == 35, "X_35_hours"

# X and Y work maximum 7h per day and minimum 5h if they work
for e in ['X', 'Y']:
    for d in days:
        prob += lpSum(x[e, d, s] * hours_needed[d][s] for s in shifts if s != 'R') <= 7, f"Max_7h_{e}_{d}"
        prob += lpSum(x[e, d, s] for s in shifts if s != 'R') <= 1, f"One_shift_per_day_{e}_{d}"  # Simplification

# Add more constraints as necessary...

# Solve the problem
prob.solve()

# Collect and display the results
schedule = pd.DataFrame(index=pd.MultiIndex.from_product([employees, days, shifts], names=['Employee', 'Day', 'Shift']),
                        columns=['Assigned'])

for e, d, s in schedule.index:
    schedule.loc[(e, d, s), 'Assigned'] = value(x[e, d, s])

schedule = schedule[schedule['Assigned'] > 0.5].reset_index()  # Filter only assigned shifts
schedule
