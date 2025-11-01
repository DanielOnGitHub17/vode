from interview.services.gemini_service import GeminiService
from interview.services.elevenlabs_service import ElevenLabsService
import logging
import base64

logger = logging.getLogger(__name__)


class InterviewOrchestrator:
    """Orchestrates the interview flow with AI agent reasoning"""

    def __init__(self):
        self.gemini = GeminiService()
        self.elevenlabs = ElevenLabsService()

    def start_interview(self, question_data, interview_context):
        """
        Initialize interview context so the AI agent understands the problem space.
        Called when the interview page loads.

        Args:
            question_data: Dict with title, statement, test_cases from actual Question
            interview_context: Dict with role, difficulty

        Returns:
            Dict with success status
        """
        try:
            self.gemini.initialize_context(question_data, interview_context)

            return {"success": True}
        except Exception as e:
            logger.error(f"Error starting interview: {e}")
            return {"success": False, "error": str(e)}

    def get_ai_response(self, candidate_code, audio_transcript, interview_context):
        """
        AI agent evaluates continuous code + audio transcript updates.
        Frontend sends these intermittently.
        Gemini maintains conversation history for all exchanges.

        Handles:
        - Initial code submission
        - Code updates
        - Candidate questions
        - Follow-ups (using conversation history)

        Args:
            candidate_code: Current code from editor (may be partial or empty)
            audio_transcript: Current audio transcript (may be partial or empty)
            interview_context: Interview metadata

        Returns:
            Dict with audio bytes, reasoning, and success status
        """
        reasoning = ""
        audio = b""

        try:
            if not candidate_code and not audio_transcript:
                return {
                    "success": False,
                    "error": "No code or transcript provided",
                    "reasoning": "",
                    "audio": b"",
                }

            # Try to get reasoning from Gemini
            try:
                reasoning = self.gemini.agent_reasoning(
                    candidate_code, audio_transcript, interview_context
                )
            except Exception as gemini_error:
                logger.error(f"Error getting Gemini reasoning: {gemini_error}")
                reasoning = "I'm having trouble analyzing your submission right now. Please continue working and try again."

            # Try to convert reasoning to speech (separate try block)
            try:
                if reasoning:
                    audio = self.elevenlabs.text_to_speech(reasoning)
            except Exception as audio_error:
                logger.error(f"Error generating audio: {audio_error}")
                audio = b""  # Empty audio if TTS fails

            return {"audio": audio, "reasoning": reasoning, "success": True}
        except Exception as e:
            logger.error(f"Error evaluating submission: {e}")
            return {
                "success": False,
                "error": str(e),
                "reasoning": (
                    reasoning
                    if reasoning
                    else "An error occurred processing your submission."
                ),
                "audio": audio,
            }

    def end_interview(self, success_metrics_list=None):
        """
        Generate end-of-interview score, feedback, and closing message.
        Called when interview timer runs out or candidate completes interview.

        Args:
            success_metrics_list: List of metrics (e.g., ['Correctness', 'Code Efficiency', 'Communication'])
                                 Set by SWE for each round. If None, uses generic metrics.

        Returns:
            Dict with:
            - score: Integer 0-100
            - feedback: String with structured feedback
            - message: Closing message text
            - audio: MP3 audio bytes (base64) or empty string if TTS fails
            - success: Boolean
        """
        score = 50  # Default score
        feedback = ""

        try:
            if not success_metrics_list:
                success_metrics_list = [
                    "Correctness",
                    "Code Quality",
                    "Problem-Solving Approach",
                    "Communication",
                ]

            # Try to get scoring from Gemini
            try:
                scoring_result = self.gemini.score_interview(success_metrics_list)
                score = scoring_result.get("score", 50)
                feedback = scoring_result.get("feedback", "")
            except Exception as scoring_error:
                logger.error(f"Error getting interview score: {scoring_error}")
                score = 50
                feedback = "Interview completed. Detailed feedback will be provided by your recruiter."

            self.gemini.clear_context()

            return {
                "score": score,
                "feedback": feedback,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Error generating end-of-interview evaluation: {e}")
            return {
                "score": score,
                "feedback": feedback or "Unable to generate detailed feedback",
                "success": False,
                "error": str(e),
            }
