import pandas as pd

# Label encoding
DI = 0   # Direct Identifier
QI = 1   # Quasi-Identifier
SA = 2   # Sensitive Attribute
NS = 3   # Non-Sensitive

# Each row: (column_name, label)
# Covers: healthcare, finance, HR, education, e-commerce, government, telecom, insurance

RAW = [
    # ── DIRECT IDENTIFIERS ──────────────────────────────────────
    ("name", DI), ("full_name", DI), ("first_name", DI), ("last_name", DI),
    ("fname", DI), ("lname", DI), ("given_name", DI), ("surname", DI),
    ("email", DI), ("email_address", DI), ("mail", DI), ("e_mail", DI),
    ("phone", DI), ("phone_number", DI), ("mobile", DI), ("cell", DI),
    ("telephone", DI), ("contact_number", DI), ("fax", DI),
    ("ssn", DI), ("social_security", DI), ("social_security_number", DI),
    ("tax_id", DI), ("tin", DI), ("national_id", DI), ("nid", DI),
    ("aadhaar", DI), ("aadhaar_number", DI), ("pan", DI), ("pan_number", DI),
    ("passport", DI), ("passport_number", DI), ("passport_no", DI),
    ("drivers_license", DI), ("license_number", DI), ("dl_number", DI),
    ("voter_id", DI), ("voter_card", DI),
    ("address", DI), ("home_address", DI), ("street_address", DI),
    ("street", DI), ("address_line1", DI), ("address_line2", DI),
    ("ip_address", DI), ("ipv4", DI), ("ipv6", DI), ("mac_address", DI),
    ("device_id", DI), ("imei", DI), ("serial_number", DI),
    ("user_id", DI), ("userid", DI), ("username", DI), ("login", DI),
    ("account_number", DI), ("account_no", DI), ("bank_account", DI),
    ("credit_card", DI), ("card_number", DI), ("card_no", DI),
    ("cvv", DI), ("pin", DI), ("otp", DI),
    ("dob", DI), ("date_of_birth", DI), ("birth_date", DI), ("birthdate", DI),
    ("birth_place", DI), ("place_of_birth", DI),
    ("employee_id", DI), ("emp_id", DI), ("staff_id", DI),
    ("student_id", DI), ("roll_number", DI), ("enrollment_no", DI),
    ("patient_id", DI), ("mrn", DI), ("medical_record_number", DI),
    ("policy_number", DI), ("policy_no", DI), ("claim_id", DI),
    ("vehicle_number", DI), ("vin", DI), ("registration_number", DI),
    ("biometric", DI), ("fingerprint", DI), ("face_id", DI), ("iris", DI),
    ("gps_location", DI), ("latitude", DI), ("longitude", DI),
    ("customer_id", DI), ("client_id", DI), ("member_id", DI),
    ("nhs_number", DI), ("health_id", DI), ("eid", DI),

    # ── QUASI-IDENTIFIERS ────────────────────────────────────────
    ("age", QI), ("age_group", QI), ("age_range", QI), ("age_band", QI),
    ("gender", QI), ("sex", QI), ("gender_identity", QI),
    ("race", QI), ("ethnicity", QI), ("ethnic_group", QI), ("nationality", QI),
    ("zip", QI), ("zip_code", QI), ("zipcode", QI), ("postal_code", QI),
    ("postcode", QI), ("pin_code", QI),
    ("city", QI), ("town", QI), ("municipality", QI),
    ("state", QI), ("province", QI), ("region", QI), ("district", QI),
    ("country", QI), ("nation", QI),
    ("marital_status", QI), ("marital", QI), ("married", QI),
    ("education", QI), ("education_level", QI), ("degree", QI),
    ("qualification", QI), ("highest_qualification", QI),
    ("occupation", QI), ("job_title", QI), ("profession", QI),
    ("employment_status", QI), ("work_status", QI),
    ("industry", QI), ("sector", QI),
    ("birth_year", QI), ("year_of_birth", QI), ("birth_month", QI),
    ("household_size", QI), ("family_size", QI), ("num_children", QI),
    ("number_of_dependents", QI), ("dependents", QI),
    ("religion", QI), ("caste", QI), ("tribe", QI),
    ("language", QI), ("mother_tongue", QI), ("native_language", QI),
    ("citizenship", QI), ("residence_status", QI), ("visa_type", QI),
    ("weight", QI), ("height", QI), ("bmi", QI), ("body_mass_index", QI),
    ("blood_type", QI), ("blood_group", QI),
    ("disability_status", QI), ("handicap", QI),
    ("veteran_status", QI), ("military_status", QI),
    ("housing_type", QI), ("residence_type", QI), ("dwelling", QI),
    ("area_code", QI), ("county", QI), ("borough", QI),
    ("income_bracket", QI), ("income_range", QI), ("salary_band", QI),
    ("socioeconomic_status", QI), ("ses", QI),
    ("work_experience", QI), ("years_of_experience", QI),

    # ── SENSITIVE ATTRIBUTES ─────────────────────────────────────
    ("salary", SA), ("income", SA), ("annual_income", SA), ("monthly_income", SA),
    ("wage", SA), ("hourly_rate", SA), ("earnings", SA), ("net_salary", SA),
    ("gross_salary", SA), ("take_home", SA), ("compensation", SA),
    ("bonus", SA), ("commission", SA), ("overtime", SA),
    ("credit_score", SA), ("cibil_score", SA), ("fico_score", SA),
    ("credit_rating", SA), ("credit_risk", SA),
    ("loan_amount", SA), ("outstanding_loan", SA), ("debt", SA),
    ("mortgage", SA), ("emi", SA), ("balance", SA), ("bank_balance", SA),
    ("savings", SA), ("net_worth", SA), ("assets", SA), ("liabilities", SA),
    ("tax_paid", SA), ("tax_amount", SA), ("tax_bracket", SA),
    ("penalty", SA), ("fine", SA),
    ("diagnosis", SA), ("medical_condition", SA), ("disease", SA),
    ("illness", SA), ("disorder", SA), ("syndrome", SA),
    ("hiv_status", SA), ("aids", SA), ("cancer_type", SA),
    ("diabetes_type", SA), ("blood_pressure", SA), ("cholesterol", SA),
    ("medication", SA), ("prescription", SA), ("drug_name", SA),
    ("treatment", SA), ("therapy", SA), ("surgery", SA),
    ("test_result", SA), ("lab_result", SA), ("pathology_result", SA),
    ("mental_health", SA), ("depression", SA), ("anxiety", SA),
    ("psychiatric_condition", SA), ("psychological_condition", SA),
    ("substance_use", SA), ("alcohol_use", SA), ("drug_use", SA),
    ("smoking_status", SA), ("tobacco_use", SA),
    ("pregnancy", SA), ("reproductive_health", SA),
    ("criminal_record", SA), ("arrest", SA), ("conviction", SA),
    ("felony", SA), ("misdemeanor", SA), ("offense", SA),
    ("political_affiliation", SA), ("political_party", SA), ("vote", SA),
    ("sexual_orientation", SA), ("lgbtq_status", SA),
    ("performance_rating", SA), ("performance_score", SA),
    ("appraisal", SA), ("review_score", SA),
    ("gpa", SA), ("grade", SA), ("marks", SA), ("score", SA),
    ("exam_result", SA), ("test_score", SA), ("academic_result", SA),
    ("insurance_claim", SA), ("claim_amount", SA), ("payout", SA),
    ("welfare_benefit", SA), ("subsidy", SA), ("social_security_benefit", SA),
    ("investment", SA), ("portfolio_value", SA), ("stock_holdings", SA),
    ("property_value", SA), ("real_estate", SA),
    ("bankruptcy", SA), ("insolvency", SA), ("default", SA),

    # ── NON-SENSITIVE ────────────────────────────────────────────
    ("id", NS), ("row_id", NS), ("record_id", NS), ("index", NS),
    ("idx", NS), ("seq", NS), ("sequence_number", NS), ("serial", NS),
    ("created_at", NS), ("updated_at", NS), ("timestamp", NS),
    ("created_date", NS), ("modified_date", NS), ("last_updated", NS),
    ("date", NS), ("time", NS), ("datetime", NS),
    ("year", NS), ("month", NS), ("day", NS), ("week", NS),
    ("product_id", NS), ("item_id", NS), ("sku", NS), ("product_code", NS),
    ("product_name", NS), ("item_name", NS), ("product_category", NS),
    ("category", NS), ("subcategory", NS), ("department", NS),
    ("brand", NS), ("manufacturer", NS), ("model", NS),
    ("order_id", NS), ("transaction_id", NS), ("invoice_id", NS),
    ("receipt_number", NS), ("booking_id", NS), ("reservation_id", NS),
    ("quantity", NS), ("units", NS), ("count", NS), ("total", NS),
    ("amount", NS), ("price", NS), ("cost", NS), ("fee", NS),
    ("discount", NS), ("tax", NS), ("vat", NS), ("gst", NS),
    ("rating", NS), ("review", NS), ("feedback", NS), ("comment", NS),
    ("status", NS), ("flag", NS), ("is_active", NS), ("is_deleted", NS),
    ("enabled", NS), ("approved", NS), ("verified", NS),
    ("version", NS), ("revision", NS), ("build_number", NS),
    ("session_id", NS), ("log_id", NS), ("event_id", NS),
    ("page_views", NS), ("clicks", NS), ("impressions", NS),
    ("conversion", NS), ("bounce_rate", NS), ("ctr", NS),
    ("latitude_zone", NS), ("region_code", NS), ("area_name", NS),
    ("store_id", NS), ("branch_id", NS), ("outlet_id", NS),
    ("channel", NS), ("source", NS), ("medium", NS), ("campaign", NS),
    ("tag", NS), ("label", NS), ("type", NS), ("class", NS),
    ("priority", NS), ("severity", NS), ("level", NS),
    ("duration", NS), ("frequency", NS), ("interval", NS),
    ("file_name", NS), ("file_type", NS), ("extension", NS),
    ("language_code", NS), ("locale", NS), ("timezone", NS),
    ("currency", NS), ("exchange_rate", NS),
    ("color", NS), ("size", NS), ("weight_kg", NS), ("dimension", NS),
    ("description", NS), ("notes", NS), ("remarks", NS), ("summary", NS),
    ("target", NS), ("output", NS), ("prediction", NS), ("class_label", NS),
]

# ==========================================
# AUTO DATA AUGMENTATION
# ==========================================

def generate_variations(base_name):
    return list(set([
        base_name,
        f"employee_{base_name}",
        f"staff_{base_name}",
        f"user_{base_name}",
        f"customer_{base_name}",
        f"patient_{base_name}",
        f"{base_name}_id",
        f"{base_name}_number",
        f"{base_name}_code",
        f"{base_name}_value",
        f"{base_name}_amount",
        f"{base_name}_details",
        f"{base_name}_info",
        f"{base_name}_data",
        f"monthly_{base_name}",
        f"annual_{base_name}",
        f"current_{base_name}",
        f"previous_{base_name}",
        f"new_{base_name}",
        f"old_{base_name}"
    ]))

extra_rows = []

for col, label in RAW:
    for v in generate_variations(col):
        extra_rows.append((v, label))

RAW.extend(extra_rows)

# Build dataframe
df = pd.DataFrame(RAW, columns=["column_name", "label"])
df.to_csv("training_labels.csv", index=False)
print(f"Generated {len(df)} labelled rows")
print(df["label"].value_counts().rename({0:"DI",1:"QI",2:"SA",3:"NS"}))