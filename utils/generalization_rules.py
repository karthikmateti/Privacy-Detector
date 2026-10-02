"""
Generalization Rules for k-Anonymity
"""

# -----------------------------
# Education
# -----------------------------

education_map = {

    "Preschool": "School",
    "1st-4th": "School",
    "5th-6th": "School",
    "7th-8th": "School",
    "9th": "School",
    "10th": "School",
    "11th": "School",
    "12th": "School",
    "HS-grad": "School",

    "Some-college": "College",

    "Assoc-acdm": "Undergraduate",
    "Assoc-voc": "Undergraduate",
    "Bachelors": "Undergraduate",

    "Masters": "Postgraduate",
    "Prof-school": "Postgraduate",

    "Doctorate": "Doctorate"
}

# -----------------------------
# Occupation
# -----------------------------

occupation_map = {

    "Tech-support": "Technical",
    "Craft-repair": "Technical",
    "Machine-op-inspct": "Technical",

    "Exec-managerial": "Management",

    "Sales": "Business",

    "Adm-clerical": "Office",

    "Prof-specialty": "Professional",

    "Protective-serv": "Government",

    "Transport-moving": "Transportation",

    "Farming-fishing": "Agriculture",

    "Other-service": "Service",

    "Handlers-cleaners": "Service",

    "Priv-house-serv": "Service"
}

# -----------------------------
# Country
# -----------------------------

country_map = {

    "India": "Asia",
    "China": "Asia",
    "Japan": "Asia",
    "Philippines": "Asia",
    "Vietnam": "Asia",

    "England": "Europe",
    "Germany": "Europe",
    "France": "Europe",
    "Italy": "Europe",
    "Poland": "Europe",

    "United-States": "North America",
    "Canada": "North America",
    "Mexico": "North America",

    "Brazil": "South America",
    "Columbia": "South America",

    "South": "Asia"
}