# Официальный образ Python
FROM python:3.11-alpine

# Рабочая директория
WORKDIR /app

# Зависимости из requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Все остальные файлы
COPY . .

# Убедиться, что Python может импортировать модули на всякий случай
ENV PYTHONPATH=/app/src

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from power import calculate_expression; result = calculate_expression('2 2 +'); assert result == 4, f'HealthCheck: ожидалось 4, получено {result}'"

# Точка входа (перезапуск калькулятора после ошибки/успешного вычисления)
CMD ["sh", "-c", "while true; do python src/main.py; echo 'Перезапуск...'; sleep 2; done"]
