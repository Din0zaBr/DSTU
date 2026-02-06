"""
Модуль для сравнительного анализа алгоритмов шифрования

Предоставляет класс для сравнения различных алгоритмов блочного шифрования.
Поддерживает расширяемую систему методов сравнения.
"""

from typing import Dict, Any, Optional, List

from .base_encryption import BlockCipher
from .comparison_methods import (
    ComparisonMethod,
    SpecificationsComparison,
    SecurityComparison,
    PerformanceComparison,
    MemoryUsageComparison,
    KeySizeComparison,
    BlockSizeComparison,
    ThroughputComparison,
    LatencyComparison,
    EnergyConsumptionComparison,
    ParallelizationComparison,
    ResistanceToAttacksComparison,
)
from .types import AlgorithmSpecification, SecurityAnalysis, PerformanceMetrics


class EncryptionComparison:
    """
    Класс для сравнительного анализа алгоритмов шифрования
    
    Поддерживает расширяемую систему методов сравнения.
    Можно добавлять новые методы сравнения через register_method().
    """
    
    def __init__(
        self,
        algorithms: Optional[Dict[str, BlockCipher]] = None,
        comparison_methods: Optional[List[ComparisonMethod]] = None
    ) -> None:
        """
        Инициализация сравнительного анализа
        
        Args:
            algorithms: Словарь с алгоритмами для сравнения {name: algorithm}
            comparison_methods: Список методов сравнения (если None, используются стандартные)
        """
        if algorithms is None:
            algorithms = {}
        
        self.algorithms: Dict[str, BlockCipher] = algorithms
        
        # Регистрация стандартных методов сравнения
        if comparison_methods is None:
            comparison_methods = [
                SpecificationsComparison(),
                SecurityComparison(),
                PerformanceComparison(),
            ]
        
        self.comparison_methods: Dict[str, ComparisonMethod] = {
            method.get_name(): method for method in comparison_methods
        }
    
    def register_method(self, method: ComparisonMethod) -> None:
        """
        Регистрация нового метода сравнения
        
        Args:
            method: Метод сравнения (экземпляр класса, наследующего ComparisonMethod)
        
        Example:
            >>> custom_method = MyCustomComparison()
            >>> comparison = EncryptionComparison()
            >>> comparison.register_method(custom_method)
        """
        self.comparison_methods[method.get_name()] = method
    
    def add_algorithm(self, name: str, algorithm: BlockCipher) -> None:
        """
        Добавление алгоритма для сравнения
        
        Args:
            name: Имя алгоритма
            algorithm: Экземпляр алгоритма шифрования
        """
        self.algorithms[name] = algorithm
    
    def compare_specifications(self) -> Dict[str, AlgorithmSpecification]:
        """
        Сравнение технических характеристик алгоритмов
        
        Returns:
            Словарь с характеристиками обоих алгоритмов
        """
        method = self.comparison_methods.get('Технические характеристики')
        if method:
            return method.compare(self.algorithms)
        return {}
    
    def security_analysis(self) -> Dict[str, SecurityAnalysis]:
        """
        Анализ безопасности алгоритмов
        
        Returns:
            Словарь с анализом безопасности
        """
        method = self.comparison_methods.get('Анализ безопасности')
        if method:
            return method.compare(self.algorithms)
        return {}
    
    def performance_test(self, data_size: int = 1024 * 1024) -> Dict[str, PerformanceMetrics]:
        """
        Тест производительности алгоритмов
        
        Args:
            data_size: Размер тестовых данных в байтах
        
        Returns:
            Словарь с результатами тестирования
        """
        method = PerformanceComparison(data_size=data_size)
        return method.compare(self.algorithms)
    
    def compare_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Выполняет все зарегистрированные методы сравнения
        
        Returns:
            Словарь с результатами всех методов сравнения
        """
        results: Dict[str, Dict[str, Any]] = {}
        
        for method_name, method in self.comparison_methods.items():
            results[method_name] = method.compare(self.algorithms)
        
        return results
    
    def print_comparison(self) -> None:
        """
        Вывод подробного сравнительного анализа
        
        Выводит результаты всех зарегистрированных методов сравнения
        в удобочитаемом формате.
        """
        print("\n" + "="*80)
        print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ АЛГОРИТМОВ БЛОЧНОГО ШИФРОВАНИЯ")
        print("="*80)
        
        # Получаем все результаты сравнения
        all_results = self.compare_all()
        
        # Выводим результаты каждого метода
        for index, (method_name, method_results) in enumerate(all_results.items(), start=1):
            print(f"\n{index}. {method_name.upper()}")
            print("-" * 80)
            
            for algo_name, algo_results in method_results.items():
                print(f"\n{algo_name}:")
                if isinstance(algo_results, dict):
                    for key, value in algo_results.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  {algo_results}")
        
        print("\n" + "="*80)
    
    def get_available_methods(self) -> List[str]:
        """
        Возвращает список доступных методов сравнения
        
        Returns:
            Список названий доступных методов сравнения
        """
        return list(self.comparison_methods.keys())

