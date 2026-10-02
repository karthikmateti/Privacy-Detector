import re

# Every keyword list used during training
DI_KW  = set(["name","fullname","first_name","last_name","email","mail","phone","mobile",
               "ssn","social_security","tax_id","tin","national_id","nid","aadhaar","pan",
               "passport","license","voter","address","street","ip","mac","device","imei",
               "user_id","userid","username","account","card","credit","cvv","pin","dob",
               "date_of_birth","birthdate","employee_id","emp_id","staff_id","student_id",
               "patient_id","mrn","policy_number","vehicle","vin","biometric","fingerprint",
               "latitude","longitude","gps","customer_id","client_id","member_id","health_id"])

QI_KW  = set(["age","gender","sex","race","ethnicity","nationality","zip","zipcode","postal",
               "postcode","city","town","state","province","region","country","marital",
               "married","education","degree","qualification","occupation","job","profession",
               "employment","industry","sector","birth_year","year_of_birth","birth_month",
               "household","family_size","children","dependents","religion","caste","tribe",
               "language","citizenship","residence","visa","weight","height","bmi","blood_type",
               "blood_group","disability","veteran","military","housing","income_bracket",
               "salary_band","socioeconomic","experience","work_experience"])

SA_KW  = set(["salary","income","wage","earnings","compensation","bonus","commission",
               "credit_score","cibil","fico","credit_rating","loan","debt","mortgage",
               "balance","savings","net_worth","assets","tax_paid","penalty","fine",
               "diagnosis","disease","illness","disorder","hiv","cancer","diabetes",
               "blood_pressure","cholesterol","medication","prescription","treatment",
               "surgery","test_result","lab_result","mental_health","depression","anxiety",
               "psychiatric","substance_use","alcohol","drug_use","smoking","pregnancy",
               "criminal","arrest","conviction","felony","political","vote","sexual_orientation",
               "performance_rating","performance_score","appraisal","gpa","grade","marks",
               "score","exam_result","insurance_claim","welfare","subsidy","investment",
               "property_value","bankruptcy","insolvency","default"])

def tokenise(col_name: str):
    """Split 'first_name' → ['first', 'name'], 'dob' → ['dob']"""
    c = col_name.lower().strip()
    tokens = set(re.split(r'[_\-\.\s]+', c))
    tokens.add(c)   # also check the full string
    return tokens

def extract_features(col_name: str) -> dict:
    tokens = tokenise(col_name)
    c = col_name.lower()

    di_hit  = int(bool(tokens & DI_KW))
    qi_hit  = int(bool(tokens & QI_KW))
    sa_hit  = int(bool(tokens & SA_KW))

    # Substring checks (catches 'email_address', 'phone_no', etc.)
    di_sub  = int(any(k in c for k in DI_KW))
    qi_sub  = int(any(k in c for k in QI_KW))
    sa_sub  = int(any(k in c for k in SA_KW))

    # Length and structural signals
    num_tokens   = len(re.split(r'[_\-\.\s]+', c))
    col_length   = len(c)
    has_number   = int(bool(re.search(r'\d', c)))
    ends_id      = int(c.endswith(('_id','_no','_num','_number','id','no')))
    ends_date    = int(c.endswith(('_date','_at','_time','date','time')))
    ends_amount  = int(c.endswith(('_amount','_value','amount','value','cost','price')))
    ends_status  = int(c.endswith(('_status','_flag','status','flag','type','code')))

    return {
        "di_exact":     di_hit,
        "qi_exact":     qi_hit,
        "sa_exact":     sa_hit,
        "di_substring": di_sub,
        "qi_substring": qi_sub,
        "sa_substring": sa_sub,
        "num_tokens":   num_tokens,
        "col_length":   col_length,
        "has_number":   has_number,
        "ends_id":      ends_id,
        "ends_date":    ends_date,
        "ends_amount":  ends_amount,
        "ends_status":  ends_status,
    }