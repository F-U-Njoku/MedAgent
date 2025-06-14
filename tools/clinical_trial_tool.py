from langchain.tools import Tool
from tools.clinical_trials_api import ClinicalTrialsAPI

def get_clinical_trials_tool():
    api = ClinicalTrialsAPI()

    def trial_search(query: str) -> str:
        results = api.search_studies(query_term=query, page_size=5)
        studies = results.get("studies", [])
        if not studies:
            return f"No trials found for '{query}'"
        
        formatted = []
        for s in studies[:5]:
            try:
                title = s["protocolSection"]["identificationModule"].get("briefTitle", "No Title")
                nct = s["protocolSection"]["identificationModule"]["nctId"]
                status = s["protocolSection"]["statusModule"].get("overallStatus", "Unknown")
                formatted.append(f"• {title} (NCT: {nct}) — Status: {status}")
            except Exception:
                continue
        return "\n".join(formatted)

    return Tool(
        name="ClinicalTrialsSearch",
        func=trial_search,
        description="Useful for finding clinical trials related to a drug or condition."
    )
