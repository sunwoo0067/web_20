from httpx import AsyncClient
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class OwnerclanClient:
    def __init__(self):
        self.client = AsyncClient()
        self.api_url = settings.OWNERCLAN_API_URL
        self.access_token = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def login(self):
        query = """
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                accessToken
            }
        }
        """
        
        variables = {
            "username": settings.OWNERCLAN_USERNAME,
            "password": settings.OWNERCLAN_PASSWORD
        }
        
        try:
            logger.info("Attempting to login to Ownerclan API")
            logger.info(f"Username: {settings.OWNERCLAN_USERNAME}")
            logger.info(f"API URL: {self.api_url}")
            
            request_data = {
                "query": query,
                "variables": variables
            }
            
            logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
            
            response = await self.client.post(
                self.api_url,
                json=request_data,
                headers=self.headers
            )
            
            response_data = response.json()
            logger.info(f"Login response status: {response.status_code}")
            logger.info(f"Login response: {json.dumps(response_data, indent=2)}")
            
            if response.status_code != 200:
                raise Exception(f"Login failed with status code: {response.status_code}")
            
            if "errors" in response_data:
                raise Exception(f"Login failed: {response_data['errors']}")
            
            if "data" not in response_data or "login" not in response_data["data"]:
                raise Exception("Invalid login response structure")
            
            self.access_token = response_data["data"]["login"]["accessToken"]
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            logger.info("Successfully logged in and got access token")
            
            return self.access_token
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise
    
    async def get_products(self, skip: int = 0, limit: int = 20):
        try:
            if not self.access_token:
                await self.login()
            
            query = """
            query($offset: Int, $limit: Int) {
                products(offset: $offset, limit: $limit) {
                    items {
                        id
                        name
                        price
                        description
                        images {
                            url
                        }
                        options {
                            name
                            values
                        }
                    }
                    total
                }
            }
            """
            
            variables = {
                "offset": skip,
                "limit": limit
            }
            
            logger.info("Sending products request")
            logger.info(f"Using headers: {self.headers}")
            
            response = await self.client.post(
                self.api_url,
                json={
                    "query": query,
                    "variables": variables
                },
                headers=self.headers
            )
            
            response_data = response.json()
            logger.info(f"Products response: {response_data}")
            
            if "errors" in response_data:
                logger.error(f"Products request failed: {response_data['errors']}")
                raise Exception(f"Products request failed: {response_data['errors']}")
            
            if "data" not in response_data or "products" not in response_data["data"]:
                logger.error(f"Unexpected response structure: {response_data}")
                raise Exception("Invalid products response structure")
            
            return response_data["data"]["products"]
            
        except Exception as e:
            logger.error(f"Products request error: {str(e)}")
            raise