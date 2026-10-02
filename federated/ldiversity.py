import pandas as pd
import numpy as np
import math
import os
import sys
from collections import Counter
MIN_GROUP_SIZE = 3

L_VALUE = 2
C_VALUE = 2


def load_files(anonymized_file, analysis_file):
    print("\nLoading Files...")
    dataset = pd.read_csv(anonymized_file)
    analysis = pd.read_csv(analysis_file)
    print("Dataset Loaded Successfully")
    return dataset, analysis


def get_qi_columns(analysis):
    qi = analysis[
        analysis["Category"].str.contains("QI", case=False)
    ]["Column"].tolist()
    return qi


def get_sensitive_columns(analysis, dataset):
    sa = analysis[
        analysis["Category"].str.contains("SA", case=False)
    ]["Column"].tolist()
    filtered = []
    for col in sa:
        if col not in dataset.columns:
            continue
        if pd.api.types.is_numeric_dtype(dataset[col]):
            unique = dataset[col].nunique()
            if unique > 20:
                continue
        filtered.append(col)
    return filtered


def create_equivalence_classes(dataset, qi_columns):
    print("\nCreating Equivalence Classes...")
    preferred_qi = ["age", "education"]
    grouping_columns = []
    for col in preferred_qi:
        if col in qi_columns:
            grouping_columns.append(col)
    if len(grouping_columns) == 0:
        grouping_columns = qi_columns
    print("\nGrouping using:")
    for col in grouping_columns:
        print("  •", col)
    groups = dataset.groupby(grouping_columns)
    print("\nEquivalence Classes :", groups.ngroups)
    return groups


def show_information(dataset, qi_columns, sa_columns, groups):
    print("\n")
    print("=" * 70)
    print("L-DIVERSITY MODULE")
    print("=" * 70)
    print("\nDataset Shape")
    print(dataset.shape)
    print("\nQuasi Identifier Columns")
    for c in qi_columns:
        print("  •", c)
    print("\nSensitive Columns")
    for c in sa_columns:
        print("  •", c)
    print("\nTotal Equivalence Classes")
    print(groups.ngroups)
    print("\nSample Groups\n")
    count = 0
    for name, group in groups:
        print("-------------------------------------------")
        print("Group :", name)
        print("Rows :", len(group))
        print(group.head())
        count += 1
        if count == 3:
            break


def distinct_l_diversity(groups, sa_columns, l=L_VALUE):
    print("\n")
    print("=" * 70)
    print("DISTINCT L-DIVERSITY")
    print("=" * 70)
    results = []
    passed = 0
    failed = 0
    for group_name, group in groups:
        group_result = {
            "group": group_name,
            "status": "PASS",
            "details": {}
        }
        for sa in sa_columns:
            distinct_count = group[sa].nunique(dropna=True)
            group_result["details"][sa] = distinct_count
            if distinct_count < l:
                group_result["status"] = "FAIL"
        if group_result["status"] == "PASS":
            passed += 1
        else:
            failed += 1
        results.append(group_result)
    print(f"Groups Passed : {passed}")
    print(f"Groups Failed : {failed}")
    return results


def calculate_entropy(values):
    probs = values.value_counts(normalize=True)
    entropy = -sum(
        p * math.log2(p)
        for p in probs
        if p > 0
    )
    return entropy


def entropy_l_diversity(groups, sa_columns, l=L_VALUE):
    print("\n")
    print("=" * 70)
    print("ENTROPY L-DIVERSITY")
    print("=" * 70)
    threshold = math.log2(l)
    results = []
    passed = 0
    failed = 0
    for group_name, group in groups:
        group_result = {
            "group": group_name,
            "status": "PASS",
            "entropy": {}
        }
        for sa in sa_columns:
            entropy = calculate_entropy(group[sa])
            group_result["entropy"][sa] = round(entropy, 4)
            distinct_values = group[sa].nunique()
            if distinct_values <= 1:
                normalized_entropy = 0
            else:
                max_entropy = math.log2(distinct_values)
                normalized_entropy = entropy / max_entropy
            group_result["normalized_entropy"] = round(normalized_entropy, 4)
            if normalized_entropy < 0.90:
                group_result["status"] = "FAIL"
        if group_result["status"] == "PASS":
            passed += 1
        else:
            failed += 1
        results.append(group_result)
    print("Normalized Entropy Threshold : 0.90")
    print(f"Groups Passed : {passed}")
    print(f"Groups Failed : {failed}")
    return results


def recursive_cl_diversity(groups, sa_columns, l=L_VALUE, c=C_VALUE):
    print("\n")
    print("=" * 70)
    print("RECURSIVE (c,l)-DIVERSITY")
    print("=" * 70)
    results = []
    passed = 0
    failed = 0
    for group_name, group in groups:
        status = "PASS"
        details = {}
        for sa in sa_columns:
            freq = group[sa].value_counts().sort_values(ascending=False)
            if len(freq) < l:
                status = "FAIL"
                details[sa] = "Less than l distinct values"
                continue
            r1 = freq.iloc[0]
            remaining = freq.iloc[1:].sum()
            recursive_condition = r1 < c * remaining
            details[sa] = {
                "Largest Frequency": int(r1),
                "Remaining Frequency": int(remaining),
                "Satisfied": recursive_condition
            }
            if not recursive_condition:
                status = "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        results.append({
            "Group": group_name,
            "Status": status,
            "Details": details
        })
    print(f"Groups Passed : {passed}")
    print(f"Groups Failed : {failed}")
    return results


def enforce_ldiversity(dataset, qi_columns, sa_columns, l=L_VALUE):
    print("\n")
    print("=" * 70)
    print("ENFORCING L-DIVERSITY")
    print("=" * 70)
    modified = dataset.copy()
    groups = create_equivalence_classes(modified, qi_columns)
    suppressed = 0
    for _, index in groups.groups.items():
        rows = modified.loc[index]
        for sa in sa_columns:
            distinct = rows[sa].nunique()
            if distinct < l:
                modified.loc[index, sa] = "Suppressed"
                suppressed += len(index)
    print("Suppressed Values :", suppressed)
    return modified


def generate_report(dataset, qi_columns, sa_columns, distinct_results, entropy_results, recursive_results, report_file):
    distinct_pass = sum(r["status"] == "PASS" for r in distinct_results)
    distinct_fail = len(distinct_results) - distinct_pass
    entropy_pass = sum(r["status"] == "PASS" for r in entropy_results)
    entropy_fail = len(entropy_results) - entropy_pass
    recursive_pass = sum(r["Status"] == "PASS" for r in recursive_results)
    recursive_fail = len(recursive_results) - recursive_pass
    with open(report_file, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("L-DIVERSITY REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Dataset Shape : {dataset.shape}\n\n")
        f.write("Quasi Identifier Columns\n")
        f.write("----------------------------\n")
        for col in qi_columns:
            f.write(col + "\n")
        f.write("\nSensitive Columns\n")
        f.write("----------------------------\n")
        for col in sa_columns:
            f.write(col + "\n")
        f.write("\n")
        f.write("=" * 50 + "\n")
        f.write("Distinct l-Diversity\n")
        f.write("=" * 50 + "\n")
        f.write(f"Passed : {distinct_pass}\n")
        f.write(f"Failed : {distinct_fail}\n\n")
        f.write("=" * 50 + "\n")
        f.write("Entropy l-Diversity\n")
        f.write("=" * 50 + "\n")
        f.write(f"Passed : {entropy_pass}\n")
        f.write(f"Failed : {entropy_fail}\n\n")
        f.write("=" * 50 + "\n")
        f.write("Recursive (c,l)-Diversity\n")
        f.write("=" * 50 + "\n")
        f.write(f"Passed : {recursive_pass}\n")
        f.write(f"Failed : {recursive_fail}\n\n")
        score = (
            distinct_pass +
            entropy_pass +
            recursive_pass
        ) / (
            len(distinct_results) +
            len(entropy_results) +
            len(recursive_results)
        ) * 100
        f.write("=" * 50 + "\n")
        f.write("Overall Privacy Score\n")
        f.write("=" * 50 + "\n")
        f.write(f"{score:.2f}%\n")
        if score >= 80:
            level = "HIGH"
        elif score >= 60:
            level = "MEDIUM"
        else:
            level = "LOW"
        f.write(f"Privacy Level : {level}\n")
    print("\nReport saved :", report_file)


def apply_ldiversity(anonymized_file: str, analysis_file: str, output_file: str, report_file: str):
    dataset, analysis = load_files(anonymized_file, analysis_file)
    qi_columns = get_qi_columns(analysis)
    sa_columns = get_sensitive_columns(analysis, dataset)
    groups = create_equivalence_classes(dataset, qi_columns)
    show_information(dataset, qi_columns, sa_columns, groups)
    distinct_results = distinct_l_diversity(groups, sa_columns)
    groups = create_equivalence_classes(dataset, qi_columns)
    entropy_results = entropy_l_diversity(groups, sa_columns)
    groups = create_equivalence_classes(dataset, qi_columns)
    recursive_results = recursive_cl_diversity(groups, sa_columns)
    modified_dataset = enforce_ldiversity(dataset, qi_columns, sa_columns)
    modified_dataset.to_csv(output_file, index=False)
    print("\nSaved :", output_file)
    generate_report(dataset, qi_columns, sa_columns, distinct_results, entropy_results, recursive_results, report_file)


def main():
    anonymized_file = sys.argv[1] if len(sys.argv) > 1 else "adult_anonymized.csv"
    analysis_file = sys.argv[2] if len(sys.argv) > 2 else "adult_privacy_analysis.csv"
    output_file = sys.argv[3] if len(sys.argv) > 3 else "adult_ldiversity.csv"
    report_file = sys.argv[4] if len(sys.argv) > 4 else "ldiversity_report.txt"
    apply_ldiversity(anonymized_file, analysis_file, output_file, report_file)


if __name__ == "__main__":
    main()