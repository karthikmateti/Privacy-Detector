# Privacy-Preserving Data Publishing Using XGBoost and Federated Learning

An end-to-end research framework for privacy-preserving data publishing that integrates automated privacy attribute detection, data anonymization, federated learning, differential privacy, privacy validation, and privacy-utility analysis.

The framework uses XGBoost to classify dataset attributes into Direct Identifiers (DI), Quasi-Identifiers (QI), Sensitive Attributes (SA), and Non-Sensitive (NS) attributes. It then applies k-Anonymity, l-Diversity, and t-Closeness, together with Differential Privacy in the federated learning pipeline.

---

## Overview

This project implements an integrated privacy-preserving pipeline that automatically identifies privacy-sensitive attributes and applies multiple privacy-preserving mechanisms before data publication or machine-learning usage.

### Main Components

- XGBoost-based privacy attribute detection
- k-Anonymity
- l-Diversity
- t-Closeness
- Federated Learning
- Differential Privacy
- Privacy validation
- Information-loss analysis
- Machine-learning utility evaluation
- Privacy-utility visualization

---

## System Architecture

```text
                         Input Dataset
                               |
                               v
                       Data Preprocessing
                               |
                               v
                  +--------------------------+
                  |    PROPOSED FRAMEWORK    |
                  |                          |
                  | XGBoost Privacy Attribute|
                  | Detection                |
                  | DI / QI / SA / NS        |
                  |           |              |
                  |           v              |
                  | Privacy Preservation     |
                  | k-Anonymity              |
                  | l-Diversity              |
                  | t-Closeness              |
                  | Differential Privacy     |
                  |           |              |
                  |           v              |
                  | Federated Learning       |
                  | Local Training -> DP ->  |
                  | Aggregation              |
                  |           |              |
                  |           v              |
                  | Privacy Validation &     |
                  | Information Loss Analysis|
                  +-------------|------------+
                                |
                                v
                     Privacy-Preserved Dataset
                         / Global Model
```

---

## Key Features

### Automated Privacy Attribute Detection

XGBoost classifies dataset attributes into:

| Category | Description |
|---|---|
| DI | Direct Identifier |
| QI | Quasi-Identifier |
| SA | Sensitive Attribute |
| NS | Non-Sensitive |

### k-Anonymity

The framework creates equivalence classes and applies generalization and suppression to satisfy the selected k-anonymity requirement.

### l-Diversity

The implementation supports:

- Distinct l-Diversity
- Entropy l-Diversity
- Recursive (c,l)-Diversity

### t-Closeness

t-Closeness compares local sensitive-attribute distributions with the global distribution using Total Variation Distance (TVD).

The implementation uses a default threshold:

```text
t = 0.2
```

### Federated Learning

The framework supports multiple local clients:

```text
Dataset
   |
   +-- Client 1
   +-- Client 2
   +-- Client 3
          |
          v
    Local Training
          |
          v
 Differential Privacy
          |
          v
 Model Aggregation
          |
          v
     Global Model
```

### Differential Privacy

Differential Privacy is incorporated into the federated learning pipeline by adding calibrated noise to model updates before aggregation.

### Privacy Validation

The framework validates:

- k-Anonymity
- Distinct l-Diversity
- Entropy l-Diversity
- Recursive (c,l)-Diversity
- t-Closeness

### Information Loss Analysis

The framework evaluates:

- Normalized Certainty Penalty (NCP)
- Discernibility Metric (DM)
- Generalization Percentage
- Suppression Percentage
- Utility Loss
- Overall Information Loss Score

---

## Dataset

The primary dataset used for evaluation is the Adult Income Dataset, also known as the Census Income dataset.

### Dataset Characteristics

- Rows: 32,561
- Attributes: 15
- Sensitive Attribute: `income`

Example privacy categories:

```text
QI:
    age
    education
    occupation
    marital-status
    relationship
    race
    sex
    native-country

SA:
    income

NS:
    workclass
    fnlwgt
    capital-gain
    capital-loss
    hours-per-week
```

---

## Privacy Attribute Detection

The privacy detector uses feature engineering based on dataset column names.

### Extracted Features

#### Keyword Features

- Exact keyword matches
- Substring keyword matches
- DI keyword indicators
- QI keyword indicators
- SA keyword indicators

#### Structural Features

- Number of tokens
- Column-name length
- Presence of numbers
- Identifier suffix
- Date suffix
- Amount suffix
- Status suffix

These features are provided to an XGBoost multi-class classifier.

---

## Project Structure

```text
Privacy-Detector/
|
+-- data/
|   +-- adult.csv
|   +-- training_labels.csv
|
+-- models/
|   +-- privacy_model.pkl
|   +-- feature_names.csv
|
+-- privacy/
|   +-- kanonymity.py
|   +-- ldiversity.py
|   +-- tcloseness.py
|   +-- privacy_validator.py
|   +-- information_loss.py
|
+-- federated/
|   +-- split_dataset.py
|   +-- client.py
|   +-- server.py
|   +-- aggregate.py
|   +-- clients/
|   +-- models/
|
+-- utils/
|   +-- feature_extractor.py
|   +-- generalization_rules.py
|   +-- visualizations.py
|
+-- outputs/
+-- reports/
+-- plots/
+-- generate_data.py
+-- train_model.py
+-- predict.py
+-- requirements.txt
+-- README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/karthikmateti/Privacy-Detector.git
cd Privacy-Detector
```

### Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Execution Pipeline

## Step 1: Generate Training Data

```bash
python generate_data.py
```

Generates:

```text
data/training_labels.csv
```

## Step 2: Train the XGBoost Privacy Detector

```bash
python train_model.py
```

Generated model:

```text
models/privacy_model.pkl
```

Feature names:

```text
models/feature_names.csv
```

## Step 3: Detect Privacy Attributes

```bash
python predict.py data/adult.csv
```

Output:

```text
outputs/adult_privacy_analysis.csv
```

The output contains:

```text
Column
Category
Confidence
```

---

# Privacy Preservation Pipeline

## Step 4: Apply k-Anonymity

```bash
python privacy/kanonymity.py data/adult.csv outputs/adult_privacy_analysis.csv outputs/adult_anonymized.csv
```

## Step 5: Apply l-Diversity

```bash
python privacy/ldiversity.py outputs/adult_anonymized.csv outputs/adult_privacy_analysis.csv outputs/adult_ldiversity.csv reports/ldiversity_report.txt
```

## Step 6: Apply t-Closeness

```bash
python privacy/tcloseness.py outputs/adult_ldiversity.csv outputs/adult_privacy_analysis.csv outputs/adult_tcloseness.csv reports/tcloseness_report.txt
```

---

# Privacy Validation

```bash
python privacy/privacy_validator.py outputs/adult_tcloseness.csv outputs/adult_privacy_analysis.csv reports/privacy_validation_report.txt
```

The validation report contains:

- k-Anonymity results
- Distinct l-Diversity results
- Entropy l-Diversity results
- Recursive l-Diversity results
- t-Closeness results
- Overall privacy score

---

# Information Loss Analysis

```bash
python privacy/information_loss.py data/adult.csv outputs/adult_tcloseness.csv outputs/adult_privacy_analysis.csv reports/information_loss_report.txt
```

The module evaluates:

- Normalized Certainty Penalty
- Discernibility Metric
- Generalization Percentage
- Suppression Percentage
- Utility Loss
- Overall Information Loss

---

# Federated Learning Pipeline

## Split the Dataset

```bash
python federated/split_dataset.py
```

The dataset is divided into three clients:

```text
Client 1
Client 2
Client 3
```

Each client performs local processing and model training.

```text
k-Anonymity
     |
l-Diversity
     |
t-Closeness
     |
Differential Privacy
     |
Local Model
```

## Model Aggregation

```bash
python federated/aggregate.py
```

The global model is stored at:

```text
federated/models/global_model.pkl
```

---

# End-to-End Workflow

```text
Raw Dataset
     |
     v
Data Preprocessing
     |
     v
Feature Extraction
     |
     v
XGBoost Privacy Attribute Detection
     |
     +-- DI
     +-- QI
     +-- SA
     +-- NS
     |
     v
k-Anonymity
     |
     v
l-Diversity
     |
     v
t-Closeness
     |
     v
Differential Privacy
     |
     v
Federated Local Training
     |
     v
Model Aggregation
     |
     v
Privacy Validation
     |
     v
Information Loss Analysis
     |
     v
Utility Evaluation
     |
     v
Privacy-Preserved Dataset / Global Model
```

---

# Experimental Results

## Privacy Validation Results

| Metric | Result |
|---|---:|
| k-Anonymity Passed | 41 groups |
| k-Anonymity Failed | 2 groups |
| Distinct l-Diversity Passed | 21 groups |
| Distinct l-Diversity Failed | 22 groups |
| Entropy l-Diversity Passed | 6 groups |
| Entropy l-Diversity Failed | 37 groups |
| Recursive l-Diversity Passed | 3 groups |
| Recursive l-Diversity Failed | 40 groups |
| Overall Privacy Score | 41.28% |

## Information Loss Results

| Metric | Result |
|---|---:|
| NCP | 0.5561 |
| Generalization | 65.35% |
| Suppression | 4.04% |
| DM | 67.5240 |
| Overall Information Loss | 0.3896 |

## Machine Learning Utility Results

| Metric | Original Dataset | Anonymized Dataset |
|---|---:|---:|
| Accuracy | 86.86% | 84.59% |
| Precision | 86.33% | 84.17% |
| Recall | 86.86% | 84.59% |
| F1-Score | 86.15% | 82.57% |

### Utility Loss

| Metric | Loss |
|---|---:|
| Accuracy | 2.26% |
| Precision | 2.16% |
| Recall | 2.26% |
| F1-Score | 3.58% |

These results illustrate the privacy-utility trade-off introduced by the anonymization process.

---

# Generated Reports

The framework generates detailed reports under the `reports/` directory.

### Privacy Validation Report

```text
reports/privacy_validation_report.txt
```

### l-Diversity Report

```text
reports/ldiversity_report.txt
```

### t-Closeness Report

```text
reports/tcloseness_report.txt
```

### Information Loss Report

```text
reports/information_loss_report.txt
```

---

# Visualizations

### Accuracy Comparison

```text
plots/accuracy_comparison.png
```

### Privacy vs. Utility

```text
plots/privacy_vs_utility.png
```

### Suppression vs. Generalization

```text
plots/suppression_generalization.png
```

---

# Research Contributions

1. **Automated Privacy Attribute Detection**  
   XGBoost is used to classify dataset attributes into DI, QI, SA, and NS categories.

2. **Multi-Level Data Anonymization**  
   k-Anonymity, l-Diversity, and t-Closeness are integrated into a sequential privacy-preservation pipeline.

3. **Federated Learning**  
   Distributed local processing and model training are supported across multiple clients.

4. **Differential Privacy**  
   Differential Privacy is incorporated into the federated learning process for an additional protection layer.

5. **Privacy Validation**  
   Multiple privacy criteria are evaluated at the equivalence-class level.

6. **Information Loss Analysis**  
   The effect of anonymization on data utility is measured.

7. **Privacy-Utility Evaluation**  
   Machine-learning performance is compared between original and anonymized datasets.

---

# Technologies Used

### Programming

- Python

### Machine Learning

- XGBoost
- Scikit-learn
- Pandas
- NumPy

### Privacy Techniques

- k-Anonymity
- l-Diversity
- t-Closeness
- Differential Privacy

### Distributed Learning

- Federated Learning

### Visualization

- Matplotlib

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

# Advantages

- End-to-end privacy-preserving data processing
- Automated privacy attribute classification
- Multiple complementary anonymization techniques
- Federated learning support
- Differential privacy integration
- Privacy validation reports
- Information-loss analysis
- Machine-learning utility evaluation
- Privacy-utility visualization
- Modular architecture

---

# Limitations

The current implementation has the following limitations:

1. Generalization hierarchies are manually defined for supported attributes.
2. The primary experimental evaluation uses the Adult Income dataset.
3. The federated aggregation implementation is intended for research and demonstration purposes.
4. The overall privacy score uses weighted validation results.
5. The current implementation primarily evaluates a single sensitive-attribute configuration.

---

# Future Work

Potential extensions include:

- Automatic generation of generalization hierarchies
- Evaluation on additional datasets
- Full FedAvg implementation
- Adaptive privacy-parameter selection
- Support for multiple sensitive attributes
- Additional Differential Privacy mechanisms
- Synthetic data generation
- Secure aggregation
- Larger-scale federated experiments
- Statistical significance testing
- Interactive web-based interface
- Evaluation on healthcare and financial datasets
- Communication and computational overhead analysis

---

# Research Context

This project explores the integration of:

```text
Machine Learning
        +
Privacy-Preserving Data Publishing
        +
Federated Learning
        +
Differential Privacy
        +
Privacy Validation
        +
Information Loss Analysis
        +
Utility Evaluation
```

The framework is designed as a modular research implementation for studying privacy protection and its effect on downstream machine-learning utility.

---

# Author

**Mateti Karthik**

B.Tech in Computing and Data Science Sai University, Chennai, Tamil Nadu, India

**Dr Priyank Jain**

Assistant Professor, Department of Computer Science and Engineering 
IIIT Pune, India

### Research Interests

- Privacy-Preserving Machine Learning
- Federated Learning
- Differential Privacy
- Explainable AI
- Machine Learning
- Data Science
- Agentic AI

---

# Acknowledgement

This project was developed as a research-oriented implementation for studying privacy-preserving data publishing, distributed machine learning, and privacy-utility trade-offs.

If you find this project useful for research or educational purposes, consider giving the repository a ⭐.

---

# License

This project is intended primarily for academic and research purposes.

Please refer to the repository license for the applicable terms of use.
