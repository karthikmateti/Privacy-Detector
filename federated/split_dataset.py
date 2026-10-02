import os
import pandas as pd
from sklearn.model_selection import train_test_split

# ==========================================================
# FEDERATED DATASET SPLITTING
# ==========================================================

INPUT_DATASET = "adult.csv"

CLIENT_FOLDER = "federated/clients"

os.makedirs(CLIENT_FOLDER, exist_ok=True)

print("=" * 70)
print("FEDERATED DATASET SPLITTING")
print("=" * 70)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv(INPUT_DATASET)

print("\nOriginal Dataset Shape")

print(df.shape)

# ----------------------------------------------------------
# Shuffle Dataset
# ----------------------------------------------------------

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

# ----------------------------------------------------------
# Split Dataset
# ----------------------------------------------------------

client1, temp = train_test_split(
    df,
    test_size=0.67,
    random_state=42
)

client2, client3 = train_test_split(
    temp,
    test_size=0.50,
    random_state=42
)

# ----------------------------------------------------------
# Save Client Datasets
# ----------------------------------------------------------

client1.to_csv(
    os.path.join(CLIENT_FOLDER, "client1.csv"),
    index=False
)

client2.to_csv(
    os.path.join(CLIENT_FOLDER, "client2.csv"),
    index=False
)

client3.to_csv(
    os.path.join(CLIENT_FOLDER, "client3.csv"),
    index=False
)

print("\nDataset Successfully Split\n")

print(f"Client 1 : {client1.shape}")

print(f"Client 2 : {client2.shape}")

print(f"Client 3 : {client3.shape}")

print("\nSaved Inside")

print(CLIENT_FOLDER)

print("=" * 70)