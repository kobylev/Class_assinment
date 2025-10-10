import numpy as np
from itertools import combinations

from create_csv_dataset import create_csv_dataset

# ייצר את קובץ הדאטה
create_csv_dataset()

filename = 'biased_6_columns_aliens.csv'
with open(filename, 'r') as f:
    headers = f.readline().strip().split(',')

data = np.loadtxt(filename, delimiter=',', skiprows=1)
# מלא את העמודה הראשונה בערך 1 בכ-90% מהמקרים
num_rows = data.shape[0]
num_ones = int(0.9 * num_rows)
data[:num_ones, 0] = 1
data[num_ones:, 0] = 0

bool_data = data.astype(bool)
print(headers)

num_rows, num_cols = bool_data.shape
columns = headers

def support(X, Y):
    return np.sum(np.logical_and(X, Y)) / num_rows

def confidence(X, Y):
    support_X = np.sum(X) / num_rows
    if support_X == 0:
        return 0
    return support(X, Y) / support_X

def lift(X, Y):
    support_X = np.sum(X) / num_rows
    support_Y = np.sum(Y) / num_rows
    support_XY = support(X, Y)
    if support_X * support_Y == 0:
        return 0
    return support_XY / (support_X * support_Y)

min_support = 0.3
min_confidence = 0.7

rules_found = []

for r in range(1, 4):
    for combo in combinations(range(num_cols), r):
        X_mask = np.ones(num_rows, dtype=bool)
        for c in combo:
            X_mask = np.logical_and(X_mask, bool_data[:, c])

        for y_col in range(num_cols):
            if y_col in combo:
                continue

            Y_mask = bool_data[:, y_col]

            sup = support(X_mask, Y_mask)
            conf = confidence(X_mask, Y_mask)
            lft = lift(X_mask, Y_mask)

            if sup >= min_support and conf >= min_confidence:
                rule = {
                    'Rule': f"{' & '.join([columns[c] for c in combo])} -> {columns[y_col]}",
                    'Support (%)': sup * 100,
                    'Confidence (%)': conf * 100,
                    'Lift': lft
                }
                rules_found.append(rule)

print(f"\nTotal number of Transactions (N): {num_rows}\n")
print(f"Filter: Support >= {min_support*100:.1f}%, Confidence >= {min_confidence*100:.1f}%\n")

print(f"{'Rule':<40} | {'Support (%)':>12} | {'Confidence (%)':>14} | {'Lift':>8}")
print("-" * 85)
for rule in rules_found:
    print(f"{rule['Rule']:<40} | {rule['Support (%)']:12.2f} | {rule['Confidence (%)']:14.2f} | {rule['Lift']:8.3f}")
