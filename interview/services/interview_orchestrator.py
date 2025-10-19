from interview.services.gemini_service import GeminiService
from interview.services.elevenlabs_service import ElevenLabsService
from interview.mocks import MOCK_QUESTION
import logging

logger = logging.getLogger(__name__)


class InterviewOrchestrator:
    """Orchestrates the interview flow with AI agent reasoning"""
    
    def __init__(self):
        self.gemini = GeminiService()
        self.elevenlabs = ElevenLabsService()
    
    def start_interview(self, interview_context):
        """
        Initialize interview context so the AI agent understands the problem space.
        Called when the interview page loads.
        
        Args:
            interview_context: Dict with role, round, difficulty, total_rounds
        
        Returns:
            Dict with question and success status
        """
        try:
            question = MOCK_QUESTION            
            self.gemini.initialize_context(question, interview_context)
            
            return {
                'question': question,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error starting interview: {e}")
            return {
                'success': False,
                'error': str(e),
                'question': MOCK_QUESTION
            }
    
    def get_ai_response(self, candidate_code, audio_transcript, interview_context):
        """
        AI agent evaluates continuous code + audio transcript updates.
        Frontend sends these intermittently based on inactivity.
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
            Dict with audio bytes and success status
        """
        try:
            if not candidate_code and not audio_transcript:
                return {
                    'success': False,
                    'error': 'No code or transcript provided'
                }
            
            reasoning = self.gemini.agent_reasoning(
                candidate_code,
                audio_transcript,
                interview_context
            )
            
            # Convert reasoning to speech
            audio = self.elevenlabs.text_to_speech(reasoning)
            
            return {
                'audio': audio,
                'reasoning': reasoning,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error evaluating submission: {e}")
            return {
                'success': False,
                'error': str(e)
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
            - audio: MP3 audio bytes of closing message
            - success: Boolean
        """
        try:
            if not success_metrics_list:
                success_metrics_list = ['Correctness', 'Code Quality', 'Problem-Solving Approach', 'Communication']
            
            scoring_result = self.gemini.score_interview(success_metrics_list)
            score = scoring_result['score']
            feedback = scoring_result['feedback']
            end_message = f"""Thank you for taking the time to interview with us today. We appreciate your participation and the effort you put into solving this problem. Your recruiter will be reaching out to you shortly with feedback and next steps. We look forward to staying in touch!"""
            audio = self.elevenlabs.text_to_speech(end_message)
            self.gemini.clear_context()
            
            return {
                'score': score,
                'feedback': feedback,
                'message': end_message,
                'audio': audio,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error generating end-of-interview evaluation: {e}")
            return {
                'score': 0,
                'feedback': 'Unable to generate feedback',
                'message': '',
                'audio': None,
                'success': False,
                'error': str(e)
            }
