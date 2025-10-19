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
    - reasoning: Text response from AI
    - audio: Base64 encoded MP3 audio feedback
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

        print("got result", result)

        if result['success']:
            # Return JSON with reasoning text and audio
            return JsonResponse({
                'reasoning': result.get('reasoning', result.get('message', '')),
                'audio': result.get('audio', ''),  # Base64 encoded audio
                'success': True
            })
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
    End interview endpoint: Generate AI-based score, feedback, and closing audio.
    Called when interview timer runs out or candidate completes interview.
    
    Frontend sends:
    - interview_id: Which interview to end
    
    Backend:
    1. Fetches Round.success_metrics from the interview
    2. Calls orchestrator.end_interview() with metrics
    3. Saves score and feedback to Interview model
    4. Returns JSON with score, feedback, and audio MP3
    
    Returns:
        JSON with score (0-100), feedback (string), audio (MP3 bytes)
    """
    try:
        data = json.loads(request.body)
        interview_id = data.get('interview_id')
        
        # Get interview to fetch metrics
        interview = Interview.objects.select_related('round').get(id=interview_id)
        
        # Get success metrics from the round
        success_metrics = interview.round.success_metrics_list
        
        # Get score and feedback from orchestrator
        result = orchestrator.end_interview(success_metrics)
        
        if result['success']:
            # Save score and feedback to Interview model
            score = result.get('score', 50)
            
            # Ensure score is valid integer between 0-100
            if score is None:
                score = 50
            else:
                try:
                    score = int(score)
                    score = max(0, min(100, score))
                except (ValueError, TypeError):
                    logger.warning(f"Invalid score value: {score}, defaulting to 50")
                    score = 50
            
            feedback = result.get('feedback', '')
            
            interview.score = score
            interview.notes = feedback
            interview.completed_at = datetime.now()
            interview.save()
            
            logger.info(f"Interview {interview_id} completed with score {score}/100")
            
            return JsonResponse({
                'score': score,
                'feedback': feedback,
                'audio': None,  # Frontend will handle binary audio separately if needed
                'message': result['message'],
                'success': True
            })
        else:
            return JsonResponse({
                'error': result.get('error', 'Unknown error'),
                'success': False
            }, status=500)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found', 'success': False}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON', 'success': False}, status=400)
    except Exception as e:
        logger.error(f"Error ending interview: {e}")
        return JsonResponse({'error': str(e), 'success': False}, status=500)


