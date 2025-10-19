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
            
            # Initialize the AI agent with full context
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
    
    def get_question_with_audio(self):
        """Get the Two Sum question and convert to speech"""
        try:
            question = MOCK_QUESTION
            
            # Extract clean text for speech - use the HTML-stripped version
            speech_text = f"{question['title']}. {question['statement']}"
            
            # Convert to speech
            audio = self.elevenlabs.text_to_speech(speech_text)
            
            return {
                'question': question,
                'audio': audio,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error getting question: {e}")
            return {
                'success': False,
                'error': str(e),
                'question': MOCK_QUESTION
            }
    
    def agent_evaluate_submission(self, candidate_code, audio_transcript, interview_context):
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
            # If both code and transcript are empty, return error
            if not candidate_code and not audio_transcript:
                return {
                    'success': False,
                    'error': 'No code or transcript provided'
                }
            
            # Get AI agent reasoning (uses conversation history internally)
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
    
    def end_interview(self):
        """Clean up interview context"""
        self.gemini.clear_context()
