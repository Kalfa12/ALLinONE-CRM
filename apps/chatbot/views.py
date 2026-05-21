import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import translation
from django.views.decorators.http import require_POST

from .models import ChatMessage, ChatSession
from .services import ask_deepseek


@login_required
@require_POST
def chat(request):
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid JSON'}, status=400)

    message = (data.get('message') or '').strip()
    if not message:
        return JsonResponse({'error': 'empty message'}, status=400)

    session_id = data.get('session_id')
    if session_id:
        try:
            session = ChatSession.objects.get(pk=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            session = ChatSession.objects.create(user=request.user)
    else:
        session = ChatSession.objects.create(user=request.user)

    history = [
        {'role': m.role, 'content': m.content}
        for m in session.messages.all()[:20]
    ]

    ChatMessage.objects.create(session=session, role='user', content=message)

    try:
        reply = ask_deepseek(
            user=request.user,
            user_message=message,
            history=history,
            language=translation.get_language() or 'en',
        )
    except Exception as exc:  # surface upstream failures to the UI
        return JsonResponse(
            {'error': f'DeepSeek call failed: {exc}'}, status=502,
        )

    ChatMessage.objects.create(session=session, role='assistant', content=reply)

    return JsonResponse({'reply': reply, 'session_id': session.id})
