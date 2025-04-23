#!/usr/bin/env python3
import os
import sys
import signal
import subprocess
import time
import psutil

BOT_PROCESS = None
LOG_FILE = "bot.log"

def find_bot_process():
    """Найти процесс бота"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower() and 'bot.main' in ' '.join(proc.info['cmdline']):
                return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def start_bot():
    """Запустить бота"""
    global BOT_PROCESS
    
    if find_bot_process():
        print("❌ Бот уже запущен")
        return
        
    try:
        # Запускаем бота в фоновом режиме с перенаправлением вывода в лог
        with open(LOG_FILE, 'a') as log_file:
            BOT_PROCESS = subprocess.Popen(
                [sys.executable, '-m', 'bot.main'],
                stdout=log_file,
                stderr=log_file,
                preexec_fn=os.setsid
            )
        print("✅ Бот успешно запущен")
        print(f"📝 Логи записываются в {LOG_FILE}")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {str(e)}")

def stop_bot():
    """Остановить бота"""
    bot_process = find_bot_process()
    if not bot_process:
        print("❌ Бот не запущен")
        return
        
    try:
        # Отправляем сигнал SIGTERM всей группе процессов
        os.killpg(os.getpgid(bot_process.pid), signal.SIGTERM)
        print("✅ Бот успешно остановлен")
    except Exception as e:
        print(f"❌ Ошибка при остановке бота: {str(e)}")

def restart_bot():
    """Перезапустить бота"""
    print("🔄 Перезапуск бота...")
    stop_bot()
    time.sleep(2)  # Ждем, пока процесс полностью остановится
    start_bot()

def show_status():
    """Показать статус бота"""
    bot_process = find_bot_process()
    if bot_process:
        print("✅ Бот запущен")
        print(f"📊 PID: {bot_process.pid}")
        print(f"⏱️ Время работы: {time.time() - bot_process.create_time():.0f} секунд")
    else:
        print("❌ Бот не запущен")

def show_logs(lines=10):
    """Показать последние логи"""
    try:
        with open(LOG_FILE, 'r') as log_file:
            logs = log_file.readlines()
            print("📝 Последние логи:")
            print(''.join(logs[-lines:]))
    except FileNotFoundError:
        print("❌ Файл логов не найден")

def main():
    """Основная функция"""
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python manage.py start    - Запустить бота")
        print("  python manage.py stop     - Остановить бота")
        print("  python manage.py restart  - Перезапустить бота")
        print("  python manage.py status   - Показать статус")
        print("  python manage.py logs     - Показать логи")
        return

    command = sys.argv[1].lower()
    
    if command == 'start':
        start_bot()
    elif command == 'stop':
        stop_bot()
    elif command == 'restart':
        restart_bot()
    elif command == 'status':
        show_status()
    elif command == 'logs':
        show_logs()
    else:
        print(f"❌ Неизвестная команда: {command}")

if __name__ == '__main__':
    main() 