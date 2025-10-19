#!/usr/bin/env python
"""
Add 5 new roles to the interview app database
Usage: python add_roles.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vode.settings')
django.setup()

from interview.models import Role

print("\n" + "=" * 60)
print("Adding 5 New Roles to Interview App")
print("=" * 60 + "\n")

roles_data = [
    {
        "title": "Systems Engineer",
        "description": "Design and build scalable systems",
        "num_rounds": 3
    },
    {
        "title": "Security Engineer",
        "description": "Build secure and robust systems",
        "num_rounds": 4
    },
    {
        "title": "Database Administrator",
        "description": "Manage and optimize database systems",
        "num_rounds": 3
    },
    {
        "title": "Cloud Architect",
        "description": "Design cloud infrastructure and solutions",
        "num_rounds": 4
    },
    {
        "title": "Technical Lead",
        "description": "Lead technical teams and projects",
        "num_rounds": 3
    }
]

created_count = 0
for i, role_data in enumerate(roles_data, 1):
    role = Role.objects.create(
        title=role_data["title"],
        description=role_data["description"],
        num_rounds=role_data["num_rounds"]
    )
    print(f"{i}. ✅ {role.title}")
    print(f"   Description: {role.description}")
    print(f"   Rounds: {role.num_rounds}")
    print()
    created_count += 1

print("=" * 60)
print(f"✅ Successfully created {created_count} new roles!")
print(f"📊 Total roles in database: {Role.objects.count()}")
print("=" * 60 + "\n")
