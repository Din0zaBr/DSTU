"""
Типы данных для модуля шифрования

Определяет типы данных для типизации алгоритмов шифрования и сравнения.
"""

from typing import TypedDict, Literal


# Типы размеров ключей
AESKeySize = Literal[128, 192, 256]


class AlgorithmSpecification(TypedDict):
    """Технические характеристики алгоритма"""
    Название: str
    Страна: str
    Стандарт: str
    Размер_блока: str
    Размер_ключа: str
    Количество_раундов: str
    Тип: str
    Статус: str
    Применение: str


class SecurityAnalysis(TypedDict):
    """Анализ безопасности алгоритма"""
    Криптостойкость: str
    Атаки: str
    Рекомендуемый_размер_ключа: str
    Стандартизация: str
    Сертификация: str


class PerformanceMetrics(TypedDict):
    """Метрики производительности алгоритма"""
    Размер_данных: str
    Время_шифрования: str
    Время_расшифрования: str
    Скорость_шифрования: str
    Скорость_расшифрования: str
    Корректность: bool


class ComparisonResults(TypedDict):
    """Результаты сравнения алгоритмов"""
    AES: dict
    ГОСТ_Магма: dict


AlgorithmName = Literal['AES', 'ГОСТ (Магма)']

