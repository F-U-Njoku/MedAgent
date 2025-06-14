import requests
import json
from typing import Optional, Dict, List, Union
from urllib.parse import urlencode
import time

class ClinicalTrialsAPI:
    """
    A comprehensive tool for interacting with the ClinicalTrials.gov API v2.0
    
    This tool provides methods to search for clinical trials, retrieve study details,
    and fetch various types of information from the ClinicalTrials.gov database.
    """
    
    def __init__(self, base_url: str = "https://clinicaltrials.gov/api/v2"):
        """
        Initialize the ClinicalTrials API client
        
        Args:
            base_url: Base URL for the ClinicalTrials.gov API (default: v2 API)
        Note: The classic API was retired in June 2024. This uses the new v2 API.
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ClinicalTrials-API-Tool/1.0',
            'Accept': 'application/json'
        })
    
    def test_api_connection(self) -> Dict:
        """
        Test the API connection with the working parameter format
        
        Returns:
            Dictionary with response details
        """
        endpoint = f"{self.base_url}/studies"
        test_params = {
            'query.cond': 'diabetes',
            'pageSize': 1,
            'format': 'json'
        }
        
        try:
            response = self.session.get(endpoint, params=test_params)
            return {
                'status_code': response.status_code,
                'url': response.url,
                'success': response.status_code == 200,
                'sample_content': response.text[:500] if response.text else None
            }
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def search_studies(self, 
                      query_term: Optional[str] = None,
                      condition: Optional[str] = None,
                      intervention: Optional[str] = None,
                      location: Optional[str] = None,
                      status: Optional[str] = None,
                      phase: Optional[str] = None,
                      study_type: Optional[str] = None,
                      page_size: int = 100,
                      page_token: Optional[str] = None,
                      format: str = "json",
                      fields: Optional[List[str]] = None) -> Dict:
        """
        Search for clinical studies using various criteria
        
        Args:
            query_term: Free text search term
            condition: Medical condition or disease
            intervention: Drug, device, or other intervention  
            location: Geographic location (city, state, country)
            status: Study status (e.g., 'Recruiting', 'Active, not recruiting', 'Completed')
            phase: Study phase (e.g., 'Phase 1', 'Phase 2', 'Phase 3')
            study_type: Type of study (e.g., 'Interventional', 'Observational')
            page_size: Number of results per page (max 1000)
            page_token: Token for pagination
            format: Response format ('json')
            fields: Specific fields to return
            
        Returns:
            Dictionary containing search results
        """
        endpoint = f"{self.base_url}/studies"
        params = {}
        
        # Use the working parameter format discovered from testing
        if query_term:
            params['query.term'] = query_term
        if condition:
            params['query.cond'] = condition
        if intervention:
            params['query.intr'] = intervention
        if location:
            params['query.locn'] = location
        if status:
            params['filter.overallStatus'] = status
        if phase:
            params['filter.phase'] = phase
        if study_type:
            params['filter.studyType'] = study_type
        
        params['pageSize'] = min(page_size, 1000)  # API limit
        if page_token:
            params['pageToken'] = page_token
        params['format'] = format
        
        if fields:
            params['fields'] = ','.join(fields)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json() if format == 'json' else response.text
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None), 'url': response.url if 'response' in locals() else endpoint}
    
    def get_study_details(self, nct_id: str, format: str = "json", fields: Optional[List[str]] = None) -> Dict:
        """
        Get detailed information about a specific study
        
        Args:
            nct_id: NCT identifier for the study (e.g., 'NCT12345678')
            format: Response format ('json', 'csv', 'tsv')
            fields: Specific fields to return
            
        Returns:
            Dictionary containing study details
        """
        endpoint = f"{self.base_url}/studies/{nct_id}"
        params = {'format': format}
        
        if fields:
            params['fields'] = ','.join(fields)
        
        try:
            response = self.session.get(endpoint, params=params, timeout=15)
            response.raise_for_status()
            return response.json() if format == 'json' else response.text
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}
    
    def get_study_fields(self) -> Dict:
        """
        Get list of available fields for studies
        
        Returns:
            Dictionary containing available fields and their descriptions
        """
        endpoint = f"{self.base_url}/studies/metadata"
        
        try:
            response = self.session.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}
    
    
    def get_studies_by_ids(self, nct_ids: List[str], format: str = "json", fields: Optional[List[str]] = None) -> Dict:
        """
        Get multiple studies by their NCT IDs
        
        Args:
            nct_ids: List of NCT identifiers
            format: Response format
            fields: Specific fields to return
            
        Returns:
            Dictionary containing study information
        """
        endpoint = f"{self.base_url}/studies"
        params = {
            'query.id': nct_ids,
            'format': format
        }
        
        if fields:
            params['fields'] = ','.join(fields)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json() if format == 'json' else response.text
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}
    
    def get_statistics(self, 
                      query_term: Optional[str] = None,
                      condition: Optional[str] = None,
                      intervention: Optional[str] = None) -> Dict:
        """
        Get statistics about studies matching criteria
        
        Args:
            query_term: Free text search term
            condition: Medical condition
            intervention: Intervention type
            
        Returns:
            Dictionary containing statistics
        """
        endpoint = f"{self.base_url}/stats"
        params = {}
        
       # Prefer query.term for broader matching
        if query_term:
            params['query.term'] = query_term
        elif condition:
            params['query.term'] = condition  # Fallback: treat condition as free text term
        if intervention:
            params['query.intr'] = intervention
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}
    
    def paginate_all_results(self, search_params: Dict, max_results: Optional[int] = None) -> List[Dict]:
        """
        Helper function to get all results across multiple pages
        
        Args:
            search_params: Parameters for the search_studies method
            max_results: Maximum number of results to retrieve (None for all)
            
        Returns:
            List of all study records
        """
        all_studies = []
        page_token = None
        total_retrieved = 0
        
        while True:
            # Add pagination parameters
            current_params = search_params.copy()
            if page_token:
                current_params['page_token'] = page_token
            
            # Make the API call
            response = self.search_studies(**current_params)
            
            if 'error' in response:
                break
            
            studies = response.get('studies', [])
            all_studies.extend(studies)
            total_retrieved += len(studies)
            
            # Check if we should stop
            if max_results and total_retrieved >= max_results:
                all_studies = all_studies[:max_results]
                break
            
            # Check for next page
            page_token = response.get('nextPageToken')
            if not page_token:
                break
            
            # Rate limiting - be respectful to the API
            time.sleep(0.1)
        
        return all_studies

# Example usage and helper functions
def create_clinical_trials_tool():
    """Factory function to create a ClinicalTrials API instance"""
    return ClinicalTrialsAPI()

def search_covid_trials():
    """Example: Search for COVID-19 related trials"""
    api = create_clinical_trials_tool()
    return api.search_studies(
        condition="COVID-19",
        status="Recruiting",
        page_size=50
    )

def search_cancer_immunotherapy():
    """Example: Search for cancer immunotherapy trials"""
    api = create_clinical_trials_tool()
    return api.search_studies(
        condition="cancer",
        intervention="immunotherapy",
        phase="Phase 2",
        page_size=25
    )

def get_trial_summary(nct_id: str):
    """Example: Get a summary of key fields for a specific trial"""
    api = create_clinical_trials_tool()
    key_fields = [
        "NCTId", "BriefTitle", "OfficialTitle", "OverallStatus", 
        "Phase", "StudyType", "Condition", "InterventionName",
        "PrimaryOutcome", "StartDate", "CompletionDate", "LocationCity",
        "LocationState", "LocationCountry"
    ]
    return api.get_study_details(nct_id, fields=key_fields)