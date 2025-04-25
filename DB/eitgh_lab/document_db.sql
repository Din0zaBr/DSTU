-- Создание таблицы для хранения документов
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    doc_type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tags VARCHAR(50)[]
);

-- Создание индекса для быстрого поиска по JSONB полям
CREATE INDEX idx_documents_data ON documents USING gin (data jsonb_path_ops);

-- Создание индекса для быстрого поиска по типу документа
CREATE INDEX idx_documents_type ON documents (doc_type);

-- Создание индекса для быстрого поиска по тегам
CREATE INDEX idx_documents_tags ON documents USING gin (tags);

-- Функция для автоматического обновления поля updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для автоматического обновления поля updated_at
CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Вставка примеров документов

-- 1. Вставка документа типа "user"
INSERT INTO documents (doc_type, data, tags)
VALUES (
    'user',
    '{
        "name": "Иван Иванов",
        "age": 30,
        "email": "ivan@example.com",
        "address": {
            "city": "Москва",
            "street": "Ленина",
            "house": 42
        },
        "is_active": true,
        "roles": ["admin", "user"]
    }',
    ARRAY['person', 'admin', 'test']
);

-- 2. Вставка документа типа "product"
INSERT INTO documents (doc_type, data, tags)
VALUES (
    'product',
    '{
        "title": "Смартфон",
        "brand": "Xiaomi",
        "model": "Redmi Note 10",
        "price": 24999.99,
        "in_stock": true,
        "specs": {
            "memory": "128GB",
            "ram": "6GB",
            "screen": "6.5\" AMOLED"
        },
        "colors": ["черный", "белый", "синий"]
    }',
    ARRAY['electronics', 'mobile', 'popular']
);

-- 3. Вставка документа типа "order"
INSERT INTO documents (doc_type, data, tags)
VALUES (
    'order',
    '{
        "order_id": "ORD-2023-001",
        "customer_id": 12345,
        "items": [
            {
                "product_id": 101,
                "quantity": 2,
                "price": 24999.99
            },
            {
                "product_id": 205,
                "quantity": 1,
                "price": 5999.99
            }
        ],
        "total": 55999.97,
        "status": "processing",
        "delivery": {
            "address": "ул. Ленина, д.10, кв.25",
            "method": "courier",
            "estimated_date": "2023-12-15"
        }
    }',
    ARRAY['sales', 'current', 'priority']
);

-- 4. Вставка документа типа "article"
INSERT INTO documents (doc_type, data, tags)
VALUES (
    'article',
    '{
        "title": "Топ технологий 2023 года",
        "author": "Иван Петров",
        "publish_date": "2023-01-15",
        "content": "В этом году появилось много новых технологий в области искусственного интеллекта...",
        "category": "technology",
        "views": 1542,
        "comments": [
            {
                "user": "Анна",
                "text": "Отличная статья!",
                "date": "2023-01-16"
            },
            {
                "user": "Петр",
                "text": "Спасибо за информацию",
                "date": "2023-01-17"
            }
        ],
        "tags": ["AI", "innovation", "trends"]
    }',
    ARRAY['publication', 'tech', 'popular']
);

-- 5. Вставка документа типа "event"
INSERT INTO documents (doc_type, data, tags)
VALUES (
    'event',
    '{
        "name": "IT-конференция 2023",
        "date": "2023-05-20",
        "location": "Москва, Крокус Экспо",
        "organizer": "IT Events Inc.",
        "speakers": [
            {
                "name": "Анна Смирнова",
                "topic": "Будущее технологий и инноваций"
            },
            {
                "name": "Петр Иванов",
                "topic": "Тренды 2023 года"
            }
        ],
        "tickets": {
            "available": 250,
            "sold": 180,
            "price": 5000.00
        },
        "registration_required": true
    }',
    ARRAY['conference', 'it', 'business']
);
