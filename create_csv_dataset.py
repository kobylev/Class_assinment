import numpy as np
import csv

def create_csv_dataset(filename="biased_6_columns_aliens.csv", num_rows=5000,
                       prob_ones_first3=0.9, prob_ones_last3=0.1):
    num_cols = 6

    np.random.seed(42)
    data = np.zeros((num_rows, num_cols), dtype=int)

    # Fill columns 1-3 with probability for 1 given by prob_ones_first3
    for col in range(3):
        data[:, col] = (np.random.rand(num_rows) < prob_ones_first3).astype(int)

    # Fill columns 4-6 with probability for 1 given by prob_ones_last3
    for col in range(3, 6):
        data[:, col] = (np.random.rand(num_rows) < prob_ones_last3).astype(int)

    headers = [
        "Height (tall)",
        "Eye Color (blue)",
        "Skin Texture (smooth)",
        "Antenna Presence",
        "Wing Size (large)",
        "Telepathy Skill"
    ]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"CSV file '{filename}' created with {num_rows} rows.")

# Example usage:
# create_csv_dataset()
