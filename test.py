from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from f

def create_invoice_pdf(customer_name, room_number, total_amount):
    pdf_file = "hotel_invoice.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    pdfmetrics.registerFont(TTFont('DejaVuSerif','DejaVuSerif.ttf', 'UTF-8'))
    # Используем шрифт DejaVuSansCondensed
    c.setFont("DejaVu", 12)

    c.drawString(100, 750, "Счет на оплату за проживание в гостинице")
    c.drawString(100, 730, "-----------------------------------------")

    c.drawString(100, 700, f"Клиент: {customer_name}")
    c.drawString(100, 680, f"Номер комнаты: {room_number}")

    c.drawString(100, 650, f"Сумма к оплате: {total_amount} руб.")

    c.showPage()
    c.save()

    print(f"PDF-счет успешно создан: {pdf_file}")

# Пример использования функции
customer_name = "Иванов Иван"
room_number = "101"
total_amount = 2500
create_invoice_pdf(customer_name, room_number, total_amount)
