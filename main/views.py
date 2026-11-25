
import json
import urllib.parse
import urllib.request
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


def home(request):
    return render(request, 'main/home.html')


def get_telegram_settings():
    env_path = Path(settings.BASE_DIR) / '.env'

    if not env_path.exists():
        raise ValueError('Файл .env не найден')

    values = {}

    for line in env_path.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()

        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        values[key.strip()] = value.strip()

    return (
        values['TELEGRAM_BOT_TOKEN'],
        values['TELEGRAM_CHAT_ID'],
    )


@require_POST
def training_signup(request):
    name = request.POST.get('name', '').strip()
    phone = request.POST.get('phone', '').strip()
    training = request.POST.get('training', '').strip()

    if not name or not phone or not training:
        return JsonResponse(
            {'success': False, 'error': 'Заповніть усі поля.'},
            status=400,
        )

    if len(name) > 100 or len(phone) > 30 or len(training) > 100:
        return JsonResponse(
            {'success': False, 'error': 'Перевірте введені дані.'},
            status=400,
        )

    message = (
        '🥊 НОВА ЗАЯВКА — 1UA BOXING\n\n'
        f'👤 Ім’я: {name}\n'
        f'📞 Телефон: {phone}\n'
        f'🥊 Тренування: {training}'
    )

    try:
        token, chat_id = get_telegram_settings()

        url = f'https://api.telegram.org/bot{token}/sendMessage'

        data = urllib.parse.urlencode({
            'chat_id': chat_id,
            'text': message,
        }).encode('utf-8')

        with urllib.request.urlopen(url, data=data, timeout=10) as response:
            result = json.load(response)

        if not result.get('ok'):
            raise ValueError('Telegram не підтвердив відправлення')

    except Exception:
        return JsonResponse(
            {
                'success': False,
                'error': 'Не вдалося надіслати заявку. Спробуйте пізніше.',
            },
            status=500,
        )

    return JsonResponse({
        'success': True,
        'message': 'Дякуємо! Ми скоро з вами зв’яжемося.',
    })

def privacy(request):
    return render(request, 'main/privacy.html')
