"""
Скрипт для запуску тестів та вимірювання покриття коду.
Для встановлення залежностей: pip install coverage
"""

import unittest
import sys
from io import StringIO
import os

# Додаємо шляхи до модулів
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests_with_coverage():
    """Запускає тести з вимірюванням покриття коду"""
    try:
        import coverage
    except ImportError:
        print("Помилка: coverage не встановлено.")
        print("Встановіть: pip install coverage")
        return False
    
    # Ініціалізуємо об'єкт coverage
    cov = coverage.Coverage(
        source=['route', 'route_builder', 'ticket'],
        omit=['test_*.py', '*/__pycache__/*']
    )
    
    # Починаємо вимірювання
    cov.start()
    
    # Завантажуємо і запускаємо тести
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Додаємо всі тести
    suite.addTests(loader.discover('.', pattern='test_*.py'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Завершуємо вимірювання
    cov.stop()
    cov.save()
    
    print("\n" + "="*70)
    print("ЗВІТ ПОКРИТТЯ КОДУ")
    print("="*70 + "\n")
    
    # Виводимо звіт
    cov.report()
    
    # Генеруємо HTML звіт
    try:
        cov.html_report(directory='htmlcov')
        print("\nHTML звіт генеровано в папці 'htmlcov'")
        print("Відкрийте 'htmlcov/index.html' у браузері для детального аналізу")
    except Exception as e:
        print(f"Помилка при генеруванні HTML звіту: {e}")
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("✓ Всі тести пройдені успішно!")
    else:
        print(f"✗ Деякі тести не пройдені ({len(result.failures)} помилок, {len(result.errors)} помилок)")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


def run_tests_simple():
    """Запускає тести без вимірювання покриття"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Додаємо всі тести
    suite.addTests(loader.discover('.', pattern='test_*.py'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--simple':
        # Запуск тестів без покриття
        success = run_tests_simple()
    else:
        # Запуск тестів з покриттям
        success = run_tests_with_coverage()
    
    # Повертаємо код виходу
    sys.exit(0 if success else 1)
