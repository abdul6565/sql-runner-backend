from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from models.user import QueryRequest
from database import execute_query, save_query_history, get_recent_queries, get_user_profile
from routes.auth import get_current_user

router = APIRouter()


@router.post("/query", response_model=List[Dict[str, Any]])
async def execute_sql_query(
    query_request: QueryRequest,
    current_user: str = Depends(get_current_user)
):
    """Execute SQL query and return results."""
    try:
        # Validate query (basic check)
        query = query_request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Prevent dangerous operations (basic security)
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE']
        query_upper = query.upper()
        if any(keyword in query_upper for keyword in dangerous_keywords):
            raise HTTPException(
                status_code=403,
                detail="Query contains potentially dangerous operations"
            )

        # Execute query
        results = execute_query(query)

        # Save to history
        save_query_history(current_user, query, results)

        return results

    except Exception as e:
        error_msg = str(e)
        if "Database error:" in error_msg:
            error_msg = error_msg.replace("Database error:", "").strip()

        raise HTTPException(status_code=400, detail=f"Query execution failed: {error_msg}")


@router.get("/recent_queries")
async def get_recent_user_queries(current_user: str = Depends(get_current_user)):
    """Get recent queries for the authenticated user."""
    try:
        queries = get_recent_queries(current_user)
        return queries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recent queries: {str(e)}")


@router.get("/profile")
async def get_user_profile_endpoint(current_user: str = Depends(get_current_user)):
    """Get user profile information."""
    try:
        profile = get_user_profile(current_user)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {str(e)}")
