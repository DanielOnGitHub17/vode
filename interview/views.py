from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

from cand.models import Candidate
from .models import Question, Interview
from .mocks import MOCK_QUESTION

def end(request, id: int):
    """
    End the interview.
    """
    pass


def interview(request, id: int):
    """
    Interview view - displays the technical interview interface
    """
    mock_candidate = Candidate.objects.first()  # TODO: request.user.candidate
    
    try:
        interview_obj = Interview.objects.select_related(
            "candidate", "round", "round__role", "question"
        ).get(id=id)
        
        # Security: Verify interview belongs to this candidate
        if interview_obj.candidate != mock_candidate:
            messages.error(request, "You are not authorized to view this interview.")
            return redirect("/candidate/")
        
        # Check if interview has been completed
        if interview_obj.completed_at is not None:
            messages.warning(request, "This interview has already been completed.")
            return redirect("/candidate/")
        
        # Generate question if not already assigned
        if interview_obj.question is None:
            question = generate_interview_question(interview_obj)
            interview_obj.question = question
            interview_obj.save()
        else:
            question = interview_obj.question

        context = {
            "interview": interview_obj,
            "candidate": mock_candidate,
            "question": question,
        }

        return render(request, "interview/index.html", context)
        
    except Interview.DoesNotExist:
        messages.error(request, "Interview not found.")
        return redirect("/candidate/")


def generate_interview_question(interview: Interview) -> Question:
    """
    Generate and create a Question object for an interview
    Randomly selects or creates a question from the round"s question pool
    
    Args:
        interview: Interview model instance
    
    Returns:
        Question: A Question model instance
    """
    # TODO: Implement smart question selection
    # - Check if round has existing questions
    # - Select one that hasn't been used for this candidate
    # - Or create a new question from a question bank/API
    
    # For now, create a mock question
    question, created = Question.objects.get_or_create(
        title=MOCK_QUESTION["title"],
        defaults={
            "statement": MOCK_QUESTION["statement"],
            "test_cases": MOCK_QUESTION["test_cases"],
            "round": interview.round
        }
    )
    
    return question

