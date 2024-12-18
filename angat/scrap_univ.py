from pandas import read_csv
import pandas as pd
from .models.AcedemicProgram import AcedemicProgram
from .models.University import University

last_univ = ''

def fill_na(univ):
    global last_univ
    if pd.isna(univ):
        return last_univ
    else:
        last_univ = univ
        return univ

def scrap_program_csv():
    df = read_csv('/Users/dev-01/dev/Projects/dash_rat/statics/Glovera - Template For 100x - Course Info.csv')
    
    df.drop(['Unnamed: 8', 'Unnamed: 13', 'Unnamed: 18', 'Unnamed: 24', 'Unnamed: 31', 'Unnamed: 39', 'Unnamed: 43'], axis=1, inplace=True)
    
    df['University '].fillna(method='ffill', inplace=True)
    df['College'].fillna(method='ffill', inplace=True)
    df['Location'].fillna(method='ffill', inplace=True)
    df['Public/Private'].fillna(method='ffill', inplace=True)
    df['Whats Special About this location'].fillna(method='ffill', inplace=True)
    df['Whats Special about this Univ/ College'].fillna(method='ffill', inplace=True)

    df.fillna("", inplace=True)

    print(df.shape)
    for _, row in df.iterrows():
        university = University.objects.filter(name=row['University '])
        if len(university) == 0:
            university = University.objects.create(
                name=row['University '],
                type=row['Public/Private'],
                location = row['Location'],
                location_details = row['Whats Special About this location'],
                usp = row['Whats Special about this Univ/ College'],
            )
        else:
            university = university[0]
        
        AcedemicProgram.objects.create(
            ranking = row['Ranking'],
            college = row['College'],
            university = university,
            name = row['Program Name'],
            usp = row['Top USP of this Program'], 
            specialization = row['Specialization/ Concentrations Possible'], 
            intern_or_co_op = row['Co-op/ Internship'], 
            curriculum_link = row['Curriculum'],
            cost = {
                "futurense_pricing": row['Futurense Pricing'],
                "original_pricing": row['Original Pricing']
            },
            credits = {
                'total_credits': row['Total Credits'],
                'iit_or_iim': row['IIT/IIM?'],
                'credit_in_iit_iim': row['Credits in IIT/IIM'],
                'credit_in_us': row['Credits in US'],
                'total_duration': row['Can finish in']
            },
            eligibility = {
                'ug_bacground': row['UG Background'],
                'min_gpa_perc': row['Minimum GPA or %'],
                'max_backlogs': row['Backlogs'],
                'work_exp': row['Work Experience'],
                'three_year_undergrad': row['Will allow 3 years undergrad candidates?'],
                'decision_factor': row['Decision Factor']
            },
            application_requirements = {
                'transcription_evaluation': row['Trasnscript Evaluation\n(NR - Not Required)'],
                'lor': row['LOR'],
                'sop': row['SOP'],
                'interviews': row['Interviews'],
                'deposit': row['Deposit'],
                'deposit_refundabe': row['Deposit\n(Refundable in case of visa rejection)']
            },
            placement_details = {
                'co-op': row['Co-op'],
                'key_companies': row['Key Companies Hiring'],
                'key_job_roles': row['Key Job Roles']
            },
            study_type = row['Quant/ Qualitative']
        )