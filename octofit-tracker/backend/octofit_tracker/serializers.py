from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    team_name = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'team_id', 'team_name', 'date_joined', 'created_at']
        read_only_fields = ['created_at', 'date_joined']
    
    def get_team_name(self, obj):
        """Get the team name from the team_id"""
        if obj.team_id:
            try:
                team = Team.objects.get(id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'notes']
        read_only_fields = ['date']


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team_id', 'team_name', 'total_activities', 'total_duration', 'total_calories', 'total_points', 'rank', 'updated_at']
        read_only_fields = ['updated_at']
    
    def get_user_name(self, obj):
        """Get the user's full name from the user_id"""
        if obj.user_id:
            try:
                user = User.objects.get(id=obj.user_id)
                return user.full_name
            except User.DoesNotExist:
                return "Unknown User"
        return "Unknown User"
    
    def get_team_name(self, obj):
        """Get the team name from the team_id"""
        if obj.team_id:
            try:
                team = Team.objects.get(id=obj.team_id)
                return team.name
            except Team.DoesNotExist:
                return None
        return None
    
    def get_total_points(self, obj):
        """Calculate total points based on activities and duration"""
        # Points calculation: activities * 10 + duration * 2
        return (obj.total_activities * 10) + (obj.total_duration * 2)


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'activity_type', 'difficulty', 'duration', 'calories_estimate']
