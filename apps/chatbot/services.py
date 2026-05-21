"""Thin wrapper around the DeepSeek chat-completions API."""
import requests
from django.conf import settings

from .context import build_crm_context

LANG_NAMES = {'en': 'English', 'fr': 'French', 'ar': 'Arabic'}


def ask_deepseek(user, user_message: str, history: list[dict],
                 language: str = 'en') -> str:
    """Send a message to DeepSeek with live CRM context injected.

    Returns the assistant's reply as plain text.
    """
    facts = build_crm_context(user)
    lang_name = LANG_NAMES.get(language, 'English')

    system_prompt = (
        f"You are an expert digital-marketing assistant embedded in a CRM. "
        f"Always reply in {lang_name}. Be concise (max 6 sentences) and "
        f"actionable. Base every claim on these live CRM facts:\n\n{facts}\n\n"
        f"If the question cannot be answered from these facts, say so."
    )

    payload = {
        'model': settings.DEEPSEEK_MODEL,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            *history,
            {'role': 'user', 'content': user_message},
        ],
        'temperature': 0.4,
        'stream': False,
    }
    headers = {
        'Authorization': f'Bearer {settings.DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json',
    }

    if not settings.DEEPSEEK_API_KEY:
        return ('[DeepSeek API key not configured. Set DEEPSEEK_API_KEY in '
                'your .env file to enable live answers.]')

    r = requests.post(
        f'{settings.DEEPSEEK_BASE_URL}/chat/completions',
        json=payload, headers=headers, timeout=30,
    )
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']
