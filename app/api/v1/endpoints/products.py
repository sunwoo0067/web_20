from fastapi import APIRouter, HTTPException
from app.services.ownerclan import OwnerclanClient
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def get_products(
    skip: int = 0,
    limit: int = 20
) -> Dict[str, Any]:
    try:
        client = OwnerclanClient()
        
        logger.info("Attempting to login before fetching products")
        await client.login()
        
        logger.info(f"Fetching products with skip={skip}, limit={limit}")
        products_data = await client.get_products(skip=skip, limit=limit)
        
        return {
            "status": "success",
            "data": products_data,
            "meta": {
                "skip": skip,
                "limit": limit
            }
        }
        
    except Exception as e:
        logger.error(f"Error in get_products endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 