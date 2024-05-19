import flet as ft
from borb.pdf import Document
from borb.pdf import Page as PDFPage
from borb.pdf import PDF
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.io.read.types import Decimal
from borb.pdf import Table, TableCell
from borb.pdf import Barcode, BarcodeType
from borb.pdf import X11Color


async def save_doc(page_: ft.Page):
    document = Document()
    page = PDFPage()
    layout = SingleColumnLayout(page)
    layout.add(Paragraph("Счет", font="Helvetica", font_size=Decimal(20)))
    table = Table(number_of_rows=2, number_of_columns=6)



# Layout


# Create and add heading

# Create and add barcode
# layout.add(Barcode(data="0123456789", type=BarcodeType.QR, width=Decimal(64), height=Decimal(64)))

# Create and add table


# Header row
table.add(TableCell(Paragraph("Item", font_color=X11Color("White")), background_color=X11Color("SlateGray")))
table.add(TableCell(Paragraph("Unit Price", font_color=X11Color("White")), background_color=X11Color("SlateGray")))
table.add(TableCell(Paragraph("Amount", font_color=X11Color("White")), background_color=X11Color("SlateGray")))
table.add(TableCell(Paragraph("Price", font_color=X11Color("White")), background_color=X11Color("SlateGray")))

    # Data rows
for n in [("Lorem", 4.99, 1), ("Ipsum", 9.99, 2), ("Dolor", 1.99, 3), ("Sit", 1.99, 1)]:
    table.add(Paragraph(n[0]))
    table.add(Paragraph(str(n[1])))
    table.add(Paragraph(str(n[2])))
    table.add(Paragraph(str(n[1] * n[2])))

# Set padding
table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
layout.add(table)

# Append page
document.append_page(page)

# Persist PDF to file
with open("output4.pdf", "wb") as pdf_file_handle:
    PDF.dumps(pdf_file_handle, document)