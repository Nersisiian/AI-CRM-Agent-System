# 🧠 AI Business Agent Swarm — Production-Grade Multi-Agent System

[![CI](https://github.com/Nersisiian/AI-CRM-Agent-System/actions/workflows/ci.yml/badge.svg)](https://github.com/Nersisiian/AI-CRM-Agent-System/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/type%20checked-mypy-blue)](https://mypy-lang.org/)

**AI бизнес‑агенты нового поколения:** мульти‑агентная архитектура, собственный LLM‑хостинг (vLLM), RAG‑поиск по документам, файн‑тюнинг (QLoRA), интеграция с CRM и полный production‑стек.

Разработано как демонстрация **Senior AI Engineer** уровня для внедрения AI‑агентов в реальные бизнес‑процессы: продажи, поддержка, удержание клиентов.

---
``
## 🧩 Архитектура
┌─────────────────────────────────────────────────────┐
│ FastAPI │
│ ┌───────────┐ ┌───────────┐ ┌─────────────────┐ │
│ │ /chat │ │ /ingest │ │ /health /metrics│ │
│ └─────┬─────┘ └─────┬─────┘ └─────────────────┘ │
│ │ │ │
│ ┌─────▼───────────────▼──────────────────────────┐ │
│ │ AgentOrchestrator │ │
│ │ ┌─────────────────┐ ┌────────────────────┐ │ │
│ │ │ SalesAgent │ │ SupportAgent │ │ │
│ │ │ (CRM tools) │ │ (KB tools) │ │ │
│ │ └────────┬────────┘ └────────┬───────────┘ │ │
│ │ │ │ │ │
│ │ ┌────────▼────────────────────▼───────────┐ │ │
│ │ │ Shared Memory (Redis) / RAG │ │ │
│ │ └──────────────────────────────────────────┘ │ │
│ └──────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────┘
│
┌───────────────────┼───────────────────┐
│ │ │
▼ ▼ ▼
┌─────────┐ ┌─────────────┐ ┌─────────────┐
│ vLLM / │ │ Qdrant / │ │ PostgreSQL │
│ OpenAI │ │ Chroma │ │ + Redis │
└─────────┘ └─────────────┘ └─────────────┘

``

### Ключевые компоненты

| Компонент | Назначение |
|----------|------------|
| **AgentOrchestrator** | Классифицирует намерение пользователя и направляет запрос к нужному агенту |
| **SalesAgent** | Работает с CRM-инструментами: создание лидов, просмотр сделок, поиск клиентов |
| **SupportAgent** | Использует базу знаний (RAG) для ответов на вопросы, создаёт тикеты |
| **RetentionService** | Анализирует риск оттока клиентов и генерирует персональные предложения |
| **RAG Pipeline** | Ingestion + retrieval с поддержкой Qdrant / Chroma |
| **vLLM / OpenAI** | Гибкая абстракция LLM: своя модель (Mistral-7B) или OpenAI API |
| **Fine‑tuning** | QLoRA‑скрипты для адаптации open‑source LLM под бизнес‑задачи |
| **Memory** | Краткосрочная память диалогов в Redis (TTL 1 час) |
| **CI/CD** | GitHub Actions: линтинг (ruff), проверка типов (mypy), тесты (pytest), сборка Docker‑образов |

---

## 🚀 Быстрый старт

### Предварительные требования
- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)
- NVIDIA GPU + CUDA (если используете vLLM локально)
- OpenAI API ключ (для облачного режима)


### 1. Клонирование репозитория
```bash
git clone https://github.com/Nersisiian/AI-CRM-Agent-System.git
cd AI-CRM-Agent-System
2. Настройка окружения
bash
cp .env.example .env
# Отредактируйте .env:
# - LLM_PROVIDER=vllm или openai
# - OPENAI_API_KEY=sk-... (если используете OpenAI)
# - Настройки подключения к БД и Redis
3. Запуск с Docker Compose
bash
docker-compose up -d
Поднимутся все сервисы: приложение, vLLM, Qdrant, PostgreSQL, Redis.
```
4. Проверка работоспособности
```
curl http://localhost:8000/api/v1/health
5. Локальная разработка (без Docker)
bash
pip install -r requirements.txt
python scripts/init_db.py
python scripts/seed_data.py
uvicorn main:app --reload
```
📡 API Endpoints
```
POST /api/v1/chat
Основной чат с агентом.

curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Создай лид для клиента ivan@example.com",
    "session_id": "optional-session-id"
  }'
```
Ответ:
````
json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Лид создан, ID: ...",
  "sources": []
}
POST /api/v1/ingest
Загрузка PDF‑документа в базу знаний.

curl -X POST http://localhost:8000/api/v1/ingest \
  -F "file=@knowledge_base.pdf"
````
Ответ:
```
json
{
  "status": "success",
  "chunks_stored": 42,
  "filename": "knowledge_base.pdf"
}
GET /api/v1/health
json
{"status": "ok"}
GET /api/v1/metrics
json
{
  "chat_requests": 1023,
  "chat_errors": 7,
  "ingest_requests": 15
}

```
🛠 Инструменты агента
`
Инструмент	Описание
get_customer_by_email	Поиск клиента в CRM по email
create_lead	Создание нового лида
list_recent_deals	Список последних сделок
get_churn_risk	Оценка риска оттока клиента
generate_retention_offer	Генерация персонального предложения для удержания
``
🏭 Production‑ready особенности
Чистая архитектура (dependency injection, разделение слоёв)

Асинхронный код (FastAPI + asyncio + асинхронные коннекторы)

Обработка ошибок (retry для LLM‑вызовов, graceful degradation)

Rate limiting (настраиваемый через RATE_LIMIT_PER_SECOND)

Структурированное логирование (structlog)

Метрики (эндпоинт /metrics)

Healthcheck'и (для всех сервисов в docker‑compose)

Контейнеризация (Docker Compose с изолированными сервисами)

CI/CD (автоматический линтинг, тесты, сборка образов)

Безопасность (переменные окружения для секретов, не хранятся в коде)
``
``
🔬 Тонкая настройка (QLoRA)
Проект включает пайплайн для файн‑тюнинга open‑source LLM под бизнес‑задачи.
``
1. Подготовка данных

python app/training/prepare_dataset.py
Входные данные — JSONL с диалогами в ShareGPT формате.
``
2. Запуск обучения

python app/training/run_qlora.py
Используется 4‑битное квантование (bitsandbytes) и LoRA‑адаптеры (peft).
`
3. Слияние адаптера с базовой моделью

python app/training/merge_and_export.py
Результат сохраняется в models/merged-sales-agent.
`
📊 Мониторинг и эксплуатация
Логи: все важные события логируются через structlog в едином формате.
``
Метрики: доступны через /api/v1/metrics, легко интегрируются с Prometheus.

Healthcheck'и: каждый сервис в docker‑compose имеет healthcheck, оркестратор Docker перезапускает упавшие контейнеры.

Rate limiting: защита от перегрузок, настраивается через env.
``
🧪 Тестирование
`
# Юнит‑тесты
pytest tests/ -v

# Линтинг
ruff check app/

# Проверка типов
mypy app/
CI на GitHub Actions выполняет все проверки автоматически при каждом пуше в main.

🗺 Roadmap (планы развития)
Web UI для чата и администрирования

Real‑time дашборды активности агентов

Поддержка multi‑turn диалогов с глубиной памяти > 1

Интеграция с amoCRM / Bitrix24 через готовые коннекторы

A/B тестирование промптов

Автоматическое переобучение по новым данным (active learning)

🤝 Вклад в проект
Приветствуется! Пожалуйста, создавайте Issue и Pull Request.
Следуйте стилю кода (ruff), добавляйте тесты.

📝 Лицензия
MIT. См. файл LICENSE.

👨‍💻 Автор
Nersisiian 
GitHub
