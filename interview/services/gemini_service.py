import google.generativeai as genai
from django.conf import settings
from interview.mocks import MOCK_QUESTION
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        self.conversation_history = []
    
    def get_question(self):
        """Return the Two Sum question from mocks"""
        return MOCK_QUESTION
    
    def initialize_context(self, question_data, interview_context):
        """
        Initialize the interview context for the AI agent.
        This establishes the problem space and expectations.
        
        Args:
            question_data: The question details (title, statement, examples, constraints)
            interview_context: Interview metadata (role, round, difficulty)
        """
        context_prompt = f"""
You are a professional AI coding interviewer designed to conduct standardized, fair, and consistent technical interviews for software engineering candidates.

INTERVIEW SETUP:
- Position: {interview_context.get('role', 'Backend Engineer')}
- Round: {interview_context.get('round', 1)} of {interview_context.get('total_rounds', 3)}
- Difficulty Level: {interview_context.get('difficulty', 'Medium')}

PROBLEM BEING SOLVED:
Title: {question_data.get('title', 'Two Sum')}

Problem Statement:
{question_data.get('statement', '')}

Constraints:
{question_data.get('constraints', '')}

Examples:
{question_data.get('examples', '')}

YOUR ROLE:
Be polite, encouraging, and professional — act like a real interviewer who wants the candidate to succeed, not a grader.

GUIDELINES:
1. Never reveal the exact answer, final code, or the data structure or algorithm name directly.
2. Offer subtle guidance and hints only when the candidate is stuck or explicitly requests help.
3. Encourage candidates to think aloud, reason through trade-offs, and write clean, efficient, and well-structured code.
4. Assess the candidate's approach, logic, and communication, not just correctness.
5. Provide feedback in a clear, structured, and concise manner:
   - What they did well (be specific)
   - What could be improved
   - High-level guidance for next steps
6. Maintain a collaborative tone: you are a supportive interviewer, not a tutor or debugger.
7. Do not write or modify the candidate's code yourself. Instead, offer targeted feedback or gentle redirections.
8. Be consistent in your evaluation standards to ensure fairness.
9. Avoid giving away test cases, edge cases, or full code solutions.
10. Focus on their thought process, not just the code.

COMMUNICATION STYLE:
- Be conversational and approachable, not robotic
- Ask "why" or "what if" questions to deepen their thinking
- If you spot issues, guide them to discover the problems themselves
- Balance encouragement with constructive critique
- Challenge assumptions gently
- Ask ONE powerful question that deepens their thinking when providing feedback

You will now evaluate the candidate's submission and provide interview feedback based on these principles.
        """
        
        # Initialize conversation history with context
        self.conversation_history = [
            {
                "role": "user",
                "parts": [{"text": context_prompt}]
            },
            {
                "role": "model",
                "parts": [{"text": "I understand. I'm a professional coding interviewer. I'll evaluate this candidate's code and reasoning fairly, offering guidance without spoiling the solution. I'll focus on their approach, logic, and communication while maintaining a supportive and collaborative tone. I'm ready to conduct a professional interview."}]
            }
        ]
    
    def agent_reasoning(self, candidate_code, audio_transcript, interview_context):
        """
        AI agent that reasons on the spot about candidate's submission.
        Takes code, audio transcript, and interview context to provide intelligent feedback.
        Uses conversation history to maintain context across all exchanges.
        
        This single method handles:
        - Code submissions
        - Code updates
        - Questions from candidate
        - Follow-ups (via conversation history)
        
        Args:
            candidate_code: Code from editor (may be empty if just asking a question)
            audio_transcript: Audio/voice transcript of candidate's explanation
            interview_context: Dict with interview details (used as context reference)
        
        Returns:
            Agent response with reasoning and feedback
        """
        submission_prompt = f"""
        CANDIDATE'S CURRENT INPUT:
        
        Code:
        ```python
        {candidate_code if candidate_code else '(No code provided)'}
        ```
        
        Candidate's Statement (from voice/text):
        "{audio_transcript if audio_transcript else '(No statement provided)'}"
        
        ANALYZE AND RESPOND:
        Evaluate this by considering:
        1. **Correctness**: Does the code solve the problem? Test against examples.
        2. **Approach**: What strategy are they using? Efficient?
        3. **Understanding**: Does their explanation match their code?
        4. **Edge Cases**: Handling all constraints?
        5. **Trade-offs**: Time vs space complexity considerations?
        
        PROVIDE COACHING FEEDBACK:
        - Acknowledge what they're doing well
        - Ask guiding questions to make them think (not rhetorical, genuine probes)
        - Hint at better approaches without spoiling
        - Challenge assumptions gently
        - Ask ONE powerful question that deepens their thinking
        
        Keep response conversational and actionable (2-3 paragraphs max).
        """
        
        try:
            # Add the submission to conversation history
            self.conversation_history.append({
                "role": "user",
                "parts": [{"text": submission_prompt}]
            })
            
            # Get response using conversation history
            response = self.model.generate_content(self.conversation_history)
            feedback = response.text
            
            # Add response to history for continuity
            self.conversation_history.append({
                "role": "model",
                "parts": [{"text": feedback}]
            })
            
            return feedback
        except Exception as e:
            logger.error(f"Gemini agent reasoning error: {e}")
            raise
    
    def clear_context(self):
        """Clear conversation history between interviews"""
        self.conversation_history = []
