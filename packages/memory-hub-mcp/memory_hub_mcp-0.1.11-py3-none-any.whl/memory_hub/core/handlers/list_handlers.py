# handlers/list_handlers.py - ID listing endpoint handlers

# Removed FastAPI dependencies for stdio-only MCP server

# Simple exception class to replace FastAPI ValidationError
class ValidationError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

from ..config import QDRANT_COLLECTION_NAME, SCROLL_BATCH_SIZE
from ..models import ListIdsResponse
from ..services import AppConfig

async def list_app_ids(config: AppConfig):
    """
    Lists all unique app_ids found in the Memory Hub.
    """
    try:
        print("INFO: Listing all app_ids in Memory Hub")
        
        # Use scroll to get all points (Qdrant doesn't have DISTINCT queries)
        all_app_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:  # No more points
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                app_id = point.payload.get('app_id')
                if app_id:
                    all_app_ids.add(str(app_id))
            
            offset = scroll_result[1]  # Next offset for pagination
            if offset is None:  # No more pages
                break
        
        unique_app_ids = sorted(list(all_app_ids))
        print(f"INFO: Found {len(unique_app_ids)} unique app_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_app_ids,
            total_count=len(unique_app_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        print(f"ERROR: Failed to list app_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list app_ids: {str(e)}")

async def list_project_ids(config: AppConfig):
    """
    Lists all unique project_ids found in the Memory Hub.
    """
    try:
        print("INFO: Listing all project_ids in Memory Hub")
        
        all_project_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                project_id = point.payload.get('project_id')
                if project_id:  # Only include non-null project_ids
                    all_project_ids.add(str(project_id))
            
            offset = scroll_result[1]
            if offset is None:
                break
        
        unique_project_ids = sorted(list(all_project_ids))
        print(f"INFO: Found {len(unique_project_ids)} unique project_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_project_ids,
            total_count=len(unique_project_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        print(f"ERROR: Failed to list project_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list project_ids: {str(e)}")

async def list_ticket_ids(config: AppConfig):
    """
    Lists all unique ticket_ids found in the Memory Hub.
    """
    try:
        print("INFO: Listing all ticket_ids in Memory Hub")
        
        all_ticket_ids = set()
        points_scanned = 0
        offset = None
        
        while True:
            scroll_result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=SCROLL_BATCH_SIZE,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            if not scroll_result[0]:
                break
                
            for point in scroll_result[0]:
                points_scanned += 1
                ticket_id = point.payload.get('ticket_id')
                if ticket_id:  # Only include non-null ticket_ids
                    all_ticket_ids.add(str(ticket_id))
            
            offset = scroll_result[1]
            if offset is None:
                break
        
        unique_ticket_ids = sorted(list(all_ticket_ids))
        print(f"INFO: Found {len(unique_ticket_ids)} unique ticket_ids from {points_scanned} points")
        
        return ListIdsResponse(
            ids=unique_ticket_ids,
            total_count=len(unique_ticket_ids),
            points_scanned=points_scanned
        )
        
    except Exception as e:
        print(f"ERROR: Failed to list ticket_ids: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to list ticket_ids: {str(e)}") 