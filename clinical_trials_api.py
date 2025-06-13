import requests

def fetch_trials(drug_name, max_results=3):
    base_url = "https://clinicaltrials.gov/api/query/study_fields"
    params = {
        "expr": drug_name,
        "fields": "NCTId,BriefTitle,Status,Condition",
        "min_rnk": 1,
        "max_rnk": max_results,
        "fmt": "json"
    }
    response = requests.get(base_url, params=params)
    studies = response.json()["StudyFieldsResponse"]["StudyFields"]

    summaries = []
    for study in studies:
        title = study.get("BriefTitle", [""])[0]
        status = study.get("Status", [""])[0]
        condition = study.get("Condition", [""])[0]
        nct = study.get("NCTId", [""])[0]
        summaries.append(f"- {title} ({status}, NCT: {nct}, Condition: {condition})")
    
    return summaries

if __name__ == "__main__":
    fetch_trials("Ibuprofen")