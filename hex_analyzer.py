#!/usr/bin/env python3
"""
Hex-анализатор для изучения структуры изображений
Анализирует PNG, JPEG, BMP файлы на байтовом уровне
"""

import struct
import zlib
import os

class HexAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        self.file_size = 0
        
    def load_file(self):
        """Загрузка файла в память"""
        if not os.path.exists(self.filename):
            print(f"Файл {self.filename} не найден!")
            return False
            
        with open(self.filename, 'rb') as f:
            self.data = f.read()
            self.file_size = len(self.data)
            
        print(f"Загружен файл: {self.filename}")
        print(f"Размер файла: {self.file_size} байт")
        return True
    
    def print_hex_dump(self, start=0, length=64):
        """Вывод hex-дампа файла"""
        if not self.data:
            print("Файл не загружен!")
            return
            
        end = min(start + length, len(self.data))
        print(f"\n=== HEX-ДАМП ({start:04X}-{end:04X}) ===")
        
        for i in range(start, end, 16):
            # Адрес
            addr = f"{i:04X}: "
            
            # Hex данные
            hex_part = ""
            ascii_part = ""
            
            for j in range(16):
                if i + j < len(self.data):
                    byte = self.data[i + j]
                    hex_part += f"{byte:02X} "
                    if 32 <= byte <= 126:
                        ascii_part += chr(byte)
                    else:
                        ascii_part += "."
                else:
                    hex_part += "   "
                    ascii_part += " "
            
            print(f"{addr}{hex_part:<48} |{ascii_part}|")
    
    def analyze_png(self):
        """Анализ структуры PNG файла"""
        if not self.data or len(self.data) < 8:
            print("Недостаточно данных для анализа PNG")
            return
            
        print("\n=== АНАЛИЗ PNG СТРУКТУРЫ ===")
        
        # Проверка сигнатуры
        signature = self.data[:8]
        expected_sig = b'\x89PNG\r\n\x1a\n'
        
        if signature == expected_sig:
            print("✓ Сигнатура PNG корректна")
            print(f"  Сигнатура: {signature.hex().upper()}")
        else:
            print("✗ Неверная сигнатура PNG")
            return
        
        # Анализ чанков
        offset = 8
        chunk_count = 0
        
        while offset < len(self.data) - 12:
            if offset + 12 > len(self.data):
                break
                
            # Чтение заголовка чанка
            length = struct.unpack('>I', self.data[offset:offset+4])[0]
            chunk_type = self.data[offset+4:offset+8]
            chunk_data = self.data[offset+8:offset+8+length]
            crc = self.data[offset+8+length:offset+12+length]
            
            chunk_count += 1
            
            print(f"\nЧанк #{chunk_count}:")
            print(f"  Тип: {chunk_type.decode()}")
            print(f"  Длина: {length} байт")
            print(f"  CRC: {crc.hex().upper()}")
            
            # Анализ конкретных чанков
            if chunk_type == b'IHDR':
                self._analyze_ihdr_chunk(chunk_data)
            elif chunk_type == b'IDAT':
                self._analyze_idat_chunk(chunk_data)
            elif chunk_type == b'IEND':
                print("  Назначение: Маркер конца файла")
                break
            
            offset += 12 + length
    
    def _analyze_ihdr_chunk(self, data):
        """Анализ IHDR чанка"""
        if len(data) != 13:
            print("  ✗ Неверная длина IHDR чанка")
            return
            
        width = struct.unpack('>I', data[0:4])[0]
        height = struct.unpack('>I', data[4:8])[0]
        bit_depth = data[8]
        color_type = data[9]
        compression = data[10]
        filter_method = data[11]
        interlace = data[12]
        
        print("  Назначение: Заголовок изображения")
        print(f"  Размеры: {width}x{height} пикселей")
        print(f"  Глубина цвета: {bit_depth} бит")
        print(f"  Тип цвета: {color_type}")
        print(f"  Сжатие: {compression}")
        print(f"  Фильтрация: {filter_method}")
        print(f"  Чересстрочность: {interlace}")
    
    def _analyze_idat_chunk(self, data):
        """Анализ IDAT чанка"""
        print("  Назначение: Данные изображения")
        print(f"  Размер сжатых данных: {len(data)} байт")
        
        try:
            # Попытка распаковать данные
            decompressed = zlib.decompress(data)
            print(f"  Размер распакованных данных: {len(decompressed)} байт")
            print(f"  Коэффициент сжатия: {len(decompressed)/len(data):.2f}")
            
            # Анализ первых байтов
            if len(decompressed) > 0:
                print(f"  Первые байты: {decompressed[:16].hex().upper()}")
                
        except Exception as e:
            print(f"  Ошибка распаковки: {e}")
    
    def analyze_jpeg(self):
        """Анализ структуры JPEG файла"""
        if not self.data or len(self.data) < 4:
            print("Недостаточно данных для анализа JPEG")
            return
            
        print("\n=== АНАЛИЗ JPEG СТРУКТУРЫ ===")
        
        # Проверка сигнатуры
        if self.data[:2] == b'\xff\xd8':
            print("✓ Сигнатура JPEG корректна")
            print(f"  Сигнатура: {self.data[:2].hex().upper()}")
        else:
            print("✗ Неверная сигнатура JPEG")
            return
        
        # Поиск маркеров
        offset = 2
        marker_count = 0
        
        while offset < len(self.data) - 1:
            if self.data[offset] == 0xFF:
                marker = self.data[offset+1]
                marker_count += 1
                
                marker_name = self._get_jpeg_marker_name(marker)
                print(f"\nМаркер #{marker_count}: 0xFF{marker:02X} ({marker_name})")
                
                if marker == 0xD9:  # EOI
                    print("  Назначение: Конец изображения")
                    break
                elif marker == 0xDA:  # SOS
                    print("  Назначение: Начало сканирования")
                    break
                    
            offset += 1
    
    def _get_jpeg_marker_name(self, marker):
        """Получение названия JPEG маркера"""
        markers = {
            0xD8: "SOI (Start of Image)",
            0xD9: "EOI (End of Image)",
            0xDA: "SOS (Start of Scan)",
            0xDB: "DQT (Define Quantization Table)",
            0xC0: "SOF0 (Start of Frame)",
            0xC4: "DHT (Define Huffman Table)",
            0xE0: "APP0 (Application Data)",
        }
        return markers.get(marker, f"Unknown ({marker:02X})")
    
    def analyze_bmp(self):
        """Анализ структуры BMP файла"""
        if not self.data or len(self.data) < 14:
            print("Недостаточно данных для анализа BMP")
            return
            
        print("\n=== АНАЛИЗ BMP СТРУКТУРЫ ===")
        
        # Проверка сигнатуры
        if self.data[:2] == b'BM':
            print("✓ Сигнатура BMP корректна")
            print(f"  Сигнатура: {self.data[:2].hex().upper()}")
        else:
            print("✗ Неверная сигнатура BMP")
            return
        
        # Анализ заголовка файла
        file_size = struct.unpack('<I', self.data[2:6])[0]
        reserved1 = struct.unpack('<H', self.data[6:8])[0]
        reserved2 = struct.unpack('<H', self.data[8:10])[0]
        data_offset = struct.unpack('<I', self.data[10:14])[0]
        
        print(f"\nЗаголовок файла BMP:")
        print(f"  Размер файла: {file_size} байт")
        print(f"  Зарезервировано 1: {reserved1}")
        print(f"  Зарезервировано 2: {reserved2}")
        print(f"  Смещение данных: {data_offset} байт")
        
        # Анализ заголовка изображения
        if len(self.data) >= 26:
            header_size = struct.unpack('<I', self.data[14:18])[0]
            width = struct.unpack('<I', self.data[18:22])[0]
            height = struct.unpack('<I', self.data[22:26])[0]
            
            print(f"\nЗаголовок изображения BMP:")
            print(f"  Размер заголовка: {header_size} байт")
            print(f"  Ширина: {width} пикселей")
            print(f"  Высота: {height} пикселей")
    
    def analyze_file(self):
        """Основной метод анализа файла"""
        if not self.load_file():
            return
            
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ ФАЙЛА: {self.filename}")
        print(f"{'='*60}")
        
        # Определение типа файла и анализ
        if self.data[:8] == b'\x89PNG\r\n\x1a\n':
            self.analyze_png()
        elif self.data[:2] == b'\xff\xd8':
            self.analyze_jpeg()
        elif self.data[:2] == b'BM':
            self.analyze_bmp()
        else:
            print("Неизвестный формат файла")
        
        # Общий hex-дамп начала файла
        self.print_hex_dump(0, 128)

def main():
    """Главная функция для запуска анализа"""
    print("Hex-анализатор изображений")
    print("=" * 40)
    
    # Анализ файлов в папке test_images
    test_dir = "test_images"
    if os.path.exists(test_dir):
        files = [f for f in os.listdir(test_dir) if f.endswith(('.png', '.jpg', '.bmp'))]
        
        for filename in sorted(files)[:3]:  # Анализируем первые 3 файла
            filepath = os.path.join(test_dir, filename)
            analyzer = HexAnalyzer(filepath)
            analyzer.analyze_file()
            print("\n" + "="*80 + "\n")
    else:
        print("Папка test_images не найдена. Сначала запустите create_test_images.py")

if __name__ == "__main__":
    main()