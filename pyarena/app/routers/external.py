"""
External API Routes
Integration with external APIs and services.
Mission 4: External Scrolls
Mission 5: Parallel Prophecies (async operations)
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import httpx
import asyncio
import aiohttp
from typing import List, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models import User, APILog
from app.schemas import ExternalAPIRequest, ExternalAPIResponse
from app.utils.auth_utils import get_current_user

router = APIRouter()


async def log_api_call(
    db: Session,
    user_id: int,
    endpoint: str,
    method: str,
    status_code: int,
    response_time: float
):
    """
    Background task to log API calls.
    Mission 7: Echo of Time (background tasks)
    """
    log_entry = APILog(
        user_id=user_id,
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        response_time=response_time
    )
    db.add(log_entry)
    db.commit()


@router.get("/fetch")
async def fetch_external_data(
    url: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch data from an external API using httpx.
    TODO: Add request validation and sanitization.
    """
    start_time = datetime.now()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Log the API call in the background
            background_tasks.add_task(
                log_api_call,
                db,
                current_user.id,
                url,
                "GET",
                response.status_code,
                response_time
            )

            return ExternalAPIResponse(
                status_code=response.status_code,
                data=response.json() if response.headers.get('content-type', '').startswith('application/json') else {'content': response.text},
                response_time=response_time
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="External API request timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error connecting to external API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.post("/fetch-multiple")
async def fetch_multiple_apis(
    urls: List[str],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch from multiple APIs in parallel using asyncio.
    Mission 5: Parallel Prophecies
    TODO: Add retry logic and circuit breaker pattern.
    """
    async def fetch_one(url: str, client: httpx.AsyncClient) -> Dict[str, Any]:
        """Helper function to fetch a single URL"""
        start_time = datetime.now()
        try:
            response = await client.get(url)
            response_time = (datetime.now() - start_time).total_seconds() * 1000

            # Log in background
            background_tasks.add_task(
                log_api_call,
                db,
                current_user.id,
                url,
                "GET",
                response.status_code,
                response_time
            )

            return {
                'url': url,
                'status_code': response.status_code,
                'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else {'content': response.text},
                'response_time': response_time,
                'success': True
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'success': False
            }

    # Fetch all URLs in parallel
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_one(url, client) for url in urls]
        results = await asyncio.gather(*tasks)

    successful = sum(1 for r in results if r.get('success'))
    total_time = sum(r.get('response_time', 0) for r in results if r.get('success'))

    return {
        'total_requests': len(urls),
        'successful': successful,
        'failed': len(urls) - successful,
        'total_time': round(total_time, 2),
        'results': results
    }


@router.get("/github/user/{username}")
async def get_github_user(
    username: str,
    current_user: User = Depends(get_current_user)
):
    """
    Example: Fetch GitHub user information.
    TODO: Cache responses to avoid rate limiting.
    """
    url = f"https://api.github.com/users/{username}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)

            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"GitHub user '{username}' not found"
                )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching GitHub data: {str(e)}"
        )


@router.get("/async-demo")
async def async_operations_demo():
    """
    Demonstrate async operations with multiple concurrent tasks.
    Mission 5: Parallel Prophecies
    """
    async def task_one():
        """Simulate async task 1"""
        await asyncio.sleep(1)
        return {"task": "one", "result": "completed", "duration": 1}

    async def task_two():
        """Simulate async task 2"""
        await asyncio.sleep(2)
        return {"task": "two", "result": "completed", "duration": 2}

    async def task_three():
        """Simulate async task 3"""
        await asyncio.sleep(1.5)
        return {"task": "three", "result": "completed", "duration": 1.5}

    start_time = datetime.now()

    # Run all tasks in parallel
    results = await asyncio.gather(
        task_one(),
        task_two(),
        task_three()
    )

    total_time = (datetime.now() - start_time).total_seconds()

    return {
        'message': 'All tasks completed in parallel',
        'sequential_time_would_be': 4.5,  # Sum of all durations
        'actual_parallel_time': round(total_time, 2),
        'time_saved': round(4.5 - total_time, 2),
        'results': results
    }


@router.get("/public-apis")
async def get_public_apis_list(category: str = None):
    """
    Fetch list of public APIs from the Public APIs project.
    Great for testing external API integration!
    """
    url = "https://api.publicapis.org/entries"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            if category:
                # Filter by category
                entries = [
                    entry for entry in data.get('entries', [])
                    if entry.get('Category', '').lower() == category.lower()
                ]
                return {'category': category, 'count': len(entries), 'apis': entries}

            return {
                'total': data.get('count', 0),
                'apis': data.get('entries', [])[:10]  # Return first 10
            }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching public APIs: {str(e)}"
        )
