import requests
from django.conf import settings


class AIService:
    @staticmethod
    def _call_llm(messages, max_tokens=1000, temperature=0.7):
        provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()

        if provider == 'groq':
            url = "https://api.groq.com/openai/v1/chat/completions"
            api_key = getattr(settings, 'GROQ_API_KEY', '')
            model = "llama-3.3-70b-versatile"
        else:  # megallm
            url = f"{getattr(settings, 'MEGALLM_API_URL', 'https://api.megallm.uz/v1')}/chat/completions"
            api_key = getattr(settings, 'MEGALLM_API_KEY', '')
            model = "default"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"[AI Provider {provider.upper()} Error]: HTTP {response.status_code} - {response.text}"
        except Exception as e:
            return f"[AI Service Offline/Fallback Response]: Detailed analysis for your request could not connect to {provider} ({str(e)})."

    @classmethod
    def check_essay(cls, essay_text, prompt_topic=None):
        prompt = (
            f"You are an expert IELTS Writing examiner. Evaluate the following essay.\n"
            f"Topic: {prompt_topic or 'General Essay Topic'}\n\n"
            f"Essay:\n{essay_text}\n\n"
            f"Provide feedback in structured format:\n"
            f"1. Task Achievement Score & Feedback\n"
            f"2. Coherence and Cohesion Score & Feedback\n"
            f"3. Lexical Resource Score & Feedback\n"
            f"4. Grammatical Range and Accuracy Score & Feedback\n"
            f"5. Overall Estimated Band Score\n"
            f"6. Detailed Suggestions for Improvement"
        )
        messages = [{"role": "system", "content": "You are a professional writing evaluator."},
                    {"role": "user", "content": prompt}]
        return cls._call_llm(messages, max_tokens=1500)

    @classmethod
    def grammar_fix(cls, text):
        prompt = (
            f"Correct the grammar, spelling, and phrasing of the following text while preserving its original meaning.\n"
            f"Text: {text}\n\n"
            f"Provide:\n"
            f"1. Corrected Version\n"
            f"2. Explanation of mistakes fixed"
        )
        messages = [{"role": "system", "content": "You are a precise grammar correction assistant."},
                    {"role": "user", "content": prompt}]
        return cls._call_llm(messages, max_tokens=800)

    @classmethod
    def generate_roadmap(cls, target_goal, current_level):
        prompt = (
            f"Create a step-by-step personalized learning roadmap.\n"
            f"Target Goal: {target_goal}\n"
            f"Current Level: {current_level}\n\n"
            f"Provide a week-by-week structured action plan with recommended resources, daily practice habits, and milestones."
        )
        messages = [{"role": "system", "content": "You are an expert educational career coach."},
                    {"role": "user", "content": prompt}]
        return cls._call_llm(messages, max_tokens=1500)

    @classmethod
    def check_homework(cls, homework_description, submission_text):
        prompt = (
            f"Evaluate this student's homework submission against the task requirement.\n"
            f"Requirement: {homework_description}\n"
            f"Submission: {submission_text}\n\n"
            f"Provide score out of 100, strengths, weaknesses, and constructive feedback."
        )
        messages = [{"role": "system", "content": "You are a helpful teacher assistant."},
                    {"role": "user", "content": prompt}]
        return cls._call_llm(messages, max_tokens=1000)

    @classmethod
    def writing_band_prediction(cls, essay_text):
        prompt = (
            f"Predict the IELTS Writing band score (0-9) for this text and explain why in 3 bullet points.\n"
            f"Text: {essay_text}"
        )
        messages = [{"role": "system", "content": "You are an IELTS band predictor."},
                    {"role": "user", "content": prompt}]
        return cls._call_llm(messages, max_tokens=500)
