import os
from .logger import logger
from typing import Optional, Any, List


def safe_setattr(obj: Optional[Any], name: str, value: Any) -> None:
    """Безопасно вызвать setattr, если obj не None и у него есть нужный атрибут, и value не None."""
    if obj is not None and hasattr(obj, name) and value is not None:
        setattr(obj, name, value)


def safe_getattr(obj: Optional[Any], name: str) -> Any:
    """Безопасно вызвать getattr, если obj не None и у него есть нужный атрибут."""
    if obj is not None and hasattr(obj, name):
        return getattr(obj, name)
    return None


def make_attr_store_key(obj: Any, attr: str) -> str:
    """
    Сформировать уникальный ключ по объекту и атрибуту для внутреннего хранения/восстановления.
    """
    if hasattr(obj, "__name__"):
        obj_id = obj.__name__
    elif hasattr(obj, "__module__") and hasattr(obj, "__class__"):
        obj_id = f'{obj.__module__}.{obj.__class__.__name__}'
    else:
        obj_id = type(obj).__name__
    return f'#attr#{obj_id}.{attr}'


def set_tokens(env_names: List[str], value: Optional[str]) -> None:
    """Установить или удалить переменные окружения (в т.ч. HF_TOKEN)."""
    for token_env_name in env_names:
        if value is None:
            os.environ.pop(token_env_name, None)
        else:
            os.environ[token_env_name] = value
        logger.debug(f"Токен {token_env_name} установлен." if value else f"Токен {token_env_name} удалён.")
