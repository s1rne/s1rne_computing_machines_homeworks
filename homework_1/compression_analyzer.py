#!/usr/bin/env python3
"""
Анализатор сжатия изображений
Сравнивает эффективность различных форматов и настроек сжатия
"""

import os
import json
from PIL import Image
import matplotlib.pyplot as plt

class CompressionAnalyzer:
    def __init__(self):
        self.results = []
        
    def analyze_image_compression(self, image_path, output_dir="compression_analysis"):
        """Анализ сжатия одного изображения в разных форматах"""
        if not os.path.exists(image_path):
            print(f"Файл {image_path} не найден!")
            return
            
        os.makedirs(output_dir, exist_ok=True)
        
        # Загружаем исходное изображение
        img = Image.open(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        print(f"\nАнализ изображения: {base_name}")
        print(f"Исходный размер: {img.size[0]}x{img.size[1]} пикселей")
        
        analysis = {
            'filename': base_name,
            'original_size': img.size,
            'formats': {}
        }
        
        # PNG с разными настройками
        png_files = self._create_png_variants(img, base_name, output_dir)
        analysis['formats']['PNG'] = png_files
        
        # JPEG с разными уровнями качества
        jpeg_files = self._create_jpeg_variants(img, base_name, output_dir)
        analysis['formats']['JPEG'] = jpeg_files
        
        # BMP (без сжатия)
        bmp_file = self._create_bmp_variant(img, base_name, output_dir)
        analysis['formats']['BMP'] = bmp_file
        
        # WebP (современный формат)
        webp_files = self._create_webp_variants(img, base_name, output_dir)
        analysis['formats']['WebP'] = webp_files
        
        self.results.append(analysis)
        self._print_analysis_summary(analysis)
        
        return analysis
    
    def _create_png_variants(self, img, base_name, output_dir):
        """Создание PNG файлов с разными настройками"""
        variants = {}
        
        # PNG без оптимизации
        filename = os.path.join(output_dir, f"{base_name}_png_standard.png")
        img.save(filename, 'PNG')
        variants['standard'] = {
            'filename': filename,
            'size': os.path.getsize(filename),
            'description': 'Стандартный PNG'
        }
        
        # PNG с оптимизацией
        filename = os.path.join(output_dir, f"{base_name}_png_optimized.png")
        img.save(filename, 'PNG', optimize=True)
        variants['optimized'] = {
            'filename': filename,
            'size': os.path.getsize(filename),
            'description': 'Оптимизированный PNG'
        }
        
        # PNG с палитрой (для изображений с ограниченным количеством цветов)
        if img.mode in ['RGB', 'RGBA']:
            filename = os.path.join(output_dir, f"{base_name}_png_palette.png")
            # Конвертируем в палитровый режим
            palette_img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
            palette_img.save(filename, 'PNG', optimize=True)
            variants['palette'] = {
                'filename': filename,
                'size': os.path.getsize(filename),
                'description': 'PNG с палитрой'
            }
        
        return variants
    
    def _create_jpeg_variants(self, img, base_name, output_dir):
        """Создание JPEG файлов с разными уровнями качества"""
        variants = {}
        
        quality_levels = [100, 95, 85, 75, 50, 25]
        
        for quality in quality_levels:
            filename = os.path.join(output_dir, f"{base_name}_jpeg_q{quality}.jpg")
            img.save(filename, 'JPEG', quality=quality, optimize=True)
            variants[f'q{quality}'] = {
                'filename': filename,
                'size': os.path.getsize(filename),
                'description': f'JPEG качество {quality}%'
            }
        
        return variants
    
    def _create_bmp_variant(self, img, base_name, output_dir):
        """Создание BMP файла"""
        filename = os.path.join(output_dir, f"{base_name}_bmp.bmp")
        img.save(filename, 'BMP')
        
        return {
            'filename': filename,
            'size': os.path.getsize(filename),
            'description': 'BMP без сжатия'
        }
    
    def _create_webp_variants(self, img, base_name, output_dir):
        """Создание WebP файлов с разными настройками"""
        variants = {}
        
        try:
            # WebP без потерь
            filename = os.path.join(output_dir, f"{base_name}_webp_lossless.webp")
            img.save(filename, 'WebP', lossless=True)
            variants['lossless'] = {
                'filename': filename,
                'size': os.path.getsize(filename),
                'description': 'WebP без потерь'
            }
            
            # WebP с потерями
            filename = os.path.join(output_dir, f"{base_name}_webp_lossy.webp")
            img.save(filename, 'WebP', quality=80)
            variants['lossy'] = {
                'filename': filename,
                'size': os.path.getsize(filename),
                'description': 'WebP с потерями (80%)'
            }
            
        except Exception as e:
            print(f"Ошибка создания WebP: {e}")
            variants = {}
        
        return variants
    
    def _print_analysis_summary(self, analysis):
        """Вывод сводки анализа"""
        print(f"\n{'='*60}")
        print(f"РЕЗУЛЬТАТЫ АНАЛИЗА: {analysis['filename']}")
        print(f"{'='*60}")
        
        # Собираем все варианты в один список для сортировки
        all_variants = []
        
        for format_name, variants in analysis['formats'].items():
            if isinstance(variants, dict):
                for variant_name, variant_data in variants.items():
                    all_variants.append((format_name, variant_name, variant_data))
            else:
                all_variants.append((format_name, 'single', variants))
        
        # Сортируем по размеру файла
        all_variants.sort(key=lambda x: x[2]['size'])
        
        print(f"{'Формат':<12} {'Вариант':<15} {'Размер (байт)':<15} {'Описание'}")
        print("-" * 70)
        
        smallest_size = all_variants[0][2]['size']
        
        for format_name, variant_name, data in all_variants:
            size = data['size']
            compression_ratio = (size / smallest_size) if smallest_size > 0 else 1
            print(f"{format_name:<12} {variant_name:<15} {size:<15} {data['description']}")
            print(f"{'':12} {'':15} {'':15} (коэфф. сжатия: {compression_ratio:.2f})")
        
        # Находим лучшие варианты
        best_compression = all_variants[0]
        best_quality = None
        
        # Ищем лучшее качество среди JPEG
        jpeg_variants = [v for v in all_variants if v[0] == 'JPEG']
        if jpeg_variants:
            best_quality = jpeg_variants[0]
        
        print(f"\nЛучшее сжатие: {best_compression[0]} ({best_compression[2]['size']} байт)")
        if best_quality:
            print(f"Лучшее качество JPEG: {best_quality[1]} ({best_quality[2]['size']} байт)")
    
    def analyze_directory(self, directory="test_images"):
        """Анализ всех изображений в директории"""
        if not os.path.exists(directory):
            print(f"Директория {directory} не найдена!")
            return
        
        image_files = [f for f in os.listdir(directory) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        if not image_files:
            print(f"В директории {directory} не найдено изображений!")
            return
        
        print(f"Найдено {len(image_files)} изображений для анализа")
        
        for image_file in image_files:
            image_path = os.path.join(directory, image_file)
            self.analyze_image_compression(image_path)
        
        # Создание итогового отчета
        self.create_summary_report()
    
    def create_summary_report(self):
        """Создание итогового отчета"""
        if not self.results:
            return
        
        print(f"\n{'='*80}")
        print("ИТОГОВЫЙ ОТЧЕТ ПО АНАЛИЗУ СЖАТИЯ")
        print(f"{'='*80}")
        
        # Статистика по форматам
        format_stats = {}
        
        for result in self.results:
            for format_name, variants in result['formats'].items():
                if format_name not in format_stats:
                    format_stats[format_name] = {'total_size': 0, 'count': 0}
                
                if isinstance(variants, dict):
                    for variant_data in variants.values():
                        format_stats[format_name]['total_size'] += variant_data['size']
                        format_stats[format_name]['count'] += 1
                else:
                    format_stats[format_name]['total_size'] += variants['size']
                    format_stats[format_name]['count'] += 1
        
        print(f"\nСТАТИСТИКА ПО ФОРМАТАМ:")
        print(f"{'Формат':<12} {'Средний размер':<15} {'Количество':<12}")
        print("-" * 40)
        
        for format_name, stats in format_stats.items():
            avg_size = stats['total_size'] / stats['count']
            print(f"{format_name:<12} {avg_size:<15.0f} {stats['count']:<12}")
        
        # Сохранение результатов в JSON
        with open('compression_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\nДетальные результаты сохранены в: compression_analysis_results.json")

def main():
    """Главная функция"""
    print("Анализатор сжатия изображений")
    print("=" * 40)
    
    analyzer = CompressionAnalyzer()
    
    # Анализируем все изображения в папке test_images
    analyzer.analyze_directory("test_images")

if __name__ == "__main__":
    main()
