#!/usr/bin/env python3
"""
Демонстрационный скрипт для домашнего задания
Показывает все возможности анализа кодирования изображений
"""

import os
import sys
from create_test_images import create_all_test_images
from hex_analyzer import HexAnalyzer
from compression_analyzer import CompressionAnalyzer

def print_header(title):
    """Печать заголовка"""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)

def print_section(title):
    """Печать раздела"""
    print(f"\n--- {title} ---")

def main():
    """Главная демонстрационная функция"""
    print_header("ДОМАШНЕЕ ЗАДАНИЕ №1: КОДИРОВАНИЕ ИЗОБРАЖЕНИЙ")
    print("Демонстрация всех возможностей анализа")
    
    print_section("1. СОЗДАНИЕ ТЕСТОВЫХ ИЗОБРАЖЕНИЙ")
    print("Создаем тестовые изображения различных типов...")
    
    # Создаем тестовые изображения
    test_files = create_all_test_images()
    
    print_section("2. HEX-АНАЛИЗ СТРУКТУРЫ ФАЙЛОВ")
    print("Анализируем структуру созданных файлов...")
    
    # Анализируем несколько файлов
    demo_files = [
        'test_images/test_minimal_black.png',
        'test_images/test_gradient_10x10.png',
        'test_images/test_colorful_50x50.png'
    ]
    
    for demo_file in demo_files:
        if os.path.exists(demo_file):
            analyzer = HexAnalyzer(demo_file)
            analyzer.analyze_file()
            print("\n" + "-"*60 + "\n")
    
    print_section("3. АНАЛИЗ СЖАТИЯ ИЗОБРАЖЕНИЙ")
    print("Сравниваем эффективность различных форматов...")
    
    # Анализируем сжатие
    compression_analyzer = CompressionAnalyzer()
    compression_analyzer.analyze_directory("test_images")
    
    print_section("4. ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("Ключевые выводы исследования:")
    
    print("\n✓ PNG оптимален для простых изображений")
    print("  - Коэффициент сжатия: 1.09 - 8.41")
    print("  - Без потерь качества")
    print("  - Поддержка прозрачности")
    
    print("\n✓ JPEG эффективен для фотографий")
    print("  - Коэффициент сжатия: 0.49 - 13.23")
    print("  - Настраиваемое качество")
    print("  - Неэффективен для простой графики")
    
    print("\n✓ WebP показывает лучшие результаты")
    print("  - Коэффициент сжатия: до 16.85")
    print("  - Современный формат")
    print("  - Хорошая поддержка браузерами")
    
    print("\n✓ Hex-анализ критичен для оптимизации")
    print("  - Понимание структуры чанков")
    print("  - Возможность ручной оптимизации")
    print("  - Диагностика проблем с файлами")
    
    print_header("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("Все файлы созданы в папке 'test_images/'")
    print("Результаты анализа сохранены в JSON файлах")
    print("\nДля подробного изучения запустите отдельные скрипты:")
    print("- python create_test_images.py")
    print("- python hex_analyzer.py") 
    print("- python compression_analyzer.py")

if __name__ == "__main__":
    main()