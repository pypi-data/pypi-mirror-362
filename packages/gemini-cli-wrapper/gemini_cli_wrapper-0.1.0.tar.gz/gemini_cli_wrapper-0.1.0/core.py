import subprocess
import os
import sys

class GeminiCLIError(Exception):
    """Кастомное исключение для ошибок при работе с Gemini CLI."""
    pass

class GeminiCLIWrapper:
    """
    Оболочка для взаимодействия с утилитой командной строки Gemini CLI.

    Требует, чтобы утилита `gemini` была установлена и доступна в системном PATH,
    а также чтобы была выполнена аутентификация через `gcloud auth application-default login`.
    """
    def __init__(self, project_id: str):
        """
        Инициализирует оболочку.

        :param project_id: Ваш Google Cloud Project ID.
        """
        if not project_id:
            raise ValueError("Необходимо указать project_id.")
        self.project_id = project_id

    def ask(self, user_prompt: str, system_prompt: str = "") -> str:
        """
        Отправляет запрос к Gemini.

        :param user_prompt: Запрос от пользователя.
        :param system_prompt: Системный промпт для задания контекста.
        :return: Ответ от модели в виде строки.
        :raises GeminiCLIError: Если произошла ошибка при вызове CLI.
        """
        env = os.environ.copy()
        env["GOOGLE_CLOUD_PROJECT"] = self.project_id
        env["PYTHONIOENCODING"] = "utf-8"
        # Для кросс-платформенной совместимости
        if sys.platform.startswith('linux') or sys.platform == 'darwin':
            env["LANG"] = "en_US.UTF-8"

        full_prompt = f"System: {system_prompt}\nUser: {user_prompt}" if system_prompt else user_prompt

        # Кросс-платформенный вызов
        if sys.platform == "win32":
            command = ["powershell", "-ExecutionPolicy", "Bypass", "-Command", f'gemini --prompt "{full_prompt}"']
        else:
            # Для Linux и macOS команда проще
            command = ["gemini", "--prompt", full_prompt]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                env=env,
                encoding="utf-8",
                check=True  # Эта опция вызовет исключение при коде возврата != 0
            )
            return result.stdout.strip()
        except FileNotFoundError:
            raise GeminiCLIError("Команда 'gemini' не найдена. Убедитесь, что Google Cloud CLI установлен и находится в PATH.")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip()
            raise GeminiCLIError(f"Ошибка при вызове Gemini CLI:\n{error_message}")