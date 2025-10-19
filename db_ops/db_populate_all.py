#!/usr/bin/env python
"""
Populate VODE database with test data
Creates: 1 Recruiter, 2 SWEs, 3 Candidates, 3 Roles, Rounds, and Interviews
Usage: python db_populate_all.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vode.settings')
django.setup()

from django.contrib.auth.models import User
from recruit.models import Recruiter
from swe.models import SWE
from cand.models import Candidate
from interview.models import Role, Round, Interview

print("\n" + "=" * 60)
print("� Populating VODE Database")
print("=" * 60 + "\n")

# Clear existing data (optional - comment out if you want to keep existing data)
print("🗑️  Clearing existing data...")
Interview.objects.all().delete()
Round.objects.all().delete()
Role.objects.all().delete()
Candidate.objects.all().delete()
SWE.objects.all().delete()
Recruiter.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
print("  ✅ Cleared\n")
# exit()

# Create 1 Recruiter
print("👤 Creating Recruiter...")
recruiter_user = User.objects.create_user(
    username='recruiter1',
    email='recruiter@vode.com',
    password='password123',
    first_name='Rachel',
    last_name='Hamilton'
)
recruiter = Recruiter.objects.create(user=recruiter_user)
print(f"  ✅ {recruiter}\n")

# Create 2 SWEs
print("👨‍💻 Creating SWEs...")
swe1_user = User.objects.create_user(
    username='swe1',
    email='swe1@vode.com',
    password='password123',
    first_name='Sarah',
    last_name='Jenkins'
)
swe1 = SWE.objects.create(user=swe1_user)
print(f"  ✅ {swe1}")

swe2_user = User.objects.create_user(
    username='swe2',
    email='swe2@vode.com',
    password='password123',
    first_name='Sapp',
    last_name='Aluri'
)
swe2 = SWE.objects.create(user=swe2_user)
print(f"  ✅ {swe2}\n")

# Create 3 Candidates
print("🎯 Creating Candidates...")
candidate1_user = User.objects.create_user(
    username='candidate1',
    email='candidate1@example.com',
    password='password123',
    first_name='Alice',
    last_name='Anderson'
)
candidate1 = Candidate.objects.create(user=candidate1_user)
print(f"  ✅ {candidate1}")

candidate2_user = User.objects.create_user(
    username='candidate2',
    email='candidate2@example.com',
    password='password123',
    first_name='Bob',
    last_name='Brown'
)
candidate2 = Candidate.objects.create(user=candidate2_user)
print(f"  ✅ {candidate2}")

candidate3_user = User.objects.create_user(
    username='candidate3',
    email='candidate3@example.com',
    password='password123',
    first_name='Charlie',
    last_name='Chen'
)
candidate3 = Candidate.objects.create(user=candidate3_user)
print(f"  ✅ {candidate3}\n")

# Recruiter creates 3 Roles
print("📋 Creating Roles...")
role1 = Role.objects.create(
    title="Backend Engineer",
    description="Build scalable server-side systems",
    num_rounds=1,
    owning_recruiter=recruiter
)
print(f"  ✅ {role1.title} ({role1.num_rounds} round)")

role2 = Role.objects.create(
    title="Frontend Engineer",
    description="Create beautiful user interfaces",
    num_rounds=2,
    owning_recruiter=recruiter
)
print(f"  ✅ {role2.title} ({role2.num_rounds} rounds)")

role3 = Role.objects.create(
    title="Full Stack Engineer",
    description="End-to-end development",
    num_rounds=3,
    owning_recruiter=recruiter
)
print(f"  ✅ {role3.title} ({role3.num_rounds} rounds)\n")

# Assign roles to SWEs: 1 to swe1, 2 to swe2
print("🔗 Assigning Roles to SWEs...")
role1.assigned_swe = swe1
role1.save()
print(f"  ✅ {role1.title} → {swe1}")

role2.assigned_swe = swe2
role2.save()
print(f"  ✅ {role2.title} → {swe2}")

role3.assigned_swe = swe2
role3.save()
print(f"  ✅ {role3.title} → {swe2}\n")

# Create Rounds for each Role
print("� Creating Rounds...")
round_templates = [
    ("Technical Screening", "Initial coding assessment", "easy", "Arrays, Strings", "Clean code, Problem solving", 60),
    ("Algorithms Round", "Data structures and algorithms", "medium", "Trees, Graphs, Dynamic Programming", "Optimal solutions, Time complexity", 90),
    ("System Design", "Architecture and scalability", "hard", "System Design, Distributed Systems", "Scalability, Trade-offs", 120),
]

all_rounds = []
for role in [role1, role2, role3]:
    for round_num in range(1, role.num_rounds + 1):
        template = round_templates[round_num - 1] if round_num <= len(round_templates) else round_templates[-1]
        round_obj = Round.objects.create(
            role=role,
            round_number=round_num,
            name=template[0],
            description=template[1],
            difficulty_level=template[2],
            data_structures=template[3],
            success_metrics=template[4],
            time_limit=template[5]
        )
        all_rounds.append(round_obj)
        print(f"  ✅ {role.title} - Round {round_num}: {round_obj.name}")

print()

# Create Interviews
print("📅 Creating Interviews...")

# Candidate 1: Has interview in round 1 of all three roles
print(f"  {candidate1}:")
interview1_1 = Interview.objects.create(
    candidate=candidate1,
    round=Round.objects.get(role=role1, round_number=1)
)
print(f"    ✅ Interview for {role1.title} - Round 1")

interview1_2 = Interview.objects.create(
    candidate=candidate1,
    round=Round.objects.get(role=role2, round_number=1)
)
print(f"    ✅ Interview for {role2.title} - Round 1")

interview1_3 = Interview.objects.create(
    candidate=candidate1,
    round=Round.objects.get(role=role3, round_number=1)
)
print(f"    ✅ Interview for {role3.title} - Round 1")

# Candidate 2: Has interview in round 1 of two roles (role1 and role2)
print(f"\n  {candidate2}:")
interview2_1 = Interview.objects.create(
    candidate=candidate2,
    round=Round.objects.get(role=role1, round_number=1)
)
print(f"    ✅ Interview for {role1.title} - Round 1")

interview2_2 = Interview.objects.create(
    candidate=candidate2,
    round=Round.objects.get(role=role2, round_number=1)
)
print(f"    ✅ Interview for {role2.title} - Round 1")

# Candidate 3: Has interview in round 1 of one role (role1)
print(f"\n  {candidate3}:")
interview3_1 = Interview.objects.create(
    candidate=candidate3,
    round=Round.objects.get(role=role1, round_number=1)
)
print(f"    ✅ Interview for {role1.title} - Round 1")

print("\n" + "=" * 60)
print("📊 Database Summary:")
print("=" * 60)
print(f"  • Recruiters: {Recruiter.objects.count()}")
print(f"  • SWEs: {SWE.objects.count()}")
print(f"  • Candidates: {Candidate.objects.count()}")
print(f"  • Roles: {Role.objects.count()}")
print(f"  • Rounds: {Round.objects.count()}")
print(f"  • Interviews: {Interview.objects.count()}")
print("=" * 60 + "\n")

print("✅ Database populated successfully!\n")
