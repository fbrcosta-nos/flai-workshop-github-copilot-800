from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing existing data...')
        
        # Delete existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            id=1,
            name='Team Marvel',
            description='Avengers assemble! The mightiest heroes on Earth united in fitness.'
        )
        
        team_dc = Team.objects.create(
            id=2,
            name='Team DC',
            description='Justice League unite! Champions of truth, justice, and fitness.'
        )
        
        self.stdout.write(self.style.SUCCESS(f'Created teams: {team_marvel.name}, {team_dc.name}'))
        
        # Create Marvel Users
        self.stdout.write('Creating users...')
        marvel_users = [
            {'email': 'ironman@marvel.com', 'username': 'ironman', 'full_name': 'Tony Stark', 'team_id': 1},
            {'email': 'captainamerica@marvel.com', 'username': 'captainamerica', 'full_name': 'Steve Rogers', 'team_id': 1},
            {'email': 'thor@marvel.com', 'username': 'thor', 'full_name': 'Thor Odinson', 'team_id': 1},
            {'email': 'blackwidow@marvel.com', 'username': 'blackwidow', 'full_name': 'Natasha Romanoff', 'team_id': 1},
            {'email': 'hulk@marvel.com', 'username': 'hulk', 'full_name': 'Bruce Banner', 'team_id': 1},
            {'email': 'spiderman@marvel.com', 'username': 'spiderman', 'full_name': 'Peter Parker', 'team_id': 1},
            {'email': 'blackpanther@marvel.com', 'username': 'blackpanther', 'full_name': 'T\'Challa', 'team_id': 1},
            {'email': 'scarletwitch@marvel.com', 'username': 'scarletwitch', 'full_name': 'Wanda Maximoff', 'team_id': 1},
        ]
        
        # Create DC Users
        dc_users = [
            {'email': 'batman@dc.com', 'username': 'batman', 'full_name': 'Bruce Wayne', 'team_id': 2},
            {'email': 'superman@dc.com', 'username': 'superman', 'full_name': 'Clark Kent', 'team_id': 2},
            {'email': 'wonderwoman@dc.com', 'username': 'wonderwoman', 'full_name': 'Diana Prince', 'team_id': 2},
            {'email': 'flash@dc.com', 'username': 'flash', 'full_name': 'Barry Allen', 'team_id': 2},
            {'email': 'aquaman@dc.com', 'username': 'aquaman', 'full_name': 'Arthur Curry', 'team_id': 2},
            {'email': 'cyborg@dc.com', 'username': 'cyborg', 'full_name': 'Victor Stone', 'team_id': 2},
            {'email': 'greenlantern@dc.com', 'username': 'greenlantern', 'full_name': 'Hal Jordan', 'team_id': 2},
            {'email': 'martianmanhunter@dc.com', 'username': 'martianmanhunter', 'full_name': 'J\'onn J\'onzz', 'team_id': 2},
        ]
        
        all_users_data = marvel_users + dc_users
        created_users = []
        
        for idx, user_data in enumerate(all_users_data, start=1):
            user = User.objects.create(
                id=idx,
                **user_data
            )
            created_users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_users)} users'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'Martial Arts', 'HIIT']
        
        activities_created = 0
        for user in created_users:
            num_activities = random.randint(5, 15)
            for _ in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(2, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 12)
                days_ago = random.randint(0, 30)
                
                Activity.objects.create(
                    user_id=user.id,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=timezone.now() - timedelta(days=days_ago),
                    notes=f'{activity_type} session by {user.username}'
                )
                activities_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_data = []
        
        for user in created_users:
            user_activities = Activity.objects.filter(user_id=user.id)
            total_activities = user_activities.count()
            total_duration = sum(a.duration for a in user_activities)
            total_calories = sum(a.calories for a in user_activities)
            
            leaderboard_data.append({
                'user_id': user.id,
                'team_id': user.team_id,
                'total_activities': total_activities,
                'total_duration': total_duration,
                'total_calories': total_calories,
            })
        
        # Sort by total_calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, entry in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_id=entry['user_id'],
                team_id=entry['team_id'],
                total_activities=entry['total_activities'],
                total_duration=entry['total_duration'],
                total_calories=entry['total_calories'],
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_data)} leaderboard entries'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        workouts = [
            {
                'name': 'Super Soldier Training',
                'description': 'Captain America\'s legendary workout routine for peak human performance',
                'activity_type': 'HIIT',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 600
            },
            {
                'name': 'Asgardian Power Lift',
                'description': 'Thor\'s mighty weightlifting session to build godlike strength',
                'activity_type': 'Weightlifting',
                'difficulty': 'Advanced',
                'duration': 75,
                'calories_estimate': 450
            },
            {
                'name': 'Web-Slinger Cardio',
                'description': 'Spider-Man\'s agility and cardio workout for enhanced reflexes',
                'activity_type': 'Running',
                'difficulty': 'Intermediate',
                'duration': 45,
                'calories_estimate': 400
            },
            {
                'name': 'Widow\'s Assassin Training',
                'description': 'Black Widow\'s martial arts and flexibility routine',
                'activity_type': 'Martial Arts',
                'difficulty': 'Advanced',
                'duration': 50,
                'calories_estimate': 500
            },
            {
                'name': 'Hulk Smash Strength',
                'description': 'Intense power training inspired by the Incredible Hulk',
                'activity_type': 'Weightlifting',
                'difficulty': 'Advanced',
                'duration': 90,
                'calories_estimate': 550
            },
            {
                'name': 'Dark Knight Discipline',
                'description': 'Batman\'s comprehensive training combining martial arts and strength',
                'activity_type': 'Mixed',
                'difficulty': 'Expert',
                'duration': 120,
                'calories_estimate': 800
            },
            {
                'name': 'Kryptonian Cardio',
                'description': 'Superman\'s high-intensity endurance workout',
                'activity_type': 'Running',
                'difficulty': 'Advanced',
                'duration': 60,
                'calories_estimate': 650
            },
            {
                'name': 'Amazonian Warrior Training',
                'description': 'Wonder Woman\'s balanced combat and strength routine',
                'activity_type': 'Mixed',
                'difficulty': 'Advanced',
                'duration': 70,
                'calories_estimate': 600
            },
            {
                'name': 'Speed Force Sprint',
                'description': 'The Flash\'s ultimate speed and agility workout',
                'activity_type': 'Running',
                'difficulty': 'Intermediate',
                'duration': 30,
                'calories_estimate': 450
            },
            {
                'name': 'Atlantean Swim Session',
                'description': 'Aquaman\'s underwater-inspired swimming workout',
                'activity_type': 'Swimming',
                'difficulty': 'Intermediate',
                'duration': 45,
                'calories_estimate': 400
            },
            {
                'name': 'Panther\'s Prowess',
                'description': 'Black Panther\'s agility and combat training',
                'activity_type': 'Martial Arts',
                'difficulty': 'Advanced',
                'duration': 55,
                'calories_estimate': 500
            },
            {
                'name': 'Mystic Arts Meditation',
                'description': 'Scarlet Witch\'s yoga and flexibility routine',
                'activity_type': 'Yoga',
                'difficulty': 'Beginner',
                'duration': 40,
                'calories_estimate': 200
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workouts'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams: {Team.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {Activity.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {Leaderboard.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {Workout.objects.count()}'))
