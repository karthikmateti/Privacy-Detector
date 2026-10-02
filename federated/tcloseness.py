import pandas as pd
import numpy as np
import math
import sys


T_VALUE = 0.20
GROUPING_QI = ["age", "education"]


def load_files(input_file, analysis_file):
    print("\nLoading Files...")
    dataset = pd.read_csv(input_file)
    analysis = pd.read_csv(analysis_file)
    print("Dataset Loaded Successfully")
    return dataset, analysis


def get_qi_columns(analysis):
    qi = analysis[
        analysis["Category"].str.contains("QI", case=False)
    ]["Column"].tolist()
    return qi


def get_sa_columns(analysis):
    sa = analysis[
        analysis["Category"].str.contains("SA", case=False)
    ]["Column"].tolist()
    return sa


def create_equivalence_classes(dataset, qi_columns):
    grouping = []
    for col in GROUPING_QI:
        if col in qi_columns:
            grouping.append(col)
    if len(grouping) == 0:
        grouping = qi_columns
    print("\nCreating Equivalence Classes...")
    print("\nGrouping using:")
    for g in grouping:
        print("  •", g)
    groups = dataset.groupby(grouping)
    print("\nEquivalence Classes :", len(groups))
    return groups


def show_summary(dataset, qi_columns, sa_columns, groups):
    print("\n")
    print("=" * 70)
    print("T-CLOSENESS MODULE")
    print("=" * 70)
    print("\nDataset Shape")
    print(dataset.shape)
    print("\nQuasi Identifier Columns")
    for col in qi_columns:
        print("  •", col)
    print("\nSensitive Columns")
    for col in sa_columns:
        print("  •", col)
    print("\nTotal Equivalence Classes")
    print(len(groups))
    print("\nSample Groups")
    count = 0
    for name, group in groups:
        print("\n--------------------------------")
        print("Group :", name)
        print("Rows :", len(group))
        print(group.head())
        count += 1
        if count == 3:
            break


def global_distribution(dataset, sa_columns):
    print("\n")
    print("=" * 70)
    print("GLOBAL DISTRIBUTION")
    print("=" * 70)
    distributions = {}
    for sa in sa_columns:
        dist = dataset[sa].value_counts(normalize=True)
        distributions[sa] = dist
        print(f"\nSensitive Attribute : {sa}")
        print(dist)
    return distributions


def local_distribution(group, sa):
    return group[sa].value_counts(normalize=True)


def total_variation_distance(global_dist, local_dist):
    categories = set(global_dist.index).union(set(local_dist.index))
    distance = 0
    for value in categories:
        g = global_dist.get(value, 0)
        l = local_dist.get(value, 0)
        distance += abs(g - l)
    distance *= 0.5
    return distance


def t_closeness(groups, global_dist, sa_columns, t=T_VALUE):
    print("\n")
    print("=" * 70)
    print("T-CLOSENESS")
    print("=" * 70)
    passed = 0
    failed = 0
    results = []
    for group_name, group in groups:
        status = "PASS"
        distances = {}
        for sa in sa_columns:
            local = local_distribution(group, sa)
            distance = total_variation_distance(global_dist[sa], local)
            distances[sa] = round(distance, 4)
            if distance > t:
                status = "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        results.append({
            "Group": group_name,
            "Status": status,
            "Distance": distances
        })
    print(f"\nThreshold : {t}")
    print(f"Groups Passed : {passed}")
    print(f"Groups Failed : {failed}")
    return results


def enforce_tcloseness(dataset, groups, results, sa_columns):
    print("\n")
    print("=" * 70)
    print("ENFORCING T-CLOSENESS")
    print("=" * 70)
    protected = dataset.copy()
    suppressed = 0
    for result, (_, indices) in zip(results, groups.groups.items()):
        if result["Status"] == "FAIL":
            for sa in sa_columns:
                protected.loc[indices, sa] = "Suppressed"
                suppressed += len(indices)
    print("Suppressed Values :", suppressed)
    return protected


def generate_report(dataset, qi_columns, sa_columns, results, report_file, t=T_VALUE):
    passed = sum(r["Status"] == "PASS" for r in results)
    failed = len(results) - passed
    distances = []
    for r in results:
        for d in r["Distance"].values():
            distances.append(d)
    avg_distance = sum(distances) / len(distances) if distances else 0
    max_distance = max(distances) if distances else 0
    with open(report_file, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("T-CLOSENESS REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Dataset Shape : {dataset.shape}\n\n")
        f.write("Quasi Identifier Columns\n")
        f.write("----------------------------\n")
        for q in qi_columns:
            f.write(q + "\n")
        f.write("\nSensitive Attributes\n")
        f.write("----------------------------\n")
        for s in sa_columns:
            f.write(s + "\n")
        f.write("\n")
        f.write(f"Threshold : {t}\n")
        f.write(f"Total Groups : {len(results)}\n")
        f.write(f"Passed Groups : {passed}\n")
        f.write(f"Failed Groups : {failed}\n\n")
        f.write(f"Average Distance : {avg_distance:.4f}\n")
        f.write(f"Maximum Distance : {max_distance:.4f}\n")
    print("\nReport Saved :", report_file)


def apply_tcloseness(input_file: str, analysis_file: str, output_file: str, report_file: str):
    dataset, analysis = load_files(input_file, analysis_file)
    qi_columns = get_qi_columns(analysis)
    sa_columns = get_sa_columns(analysis)
    groups = create_equivalence_classes(dataset, qi_columns)
    show_summary(dataset, qi_columns, sa_columns, groups)
    global_dist = global_distribution(dataset, sa_columns)
    groups = create_equivalence_classes(dataset, qi_columns)
    results = t_closeness(groups, global_dist, sa_columns)
    protected_dataset = enforce_tcloseness(dataset, groups, results, sa_columns)
    protected_dataset.to_csv(output_file, index=False)
    print("\nSaved :", output_file)
    generate_report(protected_dataset, qi_columns, sa_columns, results, report_file)


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "adult_ldiversity.csv"
    analysis_file = sys.argv[2] if len(sys.argv) > 2 else "adult_privacy_analysis.csv"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "adult_tcloseness.csv"
    report_file = sys.argv[4] if len(sys.argv) > 4 else "tcloseness_report.txt"
    apply_tcloseness(input_file, analysis_file, output_file, report_file)


if __name__ == "__main__":
    main()