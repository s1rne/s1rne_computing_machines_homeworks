#!/usr/bin/env python3
"""
Генератор тестовых изображений для анализа кодирования
Создает различные типы изображений для изучения структуры файлов
"""

from PIL import Image, ImageDraw
import os
import struct

def create_minimal_png():
    """Создание минимального PNG файла (черный пиксель 1x1)"""
    img = Image.new('RGB', (1, 1), (0, 0, 0))
    img.save('test_minimal_black.png', 'PNG', optimize=True)
    return 'test_minimal_black.png'

def create_gradient_image():
    """Создание градиентного изображения 10x10"""
    img = Image.new('RGB', (10, 10))
    for x in range(10):
        for y in range(10):
            # Создаем градиент от черного к белому
            intensity = int(255 * (x + y) / 18)
            img.putpixel((x, y), (intensity, intensity, intensity))
    
    img.save('test_gradient_10x10.png', 'PNG', optimize=True)
    img.save('test_gradient_10x10.jpg', 'JPEG', quality=95)
    img.save('test_gradient_10x10.bmp', 'BMP')
    return ['test_gradient_10x10.png', 'test_gradient_10x10.jpg', 'test_gradient_10x10.bmp']

def create_colorful_image():
    """Создание цветного изображения 50x50 с узором"""
    img = Image.new('RGB', (50, 50))
    for x in range(50):
        for y in range(50):
            # Создаем цветной узор
            r = (x * 5) % 256
            g = (y * 5) % 256
            b = ((x + y) * 3) % 256
            img.putpixel((x, y), (r, g, b))
    
    img.save('test_colorful_50x50.png', 'PNG', optimize=True)
    img.save('test_colorful_50x50.jpg', 'JPEG', quality=85)
    img.save('test_colorful_50x50.bmp', 'BMP')
    return ['test_colorful_50x50.png', 'test_colorful_50x50.jpg', 'test_colorful_50x50.bmp']

def create_geometric_pattern():
    """Создание геометрического узора для анализа сжатия"""
    img = Image.new('RGB', (100, 100), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Рисуем геометрические фигуры
    for i in range(0, 100, 10):
        color = (i, 255-i, 128)
        draw.rectangle([i, i, i+8, i+8], fill=color)
        draw.ellipse([i+1, i+1, i+7, i+7], outline=(0, 0, 0))
    
    img.save('test_geometric_100x100.png', 'PNG', optimize=True)
    img.save('test_geometric_100x100.jpg', 'JPEG', quality=90)
    img.save('test_geometric_100x100.bmp', 'BMP')
    return ['test_geometric_100x100.png', 'test_geometric_100x100.jpg', 'test_geometric_100x100.bmp']

def analyze_file_size(filename):
    """Анализ размера файла"""
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        return size
    return 0

def print_file_analysis(filenames):
    """Вывод анализа размеров файлов"""
    print("\n=== АНАЛИЗ РАЗМЕРОВ ФАЙЛОВ ===")
    print(f"{'Файл':<30} {'Размер (байт)':<15} {'Формат':<10}")
    print("-" * 55)
    
    total_size = 0
    for filename in filenames:
        if os.path.exists(filename):
            size = analyze_file_size(filename)
            format_type = filename.split('.')[-1].upper()
            print(f"{filename:<30} {size:<15} {format_type:<10}")
            total_size += size
    
    print("-" * 55)
    print(f"{'ИТОГО:':<30} {total_size:<15}")

def create_all_test_images():
    """Создание всех тестовых изображений"""
    print("Создание тестовых изображений для анализа кодирования...")
    
    # Создаем папку для результатов
    os.makedirs('test_images', exist_ok=True)
    os.chdir('test_images')
    
    all_files = []
    
    # Минимальное изображение
    print("1. Создание минимального черного пикселя...")
    minimal_file = create_minimal_png()
    all_files.append(minimal_file)
    
    # Градиентное изображение
    print("2. Создание градиентного изображения...")
    gradient_files = create_gradient_image()
    all_files.extend(gradient_files)
    
    # Цветное изображение
    print("3. Создание цветного изображения...")
    color_files = create_colorful_image()
    all_files.extend(color_files)
    
    # Геометрический узор
    print("4. Создание геометрического узора...")
    geometric_files = create_geometric_pattern()
    all_files.extend(geometric_files)
    
    # Анализ размеров
    print_file_analysis(all_files)
    
    print(f"\nСоздано {len(all_files)} тестовых файлов в папке 'test_images/'")
    return all_files

if __name__ == "__main__":
    create_all_test_images()