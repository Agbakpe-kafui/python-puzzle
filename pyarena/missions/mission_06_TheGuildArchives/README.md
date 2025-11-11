# 📊 Mission 6: The Guild Archives

**Status**: Core
**Difficulty**: Intermediate
**Focus**: Data Analysis with pandas & numpy

---

## 🎯 Mission Objective

Unlock the secrets hidden in data! Learn to use pandas and numpy for data analysis, create analytics endpoints, and generate insights from your Guild's records.

---

## 📚 What You'll Learn

- pandas DataFrame operations
- numpy array calculations
- Data aggregation and grouping
- Statistical analysis
- Data visualization preparation
- Performance optimization with vectorization

---

## ✅ Tasks

### 1. Explore Analytics Endpoints

Check out `app/routers/analytics.py` which already uses pandas:

```bash
# Get user statistics
curl http://localhost:8000/api/analytics/users/stats

# Get mission statistics
curl http://localhost:8000/api/analytics/missions/stats

# Get leaderboard
curl http://localhost:8000/api/analytics/leaderboard
```

### 2. Create Advanced User Analytics

Implement comprehensive user analytics:

```python
import pandas as pd
import numpy as np

@router.get("/users/advanced-stats")
async def get_advanced_user_stats(db: Session = Depends(get_db)):
    """
    TODO: Calculate advanced user statistics
    - User growth over time
    - Experience distribution (percentiles)
    - Active vs inactive ratio
    - Guild rank distribution
    - Mission completion rate by user segment
    """

    users = db.query(User).all()
    df = pd.DataFrame([{
        'id': u.id,
        'username': u.username,
        'experience_points': u.experience_points,
        'missions_completed': u.missions_completed,
        'guild_rank': u.guild_rank,
        'is_active': u.is_active,
        'created_at': u.created_at
    } for u in users])

    # TODO: Calculate statistics
    stats = {
        'total_users': len(df),
        'experience_percentiles': {
            'p25': float(df['experience_points'].quantile(0.25)),
            'p50': float(df['experience_points'].quantile(0.50)),
            'p75': float(df['experience_points'].quantile(0.75)),
            'p90': float(df['experience_points'].quantile(0.90)),
        },
        'rank_distribution': df['guild_rank'].value_counts().to_dict(),
        'avg_missions_per_user': float(df['missions_completed'].mean()),
        # Add more metrics
    }

    return stats
```

### 3. Build Time Series Analysis

Analyze user activity over time:

```python
@router.get("/activity/timeline")
async def get_activity_timeline(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    TODO: Create activity timeline
    - Get user registrations per day
    - Mission completions per day
    - Active users per day
    - Use pandas time series functions
    - Return data suitable for charting
    """

    # Get data
    users = db.query(User).all()
    df = pd.DataFrame([{
        'created_at': u.created_at,
        'experience_points': u.experience_points
    } for u in users])

    # Convert to datetime
    df['date'] = pd.to_datetime(df['created_at']).dt.date

    # Group by date
    timeline = df.groupby('date').agg({
        'created_at': 'count',  # New users
        'experience_points': 'sum'  # Total XP gained
    }).reset_index()

    return {
        'timeline': timeline.to_dict('records')
    }
```

### 4. Implement Cohort Analysis

Analyze user behavior by cohort:

```python
@router.get("/cohorts/retention")
async def cohort_retention_analysis(db: Session = Depends(get_db)):
    """
    TODO: Cohort retention analysis
    - Group users by signup month
    - Track their activity over following months
    - Calculate retention rates
    - Return cohort matrix
    """

    users = db.query(User).all()
    missions = db.query(MissionProgress).all()

    # Create DataFrames
    users_df = pd.DataFrame([{
        'user_id': u.id,
        'signup_month': pd.to_datetime(u.created_at).to_period('M')
    } for u in users])

    missions_df = pd.DataFrame([{
        'user_id': m.user_id,
        'completed_month': pd.to_datetime(m.completed_at).to_period('M')
            if m.completed_at else None
    } for m in missions if m.status == 'completed'])

    # TODO: Calculate cohort retention
    # Hint: Use pivot tables and groupby

    return {"cohorts": "TODO"}
```

### 5. Create Performance Comparison

Compare user performance across different dimensions:

```python
@router.get("/compare/ranks")
async def compare_by_rank(db: Session = Depends(get_db)):
    """
    TODO: Compare performance across guild ranks
    - Average experience by rank
    - Average missions completed by rank
    - Completion rate by rank
    - Use pandas groupby and aggregation
    """

    users = db.query(User).all()
    df = pd.DataFrame([{
        'guild_rank': u.guild_rank,
        'experience_points': u.experience_points,
        'missions_completed': u.missions_completed
    } for u in users])

    # Group by rank
    rank_stats = df.groupby('guild_rank').agg({
        'experience_points': ['mean', 'median', 'std'],
        'missions_completed': ['mean', 'max']
    })

    return rank_stats.to_dict()
```

### 6. Build Recommendation Engine

Use data to recommend next missions:

```python
@router.get("/recommendations/{user_id}")
async def recommend_missions(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    TODO: Recommend missions based on data
    - Analyze similar users (similar rank/experience)
    - Find missions they've completed
    - Recommend missions not yet attempted
    - Sort by popularity and success rate
    """

    # Get user
    user = db.query(User).filter(User.id == user_id).first()

    # Get similar users
    similar_users = db.query(User).filter(
        User.guild_rank == user.guild_rank,
        User.id != user_id
    ).all()

    # Get their completed missions
    # Calculate recommendations

    return {"recommended_missions": []}
```

---

## 🧪 Testing Your Solution

```bash
# Get advanced statistics
curl http://localhost:8000/api/analytics/users/advanced-stats

# Get activity timeline
curl http://localhost:8000/api/analytics/activity/timeline?days=30

# Get cohort analysis
curl http://localhost:8000/api/analytics/cohorts/retention

# Compare ranks
curl http://localhost:8000/api/analytics/compare/ranks
```

---

## 📖 Key Concepts

### Creating DataFrames
```python
import pandas as pd

df = pd.DataFrame([
    {'name': 'Alice', 'score': 95},
    {'name': 'Bob', 'score': 87}
])
```

### Basic Operations
```python
# Statistics
df['score'].mean()
df['score'].median()
df['score'].std()

# Filtering
high_scorers = df[df['score'] > 90]

# Sorting
df.sort_values('score', ascending=False)

# Grouping
df.groupby('category').agg({'score': ['mean', 'max']})
```

### numpy Operations
```python
import numpy as np

# Array operations
arr = np.array([1, 2, 3, 4, 5])
arr.mean()  # Average
arr.std()   # Standard deviation
np.percentile(arr, 95)  # 95th percentile
```

### Time Series
```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date_column'])

# Extract components
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.day_name()

# Resample
df.set_index('date').resample('D').sum()
```

---

## 🎓 Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [numpy Documentation](https://numpy.org/doc/)
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

---

## 📈 Analytics Best Practices

1. **Cache expensive queries** - Use Redis for computed metrics
2. **Paginate large datasets** - Don't load everything at once
3. **Use vectorized operations** - Avoid Python loops with pandas/numpy
4. **Index DataFrames** - Set appropriate indexes for fast lookups
5. **Handle missing data** - Use `fillna()`, `dropna()` appropriately
6. **Validate data types** - Ensure numeric columns are actually numeric

---

## ✨ Completion Criteria

- [ ] Retrieved and analyzed user statistics
- [ ] Created time series analysis
- [ ] Implemented cohort retention analysis
- [ ] Built performance comparison by rank
- [ ] Created recommendation engine
- [ ] Used pandas groupby and aggregation
- [ ] Calculated percentiles and distributions
- [ ] Exported data suitable for visualization

---

## 🐛 Common Issues

**Issue**: `KeyError` when accessing columns
**Solution**: Check column names with `df.columns`. Column names are case-sensitive.

**Issue**: `TypeError: cannot convert the series to <class 'float'>`
**Solution**: Use `.item()` or `float()` to convert single-value Series to Python types.

**Issue**: Slow performance on large datasets
**Solution**: Use vectorized operations, avoid iterating with `.iterrows()`.

---

## ⏭️ Next Mission

Data analysis complete! Move to **Mission 7: Echo of Time** to implement Redis caching and optimize performance.

*"In data, we find patterns. In patterns, we find truth..."*
