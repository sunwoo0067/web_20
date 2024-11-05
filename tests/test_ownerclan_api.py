import asyncio
import httpx
import logging
from typing import Optional

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_login() -> Optional[str]:
    base_url = "https://api-sandbox.ownerclan.com/v1/graphql"
    
    login_query = '''
    mutation Login($username: String!, $password: String!) {
        login(username: $username, password: $password) {
            accessToken
        }
    }
    '''
    
    variables = {
        "username": "b00679540",
        "password": "ehdgod1101*"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.post(
                base_url,
                json={
                    "query": login_query,
                    "variables": variables
                },
                headers=headers
            )
            logger.info(f"Login Status Code: {response.status_code}")
            logger.info(f"Login Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "login" in data["data"]:
                    return data["data"]["login"]["accessToken"]
            return None
            
        except Exception as e:
            logger.error(f"Login Error: {str(e)}")
            return None

async def test_get_products(access_token: Optional[str] = None):
    base_url = "http://127.0.0.1:8000"
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(
                f"{base_url}/api/v1/products",
                headers=headers
            )
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Headers: {response.headers}")
            
            if response.status_code == 200:
                logger.info(f"Response: {response.json()}")
            else:
                logger.error(f"Response Text: {response.text}")
                
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")

async def run_tests():
    logger.info("Testing login...")
    access_token = await test_login()
    
    if access_token:
        logger.info("\nTesting products with access token...")
        await test_get_products(access_token)
    else:
        logger.warning("\nSkipping products test due to login failure")

if __name__ == "__main__":
    asyncio.run(run_tests())