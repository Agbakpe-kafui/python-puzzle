"""
Analytics Routes
Data analysis and statistics endpoints.
Mission 6: The Guild Archives
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
from typing import List, Dict, Any

from app.database import get_db
from app.models import User, MissionProgress, APILog
from app.schemas import UserStats, MissionStats
from app.utils.auth_utils import get_current_user

router = APIRouter()


@router.get("/users/stats", response_model=UserStats)
async def get_user_statistics(db: Session = Depends(get_db)):
    """
    Get overall user statistics using pandas for data analysis.
    TODO: Add caching for expensive queries.
    """
    # Query all users
    users = db.query(User).all()

    if not users:
        return UserStats(
            total_users=0,
            active_users=0,
            total_missions_completed=0,
            average_experience=0.0
        )

    # Convert to pandas DataFrame for analysis
    user_data = pd.DataFrame([
        {
            'id': u.id,
            'is_active': u.is_active,
            'missions_completed': u.missions_completed,
            'experience_points': u.experience_points
        }
        for u in users
    ])

    return UserStats(
        total_users=len(user_data),
        active_users=int(user_data['is_active'].sum()),
        total_missions_completed=int(user_data['missions_completed'].sum()),
        average_experience=float(user_data['experience_points'].mean())
    )


@router.get("/missions/stats")
async def get_mission_statistics(db: Session = Depends(get_db)):
    """
    Get mission completion statistics.
    TODO: Add filtering by date range and mission ID.
    """
    # Query mission progress
    missions = db.query(
        MissionProgress.mission_id,
        MissionProgress.mission_name,
        func.count(MissionProgress.id).label('total_attempts'),
        func.count(MissionProgress.id).filter(
            MissionProgress.status == 'completed'
        ).label('completed'),
        func.avg(MissionProgress.score).label('average_score')
    ).group_by(
        MissionProgress.mission_id,
        MissionProgress.mission_name
    ).all()

    results = []
    for mission in missions:
        completion_rate = (mission.completed / mission.total_attempts * 100
                          if mission.total_attempts > 0 else 0)
        results.append({
            'mission_id': mission.mission_id,
            'mission_name': mission.mission_name,
            'total_attempts': mission.total_attempts,
            'completion_rate': round(completion_rate, 2),
            'average_score': round(mission.average_score or 0, 2)
        })

    return {'missions': results}


@router.get("/users/{user_id}/performance")
async def get_user_performance(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed performance metrics for a specific user.
    TODO: Add comparison with average user performance.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Get user's mission progress
    missions = db.query(MissionProgress).filter(
        MissionProgress.user_id == user_id
    ).all()

    # Convert to DataFrame for analysis
    if missions:
        mission_data = pd.DataFrame([
            {
                'mission_id': m.mission_id,
                'mission_name': m.mission_name,
                'status': m.status,
                'score': m.score,
                'started_at': m.started_at,
                'completed_at': m.completed_at
            }
            for m in missions
        ])

        completed_missions = mission_data[mission_data['status'] == 'completed']

        return {
            'user_id': user_id,
            'username': user.username,
            'guild_rank': user.guild_rank,
            'total_experience': user.experience_points,
            'missions_attempted': len(mission_data),
            'missions_completed': len(completed_missions),
            'completion_rate': round(len(completed_missions) / len(mission_data) * 100, 2)
                              if len(mission_data) > 0 else 0,
            'average_score': round(completed_missions['score'].mean(), 2)
                           if len(completed_missions) > 0 else 0,
            'missions': mission_data.to_dict('records')
        }

    return {
        'user_id': user_id,
        'username': user.username,
        'guild_rank': user.guild_rank,
        'total_experience': user.experience_points,
        'missions_attempted': 0,
        'missions_completed': 0,
        'completion_rate': 0,
        'average_score': 0,
        'missions': []
    }


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get top users ranked by experience points.
    TODO: Add different ranking categories (missions completed, average score, etc.)
    """
    users = db.query(User).order_by(
        User.experience_points.desc()
    ).limit(limit).all()

    leaderboard = [
        {
            'rank': idx + 1,
            'username': user.username,
            'guild_rank': user.guild_rank,
            'experience_points': user.experience_points,
            'missions_completed': user.missions_completed
        }
        for idx, user in enumerate(users)
    ]

    return {'leaderboard': leaderboard}


@router.get("/api-usage")
async def get_api_usage_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Analyze external API usage patterns.
    Mission 4: External Scrolls
    TODO: Add time-based filtering and aggregation.
    """
    logs = db.query(APILog).all()

    if not logs:
        return {
            'total_requests': 0,
            'average_response_time': 0,
            'success_rate': 0,
            'endpoints': []
        }

    # Convert to DataFrame
    log_data = pd.DataFrame([
        {
            'endpoint': log.endpoint,
            'method': log.method,
            'status_code': log.status_code,
            'response_time': log.response_time
        }
        for log in logs
    ])

    # Calculate statistics
    total_requests = len(log_data)
    avg_response_time = log_data['response_time'].mean()
    success_count = len(log_data[log_data['status_code'] < 400])
    success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0

    # Group by endpoint
    endpoint_stats = log_data.groupby('endpoint').agg({
        'status_code': 'count',
        'response_time': 'mean'
    }).reset_index()

    endpoint_stats.columns = ['endpoint', 'request_count', 'avg_response_time']

    return {
        'total_requests': total_requests,
        'average_response_time': round(avg_response_time, 2),
        'success_rate': round(success_rate, 2),
        'endpoints': endpoint_stats.to_dict('records')
    }
