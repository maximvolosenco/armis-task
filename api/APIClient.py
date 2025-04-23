from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_log
from typing import List, Dict, Any
import logging
import requests

from utils import logger

class APIClient:    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"token": token}
    
    def __enter__(self):
        self.session = requests.Session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=30),
        retry=retry_if_exception_type((requests.exceptions.RequestException)),
        before=before_log(logger, logging.INFO),
        after=before_log(logger, logging.INFO)
    )
    
    def get_host_data(self, url_path: str, skip: int, limit: int) -> List[Dict[str, Any]]:
        return self._get_host_data(url_path, skip, limit)
    
    def _get_host_data(self, url_path: str, skip: int, limit: int) -> List[Dict[str, Any]]:
        full_url = f"{self.base_url}?skip={skip}&limit={limit}"
        
        try:
            response = requests.post(full_url, headers=self.headers, data={})
            logger.info(f"Request URL: {full_url}")
            # Handle specific error case for invalid skip/limit combo
            if response.status_code == 500 and "Error invalid skip/limit combo" in response.text:
                logger.warning(f"Invalid skip/limit combo, reducing limit. Skip: {skip}, Limit: {limit}")
                return self._get_host_data(url_path, skip, limit - 1)
            
            if response.status_code != 200:
                error_msg = f"Error: Received status code {response.status_code} for URL {full_url}"
                logger.error(error_msg)
                raise requests.exceptions.HTTPError(error_msg)
            
            result = response.json()
            if not isinstance(result, (dict, list)):
                error_msg = "Warning: Response is not a dictionary or list as expected"
                logger.error(error_msg)
                raise ValueError(error_msg)
                
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return
