from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for User model.
    """
    list_display = ['id', 'username', 'email', 'full_name', 'team_id', 'created_at']
    list_filter = ['team_id', 'created_at']
    search_fields = ['username', 'email', 'full_name']
    ordering = ['-created_at']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin interface for Team model.
    """
    list_display = ['id', 'name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """
    Admin interface for Activity model.
    """
    list_display = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date']
    list_filter = ['activity_type', 'date']
    search_fields = ['activity_type', 'notes']
    ordering = ['-date']


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """
    Admin interface for Leaderboard model.
    """
    list_display = ['id', 'user_id', 'team_id', 'rank', 'total_activities', 'total_duration', 'total_calories', 'updated_at']
    list_filter = ['team_id', 'rank', 'updated_at']
    search_fields = ['user_id', 'team_id']
    ordering = ['rank']


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """
    Admin interface for Workout model.
    """
    list_display = ['id', 'name', 'activity_type', 'difficulty', 'duration', 'calories_estimate']
    list_filter = ['activity_type', 'difficulty']
    search_fields = ['name', 'description', 'activity_type']
    ordering = ['name']
