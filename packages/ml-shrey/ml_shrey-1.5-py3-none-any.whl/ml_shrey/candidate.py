import csv

def candidate_elimination(file_path):
    import csv
    with open(file_path, 'r') as f:
        data = list(csv.reader(f))
    n_attrs = len(data[0]) - 1
    S = data[0][:n_attrs]
    G = ['?'] * n_attrs
    temp_G = []
    print(f"\nInitial S0: {S}")
    print(f"Initial G0: {G}\n")
    print("Candidate Elimination Process:")
    for i, example in enumerate(data):
        attrs, label = example[:n_attrs], example[n_attrs]
        if label == 'Yes':
            S = [S[j] if S[j] == attrs[j] else '?' for j in range(n_attrs)]
            temp_G = [h for h in temp_G if all(h[j] == '?' or h[j] == S[j] for j in range(n_attrs))]
        else:
            for j in range(n_attrs):
                if S[j] != attrs[j] and S[j] != '?':
                    new_h = ['?'] * n_attrs
                    new_h[j] = S[j]
                    temp_G.append(new_h)
        print(f"Training Eg {i + 1}: S{i + 1} = {S}")
        print(f"Training Eg {i + 1}: G{i + 1} = {temp_G if temp_G else [G]}")
    print(f"\nFinal Version Space:")
    print(f"S (Most Specific): {S}")
    print(f"G (Most General): {temp_G if temp_G else [G]}")

def candidate(*args, **kwargs):
    return candidate_elimination(*args, **kwargs)
