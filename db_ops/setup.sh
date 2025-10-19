#!/bin/bash

# Add new roles to VODE database
# Usage: ./setup.sh

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
fi

# Add new roles to database
./env/bin/python manage.py shell << 'EOF'
from interview.models import Role, Round

print("\n📋 Adding New Roles...")

new_roles = [
    ("Senior Backend Engineer", "Build scalable server-side systems with Python/Go", 3),
    ("Frontend Engineer", "Create beautiful UX with React/TypeScript", 3),
    ("Full Stack Engineer", "End-to-end development with modern tech stack", 4),
    ("DevOps Engineer", "Infrastructure, deployment, and cloud systems", 3),
    ("Machine Learning Engineer", "Build and deploy ML models with Python/TensorFlow", 3),
    ("Data Engineer", "Design and maintain data pipelines and infrastructure", 3),
    ("QA Engineer", "Ensure product quality through automated and manual testing", 3),
    ("Product Manager", "Lead product strategy and roadmap", 4),
    ("Solutions Architect", "Design solutions for enterprise clients", 3),
]

for title, desc, num_rounds in new_roles:
    role, created = Role.objects.get_or_create(
        title=title,
        defaults={"description": desc, "num_rounds": num_rounds}
    )
    if created:
        print(f"  ✅ Created: {title}")
    else:
        print(f"  ℹ️  Exists: {title}")

# Create rounds for each role
print("\n📋 Adding Rounds...")
round_templates = [
    ("Coding Challenge", "Initial technical challenge", "easy", "Problem Solving, Communication", 60),
    ("Coding Challenge", "Core competencies assessment", "medium", "Algorithms, Problem Solving", 90),
    ("Coding Challenge", "Advanced technical assessment", "hard", "System Design, Architecture", 120),
    ("Coding Challenge", "Leadership round", "hard", "Communication, Team Fit", 90),
]

round_count = 0
for role in Role.objects.all():
    for i in range(1, role.num_rounds + 1):
        t = round_templates[i-1] if i <= len(round_templates) else round_templates[-1]
        r, created = Round.objects.get_or_create(
            role=role,
            round_number=i,
            defaults={
                "name": t[0],
                "description": t[1],
                "difficulty_level": t[2],
                "data_structures": t[3],
                "time_limit": t[4]
            }
        )
        if created:
            round_count += 1

print(f"  ✅ Created {round_count} rounds\n")

print(f"� Database Summary:")
print(f"  • Total Roles: {Role.objects.count()}")
print(f"  • Total Rounds: {Round.objects.count()}\n")
EOF
