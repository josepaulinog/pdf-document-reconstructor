import json
import pandas as pd
import html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

class DocumentProcessor:
    def __init__(self, json_file, csv_file):
        self.json_data = self._load_json(json_file)
        self.layout_data = self._load_csv(csv_file)
        self.page_width, self.page_height = A4
        self.margin = inch
        self.line_height = 14  # altura de línea en puntos
        
    def _load_json(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def _load_csv(self, csv_file):
        df = pd.read_csv(csv_file, skipinitialspace=True)
        df.columns = df.columns.str.strip("'")
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip("'")
        return df

    def _clean_text(self, text):
        """Limpia y decodifica el texto"""
        if pd.isna(text) or text is None:
            return ""
        
        # Convertir a string y limpiar espacios
        text = str(text).strip()
        
        # Decodificar entidades HTML
        text = html.unescape(text)
        
        # Remover caracteres problemáticos
        text = text.replace('*', '')
        
        return text

    def _get_page_text_blocks(self, page_number):
        text_blocks = []
        for block in self.json_data.get('Blocks', []):
            if block.get('Page') == page_number and block.get('BlockType') == 'LINE':
                text = self._clean_text(block.get('Text', ''))
                if text:
                    # Obtener geometría del bloque
                    geometry = block.get('Geometry', {}).get('BoundingBox', {})
                    text_blocks.append({
                        'text': text,
                        'top': geometry.get('Top', 0),
                        'left': geometry.get('Left', 0)
                    })
        
        # Ordenar por posición vertical
        return sorted(text_blocks, key=lambda x: x['top'])

    def generate_pdf(self, output_file):
        c = canvas.Canvas(output_file, pagesize=A4)
        
        total_pages = self.json_data.get('DocumentMetadata', {}).get('Pages', 0)
        print(f"Procesando {total_pages} páginas...")
        
        for page_num in range(1, total_pages + 1):
            # Configurar fuente
            c.setFont("Helvetica", 12)
            
            # Obtener bloques de texto para esta página
            text_blocks = self._get_page_text_blocks(page_num)
            
            for block in text_blocks:
                text = block['text']
                
                # Calcular posición Y (invertida porque PDF usa coordenadas desde abajo)
                y = self.page_height - (block['top'] * self.page_height) - self.margin
                
                # Calcular posición X
                x = self.margin + (block['left'] * (self.page_width - 2*self.margin))
                
                # Dibujar texto
                try:
                    c.drawString(x, y, text)
                except Exception as e:
                    print(f"Error al procesar texto en página {page_num}: {text[:50]}...")
                    continue
            
            if page_num % 10 == 0:
                print(f"Procesada página {page_num}")
            
            c.showPage()
        
        c.save()
        print("PDF generado con éxito")

    def process_document(self, output_pdf):
        try:
            print("Iniciando procesamiento del documento...")
            self.generate_pdf(output_pdf)
            print(f"PDF generado: {output_pdf}")
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    processor = DocumentProcessor('analyzeDocResponse.json', 'layout.csv')
    processor.process_document('libro_completo.pdf')
