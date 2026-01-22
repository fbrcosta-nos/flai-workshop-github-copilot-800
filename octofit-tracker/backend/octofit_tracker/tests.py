from django.test import TestCase
from django.utils import timezone
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model."""
    
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            username='testuser',
            full_name='Test User',
            team_id=1
        )
    
    def test_user_creation(self):
        """Test user creation."""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertEqual(self.user.team_id, 1)
    
    def test_user_string_representation(self):
        """Test user string representation."""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model."""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team for unit testing'
        )
    
    def test_team_creation(self):
        """Test team creation."""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team for unit testing')
    
    def test_team_string_representation(self):
        """Test team string representation."""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model."""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id=1,
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            notes='Morning run'
        )
    
    def test_activity_creation(self):
        """Test activity creation."""
        self.assertEqual(self.activity.user_id, 1)
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertEqual(self.activity.calories, 300)
    
    def test_activity_string_representation(self):
        """Test activity string representation."""
        self.assertEqual(str(self.activity), 'Running - 30 mins')


class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model."""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_id=1,
            team_id=1,
            total_activities=10,
            total_duration=500,
            total_calories=2500,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard creation."""
        self.assertEqual(self.leaderboard.user_id, 1)
        self.assertEqual(self.leaderboard.team_id, 1)
        self.assertEqual(self.leaderboard.total_activities, 10)
        self.assertEqual(self.leaderboard.total_duration, 500)
        self.assertEqual(self.leaderboard.total_calories, 2500)
        self.assertEqual(self.leaderboard.rank, 1)
    
    def test_leaderboard_string_representation(self):
        """Test leaderboard string representation."""
        self.assertEqual(str(self.leaderboard), 'Rank 1 - User 1')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model."""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning HIIT',
            description='High intensity interval training',
            activity_type='HIIT',
            difficulty='Medium',
            duration=20,
            calories_estimate=250
        )
    
    def test_workout_creation(self):
        """Test workout creation."""
        self.assertEqual(self.workout.name, 'Morning HIIT')
        self.assertEqual(self.workout.description, 'High intensity interval training')
        self.assertEqual(self.workout.activity_type, 'HIIT')
        self.assertEqual(self.workout.difficulty, 'Medium')
        self.assertEqual(self.workout.duration, 20)
        self.assertEqual(self.workout.calories_estimate, 250)
    
    def test_workout_string_representation(self):
        """Test workout string representation."""
        self.assertEqual(str(self.workout), 'Morning HIIT')
