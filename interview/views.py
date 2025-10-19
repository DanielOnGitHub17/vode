from django.shortcuts import render
from datetime import datetime

# Create your views here.

def interview(request):
    """
    Interview view - displays the technical interview interface
    TODO: Will fetch role, round, candidate from database later
    """
    
    # Mock candidate object to simulate OneToOneField with User
    class MockUser:
        first_name = "John"
        last_name = "Doe"

    class MockCandidate:
        def __init__(self):
            self.user = MockUser()
    
    context = {
        'role': {
            'title': 'Senior Software Engineer',
        },
        'round': {
            'number': 1,
            'time': datetime.now().strftime('%I:%M %p'),
        },
        'candidate': MockCandidate(),
        'interview': {
            'question_text': '''
<div class="question-section">
    <h6 class="text-muted mb-2">Description</h6>
    <p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return <strong>indices of the two numbers</strong> such that they add up to <code>target</code>.</p>
    <p>You may assume that each input would have <strong>exactly one solution</strong>, and you may not use the same element twice.</p>
    <p>You can return the answer in any order.</p>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Examples</h6>
    
    <div class="mb-3">
        <strong>Example 1:</strong>
        <pre class="code-example"><code>Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].</code></pre>
    </div>
    
    <div class="mb-3">
        <strong>Example 2:</strong>
        <pre class="code-example"><code>Input: nums = [3,2,4], target = 6
Output: [1,2]</code></pre>
    </div>
    
    <div class="mb-3">
        <strong>Example 3:</strong>
        <pre class="code-example"><code>Input: nums = [3,3], target = 6
Output: [0,1]</code></pre>
    </div>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Constraints</h6>
    <ul>
        <li>2 ≤ nums.length ≤ 10<sup>4</sup></li>
        <li>-10<sup>9</sup> ≤ nums[i] ≤ 10<sup>9</sup></li>
        <li>-10<sup>9</sup> ≤ target ≤ 10<sup>9</sup></li>
        <li>Only one valid answer exists</li>
    </ul>
</div>

<div class="question-section">
    <h6 class="text-muted mb-2">Follow-up</h6>
    <p>Can you come up with an algorithm that is less than <strong>O(n²)</strong> time complexity?</p>
</div>
''',
        }
    }

    return render(request, "interview/index.html", context)

