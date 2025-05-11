import time
import random

def resolve(ci, cj):
    resolvents = set()
    for literal in ci:
        if -literal in cj:
            resolvent = (ci - {literal}) | (cj - {-literal})
            resolvents.add(frozenset(resolvent))
    return resolvents

def generate_random_cnf(num_clauses, num_vars=100, max_clause_len=5):
    clauses = []
    for _ in range(num_clauses):
        clause_len = random.randint(1, max_clause_len)
        clause = set()
        while len(clause) < clause_len:
            var = random.randint(1, num_vars)
            literal = var if random.random() < 0.5 else -var
            clause.add(literal)
        clauses.append(clause)
    return clauses

def resolution_algorithm(clauses):
    clauses = set(frozenset(clause) for clause in clauses)
    new = set()
    processed_pairs = set()

    while True:
        for ci in clauses:
            for cj in clauses:
                if ci == cj:
                    continue
                pair = tuple(sorted([ci, cj], key=id))
                if pair in processed_pairs:
                    continue
                processed_pairs.add(pair)

                resolvents = resolve(ci, cj)
                if frozenset() in resolvents:
                    return False
                new |= resolvents

        if new.issubset(clauses):
            return True

        clauses |= new

if __name__ == "__main__":
    clause_sizes = [10, 100, 1000, 10000, 100000, 1000000]

    for size in clause_sizes:
        print(f"\n=== Test cu {size} clauze ===")

        clauses = generate_random_cnf(size)

        start_time = time.time()
        result = resolution_algorithm(clauses)
        end_time = time.time()
        duration = end_time - start_time

        result_text = "Satisfiabila" if result else "Nesatisfiabila"

        print(f"Rezultat: {result_text}")
        print(f"Timp executie: {duration:.4f} secunde")
