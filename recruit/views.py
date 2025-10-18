from django.shortcuts import render

def index(request):
    roles = [
        {
            'id': 1,
            'title': 'Backend Engineer',
            'description': 'Python/Django developer for backend systems'
        },
        {
            'id': 2,
            'title': 'Frontend Engineer',
            'description': 'React/TypeScript developer for web interfaces'
        },
        {
            'id': 3,
            'title': 'Product Manager',
            'description': 'Lead product strategy and roadmap'
        },
    ]
    return render(request, 'recruit/index.html', {'roles': roles})

def role_detail(request, role_id):
    roles_data = {
        1: {'id': 1, 'title': 'Backend Engineer', 'description': 'Python/Django developer for backend systems'},
        2: {'id': 2, 'title': 'Frontend Engineer', 'description': 'React/TypeScript developer for web interfaces'},
        3: {'id': 3, 'title': 'Product Manager', 'description': 'Lead product strategy and roadmap'},
    }
    
    candidates_data = {
        1: [
            {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'current_round': 1, 'notes': 'Strong Python skills'},
            {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'current_round': 1, 'notes': 'Good problem solver'},
            {'id': 3, 'name': 'Carol Davis', 'email': 'carol@example.com', 'current_round': 2, 'notes': 'Excellent communication'},
            {'id': 4, 'name': 'David Lee', 'email': 'david@example.com', 'current_round': 3, 'notes': 'Outstanding candidate'},
        ],
        2: [
            {'id': 5, 'name': 'Emma Wilson', 'email': 'emma@example.com', 'current_round': 1, 'notes': 'React expert'},
            {'id': 6, 'name': 'Frank Brown', 'email': 'frank@example.com', 'current_round': 2, 'notes': 'Good TypeScript knowledge'},
        ],
        3: [
            {'id': 7, 'name': 'Grace Martinez', 'email': 'grace@example.com', 'current_round': 1, 'notes': 'Strategic thinker'},
        ],
    }
    
    role = roles_data.get(role_id)
    active_tab = int(request.GET.get('tab', 1))
    
    # Filter candidates by current_round based on active_tab
    all_candidates = candidates_data.get(role_id, [])
    candidates = [c for c in all_candidates if c['current_round'] == active_tab]
    
    return render(request, 'recruiter/role_detail.html', {
        'role': role,
        'candidates': candidates,
        'active_tab': active_tab
    })
