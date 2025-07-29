from .smart import SmartMenu
from .version import __version__

# === Проверка обновления ===
import threading
import requests

def _check_for_update():
    try:
        resp = requests.get("https://pypi.org/pypi/TH_Menu/json", timeout=2)
        latest = resp.json()["info"]["version"]
        if latest != __version__:
            print(f"\n📦 TH_Menu: доступна новая версия v{latest} (установлена v{__version__})")
            print("🔁 Обновите: pip install -U TH_Menu\n")
    except Exception:
        pass  # не мешаем пользователю

# Запуск в фоновом потоке
threading.Thread(target=_check_for_update, daemon=True).start()
