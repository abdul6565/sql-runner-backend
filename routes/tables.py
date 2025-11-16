from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from database import get_table_names, get_table_info
from routes.auth import get_current_user

router = APIRouter()


@router.get("/tables", response_model=List[str])
async def get_available_tables(current_user: str = Depends(get_current_user)):
    """Get list of available tables in the database."""
    try:
        tables = get_table_names()
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tables: {str(e)}")


@router.get("/table_info/{table_name}")
async def get_table_information(table_name: str, current_user: str = Depends(get_current_user)):
    """Get schema and sample data for a specific table."""
    try:
        # Validate table name exists
        tables = get_table_names()
        if table_name not in tables:
            raise HTTPException(status_code=404, detail=f"Table '{table_name}' not found")

        table_info = get_table_info(table_name)
        return table_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch table info: {str(e)}")
