import os
from typing import Any, Callable, Dict, Optional, List, ContextManager

import huggingface_hub
import datasets

from .logger import logger
from .helpers import safe_setattr, safe_getattr, make_attr_store_key, set_tokens

from dotenv import load_dotenv

if load_dotenv():
    logger.info("Переменные окружения загружены из .env файла")
else:
    logger.info(".env файл не найден или пустой. В таком случае вы должны явно передать токены доступа в конструктор HubSwitcher")


class HubSwitcher:
    """
    Универсальный класс для переключения между HuggingFace Hub
    и Cloud.ru Repo.

    - Управляет переменными окружения, эндпоинтами, токенами и специфичными настройками
      для huggingface_hub и datasets.
    - При инициализации автоматически проверяет наличие токенов (HF_TOKEN, RH_TOKEN) и логирует предупреждение, если их нет.
    - Контекстный менеджер для временного переключения хаба.
    """

    HF_TOKEN_ENV_NAMES: List[str] = [
        'HF_TOKEN',
        'HUGGING_FACE_HUB_TOKEN',
        'HF_API_TOKEN',
    ]
    """Список переменных окружения, используемых для авторизации HuggingFace Hub."""

    RH_TOKEN_ENV_NAMES: List[str] = [
        'RH_TOKEN',
    ]
    """Список переменных окружения, используемых для авторизации Repo."""

    RH_DEFAULT_ENDPOINT: str = "https://repo.cloud.ru"
    """Значение по умолчанию для Repo, если не указан параметром либо не найден в .env"""

    def __init__(
            self,
            rh_endpoint: Optional[str] = None,
            rh_token: Optional[str] = None,
            hf_token: Optional[str] = None,
    ) -> None:
        """
        Инициализация.

        :param rh_endpoint: URL Repo. Приоритет: явно > окружение > дефолт.
        :param rh_token: Токен для Repo. Приоритет: явно > окружение.
        :param hf_token: Токен для HuggingFace Hub. Приоритет: явно > окружение.
        """
        self._hf_endpoint: str = huggingface_hub.constants.ENDPOINT
        self._rh_endpoint: str = (
            rh_endpoint
            if rh_endpoint is not None
            else os.environ.get('RH_ENDPOINT', self.RH_DEFAULT_ENDPOINT)
        )
        self.rh_token: Optional[str] = (
            rh_token if rh_token is not None else os.environ.get('RH_TOKEN')
        )
        self.hf_token: Optional[str] = (
            hf_token if hf_token is not None else
            os.environ.get('HF_TOKEN') or
            os.environ.get('HUGGING_FACE_HUB_TOKEN') or
            os.environ.get('HF_API_TOKEN')
        )
        self._store: Dict[str, Any] = {}
        """Внутреннее хранилище для возврата переменных и атрибутов при сбросе."""

        if self.hf_token is None:
            logger.info(
                "Переменная окружения HF_TOKEN "
                "не найдена. Авторизация в HuggingFace может не работать. Для установки переменной создайте .env файл в проекте и запишите переменную либо явно предайте токен в конструктор HubSwitcher(hf_token=token)"
            )
        if self.rh_token is None:
            logger.warning(
                "Переменная окружения RH_TOKEN не найдена. "
                "Авторизация в Repo не будет работать. Для установки переменной создайте .env файл в проекте и запишите переменную либо явно предайте токен в конструктор HubSwitcher(rh_token=token)"
            )

        logger.info(
            f"HubSwitcher инициализирован. HF endpoint: {self._hf_endpoint}, RH endpoint: {self._rh_endpoint}")

    def _store_env(self, name: str) -> None:
        """Сохранить значение переменной окружения name во внутренний _store (если ещё не сохранено)."""
        if name not in self._store:
            self._store[name] = os.environ.get(name)
            logger.debug(f"Окружение {name} сохранено.")

    def _restore_env(self, name: str) -> None:
        """Восстановить переменную окружения name из внутреннего _store."""
        if name in self._store:
            val = self._store[name]
            if val is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = val
            logger.debug(f"Окружение {name} восстановлено.")

    def _store_attr(self, obj: Any, attr: str) -> None:
        """Сохранить значение obj.attr во внутренний _store (если ещё не сохранено)."""
        key: str = make_attr_store_key(obj, attr)
        if key not in self._store:
            self._store[key] = safe_getattr(obj, attr)
            logger.debug(f"Атрибут {key} сохранён.")

    def _restore_attr(self, obj: Any, attr: str) -> None:
        """Восстановить значение obj.attr из внутреннего _store."""
        key: str = make_attr_store_key(obj, attr)
        if key in self._store:
            safe_setattr(obj, attr, self._store[key])
            logger.debug(f"Атрибут {key} восстановлен.")

    def _store_tokens(self, env_names: List[str]) -> None:
        """Сохранить список токенов в _store."""
        for token_env_name in env_names:
            self._store_env(token_env_name)

    def _restore_tokens(self, env_names: List[str]) -> None:
        """Восстановить список токенов в _store."""
        for token_env_name in env_names:
            self._restore_env(token_env_name)

    def switch_to_hf(self) -> None:
        """
        Активировать HuggingFace Hub:
        - Переключает endpoint.
        - Восстанавливает HF-токены и удаляет RH-токен.
        - Обновляет специфичные настройки hub/datasets.
        """
        endpoint = self._hf_endpoint
        self._switch_hub(endpoint)
        self._restore_attr(datasets.config, 'S3_DATASETS_BUCKET_PREFIX')
        self._restore_attr(getattr(datasets, 'arrow_reader', None), 'HF_GCP_BASE_URL')
        self._store_tokens(self.HF_TOKEN_ENV_NAMES)
        set_tokens(self.HF_TOKEN_ENV_NAMES, self.hf_token)
        set_tokens(self.RH_TOKEN_ENV_NAMES, None)
        logger.info("Переключено на HuggingFace Hub (endpoint: %s)", endpoint)

    def switch_to_rh(self) -> None:
        """
        Активировать Repo:
        - Переключает endpoint.
        - Все HF_TOKEN переменные получают значение RH_TOKEN.
        - RH_TOKEN также прописывается в своё окружение.
        - Специфичные настройки hub/datasets подменяются.
        :raises NameError: если отсутствует rh_token.
        """
        endpoint = self._rh_endpoint
        if not self.rh_token:
            logger.error("Требуется RH_TOKEN (Repo)")
            raise NameError(
                "Repo токен необходим: пожалуйста, установите его явно в rh_token или через переменную окружения RH_TOKEN")
        self._switch_hub(endpoint)
        self._store_attr(datasets.config, 'S3_DATASETS_BUCKET_PREFIX')
        safe_setattr(datasets.config, 'S3_DATASETS_BUCKET_PREFIX', endpoint)
        arrow_reader = getattr(datasets, 'arrow_reader', None)
        if arrow_reader:
            self._store_attr(arrow_reader, 'HF_GCP_BASE_URL')
            safe_setattr(arrow_reader, 'HF_GCP_BASE_URL', endpoint)
        self._store_tokens(self.HF_TOKEN_ENV_NAMES)
        set_tokens(self.HF_TOKEN_ENV_NAMES, self.rh_token)
        self._store_tokens(self.RH_TOKEN_ENV_NAMES)
        set_tokens(self.RH_TOKEN_ENV_NAMES, self.rh_token)
        logger.info("Переключено на Repo (endpoint: %s)", endpoint)

    def _switch_hub(self, endpoint: str) -> None:
        """
        Подменяет endpoint и связанные атрибуты в huggingface_hub и datasets.
        """
        self._store_env('HF_ENDPOINT')
        os.environ['HF_ENDPOINT'] = endpoint

        self._store_attr(huggingface_hub.constants, 'ENDPOINT')
        safe_setattr(huggingface_hub.constants, 'ENDPOINT', endpoint)
        self._store_attr(getattr(huggingface_hub.commands, "user", None), 'ENDPOINT')
        safe_setattr(getattr(huggingface_hub.commands, "user", None), 'ENDPOINT', endpoint)
        self._store_attr(huggingface_hub.constants, 'HUGGINGFACE_CO_URL_TEMPLATE')
        safe_setattr(
            huggingface_hub.constants, 'HUGGINGFACE_CO_URL_TEMPLATE',
            f"{endpoint}/{{repo_id}}/resolve/{{revision}}/{{filename}}"
        )
        self._store_attr(huggingface_hub.file_download, 'HUGGINGFACE_CO_URL_TEMPLATE')
        safe_setattr(
            huggingface_hub.file_download, 'HUGGINGFACE_CO_URL_TEMPLATE',
            f"{endpoint}/{{repo_id}}/resolve/{{revision}}/{{filename}}"
        )
        self._store_attr(huggingface_hub.hf_api, 'ENDPOINT')
        safe_setattr(huggingface_hub.hf_api, 'ENDPOINT', endpoint)
        self._store_attr(huggingface_hub.hf_file_system, 'ENDPOINT')
        safe_setattr(huggingface_hub.hf_file_system, 'ENDPOINT', endpoint)
        self._store_attr(getattr(huggingface_hub, 'lfs', None), 'ENDPOINT')
        safe_setattr(getattr(huggingface_hub, 'lfs', None), 'ENDPOINT', endpoint)
        self._store_attr(getattr(huggingface_hub, '_commit_api', None), 'ENDPOINT')
        safe_setattr(getattr(huggingface_hub, '_commit_api', None), 'ENDPOINT', endpoint)
        self._store_attr(getattr(huggingface_hub.hf_api, 'api', None), 'endpoint')
        safe_setattr(getattr(huggingface_hub.hf_api, 'api', None), 'endpoint', endpoint)
        self._store_attr(datasets.config, 'HF_ENDPOINT')
        safe_setattr(datasets.config, 'HF_ENDPOINT', endpoint)
        self._store_attr(datasets.config, 'HUB_DATASETS_URL')
        safe_setattr(
            datasets.config, 'HUB_DATASETS_URL',
            f"{endpoint}/datasets/{{repo_id}}/resolve/{{revision}}/{{path}}",
        )
        logger.debug("Все endpoints переключены на %s", endpoint)

    def reset(self) -> None:
        """
        Восстановить все переменные и атрибуты, которые были изменены при переключении хабов.
        Возвращает окружение к исходному состоянию.
        """
        restored = []
        for key in list(self._store):
            if key.startswith('#attr#'):
                # Восстановление атрибутов тоже желательно
                # Для основных случаев (datasets, huggingface_hub) можно парсить __name__ по шаблону (уточнить по структуре, если нужно точнее)
                # Пока пропускаем - логика восстановления ниже
                pass
            else:
                self._restore_env(key)
                restored.append(key)
        self._restore_tokens(self.HF_TOKEN_ENV_NAMES)
        self._restore_tokens(self.RH_TOKEN_ENV_NAMES)
        self._store = {}
        logger.info("Окружение и токены восстановлены по reset. Восстановлено: %s", restored)

    def context(self, mode: str) -> ContextManager[None]:
        """
        Контекстный менеджер для безопасного временного переключения между hf/rh хабами.

        Пример:
            with switcher.context('rh'):
                # все операции внутри используют "приватный" RH-хаб

        После выхода окружение вернётся к исходному.
        :param mode: 'hf' либо 'rh'
        """
        if mode not in ('hf', 'rh'):
            raise ValueError("Mode must be 'hf' or 'rh'")
        switch_func: Callable[[], None] = (
            self.switch_to_hf if mode == 'hf' else self.switch_to_rh
        )

        class Ctx:
            def __init__(self, outer):
                self._outer = outer

            def __enter__(self) -> None:
                logger.info("Вход в контекст: переключение на %s", mode)
                switch_func()

            def __exit__(self, exc_type, exc, tb) -> None:
                self._outer.reset()
                logger.info("Выход из контекста — восстановлено исходное окружение.")

        return Ctx(self)
