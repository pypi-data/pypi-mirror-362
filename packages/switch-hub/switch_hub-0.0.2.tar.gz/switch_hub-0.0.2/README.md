**Switch-Hub**  
switch-hub — это удобная утилита для переключения между разными источниками моделей и датасетов: Hugging Face Hub,
Cloud.ru Repo. Она позволяет прозрачно работать с моделями и датасетами в разных экосистемах, не изменяя привычный
интерфейс.

### Основные возможности

- Лёгкое переключение между хранилищами: Hugging Face Hub, Cloud.ru Repo.
- Минимальные изменения в коде — привычный интерфейс transformers, datasets, diffusers ....
- Гибкость для CI/CD, исследований и продакшена.

### Установка

```bash
pip install switch-hub
```

### Пример использования

```python
from transformers import AutoModel
from switch_hub import HubSwitcher

switcher = HubSwitcher()

# Переключаемся на Hugging Face Hub
switcher.switch_to_hf()
model = AutoModel.from_pretrained('dmitryradionov/some-model')

# Переключаемся на Repo Cloud.ru и пушим модель туда
switcher.switch_to_rh()
model.push_to_hub('70e5f7a7-f6a7-4fd7-a8ea-e288150b6fb8/some-model')

# Загружаем модель из Cloud.ru Repo 
model_mr = AutoModel.from_pretrained('70e5f7a7-f6a7-4fd7-a8ea-e288150b6fb8/some-model')

# Снова переключаемся на Hugging Face Hub и пушим модель назад
switcher.switch_to_hf()
model_mr.push_to_hub("dmitryradionov/some-model")
```

---

## Работа с аутентификацией и токенами

Для работы с приватными и большинством публичных репозиториев, потребуется токен доступа:

- **Hugging Face Hub:** `HF_TOKEN`
- **Cloud.ru Repo:** `RH_TOKEN` (**обязателен всегда**)

#### Как передавать токены

**1. Через переменные окружения или .env файл**  
Рекомендуется для локальной разработки и CI/CD:  
Пример `.env`:

```dotenv
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
RH_TOKEN=rh_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

**2. Явно в конструктор HubSwitcher**

```python
from switch_hub import HubSwitcher

switcher = HubSwitcher(
    hf_token="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    rh_token="rh_yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
)
```

#### Важно:

- **RH_TOKEN обязателен для Cloud.ru Repo всегда**
- **HF_TOKEN обязателен только для приватных репозиториев Hugging Face, но рекомендуется указывать всегда**, чтобы
  избежать лимитов и быть готовым к работе с приватным контентом Hugging Face
- Никогда не публикуйте свои токены в открытых источниках — используйте секреты сборки и переменные окружения

---

### Описание ключевых методов

**reset()**  
Восстанавливает все переменные окружения и внутренние настройки, которые были изменены при переключении между хабами.
Используйте этот метод, если нужно вручную откатить все изменения состояния, внесённые switcher'ом, например после
завершения операций с приватным registry.

**Пример:**

```python
switcher.switch_to_rh()
# ... работа с приватным хабом ...
switcher.reset()  # Возвращение к исходным параметрам окружения
```

**context(mode)**  
Контекстный менеджер для временного переключения хаба.  
После выхода из блока with окружение автоматически восстанавливается к исходному.

**Пример:**

```python
from switch_hub import HubSwitcher

switcher = HubSwitcher()

with switcher.context('rh'):
    # В этом блоке все операции проходят через Cloud.ru Repo
    model = AutoModel.from_pretrained('cloudru_id/some-model')
    # ... другие операции ...

# После выхода из блока — автоматически восстановлен Hugging Face/прежний хаб
# mode: может быть 'hf' (Hugging Face Hub) или 'rh' (Cloud.ru Repo)
```

---

### Кейсы использования

- **Исследование новых моделей:** переключайтесь между публичными репозиториями и приватным registry.
- **Экспорт и импорт моделей между облаком и Hugging Face.**
- **Автоматизация CI/CD пайплайнов для MLOps.**

---

**P.S.** Эти способы аутентификации работают для моделей, датасетов, diffusers и других библиотек, поддерживаемых
switch-hub.  
_Рекомендуется всегда указывать RH_TOKEN и HF_TOKEN через переменные окружения или секреты инфраструктуры для
максимальной гибкости и безопасности._