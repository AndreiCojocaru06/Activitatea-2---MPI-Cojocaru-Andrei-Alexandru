import time
import random

def dpll(clauses, assignment=set()):
    clauses = set(clauses)

    clauses, assignment = unit_propagate(clauses, assignment)
    if clauses is None:
        return False, None
    if not clauses:
        return True, assignment

    clauses, assignment = eliminate_pure_literals(clauses, assignment)
    if not clauses:
        return True, assignment

    literal = choose_literal(clauses)

    new_clauses = simplify(clauses, literal)
    if new_clauses is not None:
        sat, new_assignment = dpll(new_clauses, assignment | {literal})
        if sat:
            return True, new_assignment

    new_clauses = simplify(clauses, -literal)
    if new_clauses is not None:
        sat, new_assignment = dpll(new_clauses, assignment | {-literal})
        if sat:
            return True, new_assignment

    return False, None

def choose_literal(clauses):
    smallest_clause = min(clauses, key=len)
    return next(iter(smallest_clause))

def simplify(clauses, literal):
    new_clauses = set()
    for clause in clauses:
        if literal in clause:
            continue
        if -literal in clause:
            new_clause = clause - {-literal}
            if not new_clause:
                return None
            new_clauses.add(new_clause)
        else:
            new_clauses.add(clause)
    return new_clauses

def unit_propagate(clauses, assignment):
    clauses = set(clauses)
    unit_clauses = {next(iter(c)) for c in clauses if len(c) == 1}

    while unit_clauses:
        literal = unit_clauses.pop()
        assignment |= {literal}
        new_clauses = set()
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clause = clause - {-literal}
                if not new_clause:
                    return None, None
                new_clauses.add(new_clause)
            else:
                new_clauses.add(clause)
        clauses = new_clauses
        unit_clauses |= {next(iter(c)) for c in clauses if len(c) == 1}
    return clauses, assignment

def eliminate_pure_literals(clauses, assignment):
    literal_counts = {}
    for clause in clauses:
        for literal in clause:
            literal_counts[literal] = literal_counts.get(literal, 0) + 1

    pure_literals = {lit for lit in literal_counts if -lit not in literal_counts}
    if not pure_literals:
        return clauses, assignment

    assignment |= pure_literals
    new_clauses = {clause for clause in clauses if not any(lit in pure_literals for lit in clause)}
    return new_clauses, assignment

def generate_random_cnf(num_clauses, num_vars=100, max_clause_len=5):
    clauses = []
    for _ in range(num_clauses):
        clause_len = random.randint(1, max_clause_len)
        clause = set()
        while len(clause) < clause_len:
            var = random.randint(1, num_vars)
            literal = var if random.random() < 0.5 else -var
            clause.add(literal)
        clauses.append(frozenset(clause))
    return clauses

if __name__ == "__main__":
    clause_sizes = [10, 100, 1000, 10000, 100000, 1000000]

    for size in clause_sizes:
        print(f"\n=== Test cu {size} clauze ===")

        clauses = generate_random_cnf(size)

        start_time = time.time()
        sat, assignment = dpll(clauses)
        end_time = time.time()
        duration = end_time - start_time

        result_text = "Satisfiabila" if sat else "Nesatisfiabila"

        print(f"Rezultat: {result_text}")
        print(f"Timp executie: {duration:.4f} secunde")
