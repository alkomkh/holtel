from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)

def create_custom_invoice_pdf(customer_name, room_number, total_amount):
    pdf_file = "custom_hotel_invoice.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))


    # Данные для таблицы
    data = [
        ["Наименование", "Единица измерения", "Количество", "Цена, RUB", "Сумма, RUB"],
        ["Проживание с 5 октября 2022 г. по 6 октября 2022 г.", "Гость сут.", "1", "1000,00", "1000,00"],
        ["Дополнительная услуга: Завтрак \"Шведский стол\"", "шт.", "1", "0,00", "0,00"],
    ]

    # Создаем таблицу
    table = Table(data, colWidths=[200, 100, 60, 80, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSerif'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Добавляем дополнительные строки (по образцу)
    styles = getSampleStyleSheet()
    yourStyle = ParagraphStyle('yourtitle',
                           fontName="DejaVuSerif",
                           fontSize=16,
                           parent=styles['Heading2'],
                           alignment=1,
                           spaceAfter=14)
    elements = [
        Paragraph("Имею в копилке: Одна тысяча рублей ОО копеек, в т.ч. НДС О рублей ОО копеек", yourStyle),
        table,
    ]

    # Собираем документ
    doc.build(elements)

    print(f"PDF-счет успешно создан: {pdf_file}")

# Пример использования функции
customer_name = "Иванов Иван"
room_number = "101"
total_amount = 1000
create_custom_invoice_pdf(customer_name, room_number, total_amount)
