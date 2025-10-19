import base64
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
# from .mocks import MOCK_QUESTION
from interview.services.interview_orchestrator import InterviewOrchestrator

logger = logging.getLogger(__name__)
orchestrator = InterviewOrchestrator()
QUESTION_THRESHOLD = 5  # could be 1000


def end(request, id: int):
    """End the interview and save video URLs."""
    mock_candidate = Candidate.objects.first()

    try:
        interview_obj = Interview.objects.select_related(
            "candidate", "round", "round__role"
        ).get(id=id)

        if interview_obj.candidate != mock_candidate:
            messages.error(request, "You are not authorized to view this interview.")
            return redirect("/candidate/")
        
        screen_video = request.GET.get('screen_video', '')
        candidate_video = request.GET.get('candidate_video', '')
        
        if screen_video:
            interview_obj.screen_video = screen_video
        if candidate_video:
            interview_obj.candidate_video = candidate_video
        
        if screen_video or candidate_video:
            interview_obj.save()
            logger.info(f"Saved video URLs for interview {id}")
        
        end_result = orchestrator.end_interview(interview_obj.round.success_metrics_list)
        
        interview_obj.completed_at = datetime.now()
        if interview_obj.score == 0 and end_result.get("success"):
            score = end_result.get("score", 50)
            score = max(0, min(100, int(score))) if score else 50

            interview_obj.score = score
            interview_obj.notes = end_result.get("feedback", "")

        interview_obj.save()

        audio_data = end_result.get("audio", b"")
        if isinstance(audio_data, bytes):
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        else:
            audio_base64 = audio_data

        context = {
            "audio": audio_base64
        }
        
        messages.success(request, "Interview completed successfully!")
        return render(request, "interview/end.html", context)
        
    except Interview.DoesNotExist:
        messages.error(request, "Interview not found.")
        return redirect("/candidate/")


def interview(request, id: int):
    """
    Interview view - displays the technical interview interface
    """
    mock_candidate = Candidate.objects.first()  # TODO: request.user.candidate
    print(mock_candidate.user.get_full_name())
    
    try:
        interview_obj = Interview.objects.get(id=id)

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
            "role": interview_obj.round.role.title,
            "difficulty": interview_obj.round.difficulty_level,
        }
        
        # Prepare question data for AI initialization
        question_data = {
            "title": question.title,
            "statement": question.statement,
            "test_cases": question.test_cases,
        }

        # Initialize the AI agent with full context about the problem
        orchestrator.start_interview(question_data, interview_context)

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
        code = data.get("code", "")
        audio_transcript = data.get("audio_transcript", "")
        interview_id = data.get("interview_id")
        
        # Get interview context
        interview = Interview.objects.select_related("round", "round__role").get(id=interview_id)
        context = {
            "role": interview.round.role.title,
            "difficulty": interview.round.difficulty_level,
        }

        # Get AI coaching feedback (Gemini maintains conversation history)
        result = orchestrator.get_ai_response(
            code,
            audio_transcript,
            context
        )

        result["audio"] = base64.b64encode(result["audio"]).decode("utf-8")

        if result["success"]:
            # Return JSON with reasoning text and audio
            return JsonResponse({
                "reasoning": result.get("reasoning", result.get("message", "")),
                "audio": result.get("audio", ""),  # Base64 encoded audio
                "success": True
            })
        else:
            return JsonResponse({"error": result["error"]}, status=500)
    except Interview.DoesNotExist:
        return JsonResponse({"error": "Interview not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        logger.error(f"Error processing code/transcript: {e}")
        return JsonResponse({"error": str(e)}, status=500)


def generate_interview_question(interview: Interview) -> Question:
    """
    Generate and create a Question object for an interview
    
    Args:
        interview: Interview model instance
    
    Returns:
        Question: A Question model instance
    """
    latest_questions = Question.objects.filter(round=interview.round).order_by('-id')[:QUESTION_THRESHOLD]
    question_titles = [question.title for question in latest_questions]
    
    context = {
        "difficulty": interview.round.difficulty_level,
        "topics": interview.round.data_structures,
        "already_picked": ", ".join(question_titles) if question_titles else "None",
    }

    question = orchestrator.gemini.get_question(context)
    question, created = Question.objects.get_or_create(
        title=question["title"],
        defaults={
            "statement": question["statement"],
            "test_cases": question["test_cases"],
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
        interview_id = data.get("interview_id")
        
        # Get interview to fetch metrics
        interview = Interview.objects.select_related("round").get(id=interview_id)
        
        # Get success metrics from the round
        success_metrics = interview.round.success_metrics_list
        
        # Get score and feedback from orchestrator
        result = orchestrator.end_interview(success_metrics)
        
        if result["success"]:
            # Save score and feedback to Interview model
            score = result.get("score", 50)
            
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
            
            feedback = result.get("feedback", "")
            
            interview.score = score
            interview.notes = feedback
            interview.completed_at = datetime.now()
            interview.save()
            
            logger.info(f"Interview {interview_id} completed with score {score}/100")
            
            return JsonResponse({
                "score": score,
                "feedback": feedback,
                "audio": None,  # Frontend will handle binary audio separately if needed
                "message": result["message"],
                "success": True
            })
        else:
            return JsonResponse({
                "error": result.get("error", "Unknown error"),
                "success": False
            }, status=500)
    except Interview.DoesNotExist:
        return JsonResponse({"error": "Interview not found", "success": False}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON", "success": False}, status=400)
    except Exception as e:
        logger.error(f"Error ending interview: {e}")
        return JsonResponse({"error": str(e), "success": False}, status=500)


