from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import logging

from cand.models import Candidate
from .models import Question, Interview
from .mocks import MOCK_QUESTION
from interview.services.interview_orchestrator import InterviewOrchestrator

logger = logging.getLogger(__name__)
orchestrator = InterviewOrchestrator()


def interview(request, id: int):
    """
    Interview view - displays the technical interview interface
    """
    mock_candidate = Candidate.objects.first()  # TODO: request.user.candidate
    
    try:
        interview_obj = Interview.objects.select_related(
            "candidate", "round", "round__role", "question"
        ).get(id=id)
        
        if interview_obj.candidate != mock_candidate:
            messages.error(request, "You are not authorized to view this interview.")
            return redirect("/candidate/")
        
        if interview_obj.completed_at is not None:
            messages.warning(request, "This interview has already been completed.")
            return redirect("/candidate/")
        
        if interview_obj.question is None:
            question = generate_interview_question(interview_obj)
            interview_obj.question = question
            interview_obj.save()
        else:
            question = interview_obj.question

        interview_context = {
            'role': interview_obj.round.role.title,
            'round': interview_obj.round.round_number,
            'total_rounds': interview_obj.round.role.num_rounds,
            'difficulty': interview_obj.round.difficulty_level,
        }
        
        # Initialize the AI agent with full context about the problem
        orchestrator.start_interview(interview_context)

        context = {
            "interview": interview_obj,
            "candidate": mock_candidate,
            "question": question,
            "round": interview_obj.round,
            "role": interview_obj.round.role,
        }

        return render(request, "interview/index.html", context)
        
    except Interview.DoesNotExist:
        messages.error(request, "Interview not found.")
        return redirect("/candidate/")


@require_http_methods(["POST"])
@csrf_exempt
def get_response(request):
    """
    Main endpoint: Receive continuous code + audio updates from frontend.
    Frontend sends intermittently based on inactivity timer.
    
    Gemini maintains conversation history, so each call is contextualized
    with all previous exchanges. This handles:
    - Initial code submission
    - Code updates
    - Candidate questions
    - Follow-ups (no separate endpoint needed)
    
    Frontend sends:
    - code: Current code from editor (may be empty if just asking question)
    - audio_transcript: Current audio/text from candidate
    - interview_id: Which interview
    
    Backend returns:
    - audio: MP3 audio feedback (binary response)
    """
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        audio_transcript = data.get('audio_transcript', '')
        interview_id = data.get('interview_id')
        
        # Get interview context
        interview = Interview.objects.select_related('round', 'round__role').get(id=interview_id)
        context = {
            'role': interview.round.role.title,
            'round': interview.round.round_number,
            'difficulty': interview.round.difficulty_level,
        }
        
        # Get AI coaching feedback (Gemini maintains conversation history)
        result = orchestrator.get_ai_response(
            code,
            audio_transcript,
            context
        )
        
        if result['success']:
            # Return audio as binary response
            return HttpResponse(result['audio'], content_type='audio/mpeg')
        else:
            return JsonResponse({'error': result['error']}, status=500)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error processing code/transcript: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def generate_interview_question(interview: Interview) -> Question:
    """
    Generate and create a Question object for an interview
    
    Args:
        interview: Interview model instance
    
    Returns:
        Question: A Question model instance
    """
    # Create from mock question
    question, created = Question.objects.get_or_create(
        title=MOCK_QUESTION["title"],
        defaults={
            "statement": MOCK_QUESTION["statement"],
            "test_cases": MOCK_QUESTION["test_cases"],
            "round": interview.round
        }
    )
    
    return question


@require_http_methods(["POST"])
@csrf_exempt
def end_interview_audio(request):
    """
    Generate end-of-interview closing message as audio.
    Called when interview timer runs out or candidate completes interview.
    
    Returns:
        MP3 audio bytes with thank you message
    """
    try:
        result = orchestrator.end_interview()
        
        if result['success']:
            return HttpResponse(result['audio'], content_type='audio/mpeg')
        else:
            return JsonResponse({'error': result['error']}, status=500)
    except Exception as e:
        logger.error(f"Error generating end-of-interview audio: {e}")
        return JsonResponse({'error': str(e)}, status=500)

