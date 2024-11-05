import asyncio
import httpx
import json
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_api.log')
    ]
)
logger = logging.getLogger(__name__)

class OwnerClanAPI:
    def __init__(self):
        # 샌드박스가 아닌 프로덕션 URL 사용
        self.base_url = "https://api.ownerclan.com/v1"
        self.auth_url = "https://auth.ownerclan.com/auth"
        self.token = None
    
    async def authenticate(self):
        auth_data = {
            "service": "ownerclan",
            "userType": "seller",
            "username": "b00679540",
            "password": "ehdgod1101*"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.auth_url,
                    json=auth_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    self.token = response.text  # JWT 토큰 저장
                    return True
                return False
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    async def get_products(self, offset=0, limit=10):
        """상품 목록 조회"""
        if not self.token:
            if not await self.authenticate():
                raise Exception("인증 실패")

        query = """
        query Products($offset: Int, $limit: Int) {
            products(offset: $offset, limit: $limit) {
                items {
                    id
                    name
                    price
                    status
                    options {
                        id
                        name
                        values
                    }
                    images {
                        url
                        sortOrder
                    }
                }
                total
            }
        }
        """

        variables = {
            "offset": offset,
            "limit": limit
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/graphql",
                    json={
                        "query": query,
                        "variables": variables
                    },
                    headers=headers
                )

                data = response.json()
                if "errors" in data:
                    logger.error(f"GraphQL 에러: {data['errors']}")
                    return None
                
                products = data.get("data", {}).get("products", {})
                logger.info(f"총 {products.get('total', 0)}개의 상품 중 {len(products.get('items', []))}개 조회됨")
                return products

        except Exception as e:
            logger.error(f"상품 조회 실패: {e}")
            return None

async def main():
    api = OwnerClanAPI()
    
    # 상품 조회 테스트
    logger.info("=== 상품 조회 테스트 시작 ===")
    products = await api.get_products(limit=5)  # 5개만 조회
    
    if products:
        logger.info("\n=== 상품 목록 ===")
        for product in products.get("items", []):
            logger.info(f"""
상품ID: {product['id']}
상품명: {product['name']}
가격: {product['price']}
상태: {product['status']}
옵션수: {len(product.get('options', []))}
이미지수: {len(product.get('images', []))}
            """)
    
    logger.info("=== 테스트 완료 ===")

if __name__ == "__main__":
    asyncio.run(main()) 