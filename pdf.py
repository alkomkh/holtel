from pathlib import Path
from borb.pdf import Document
from borb.pdf import Page as PDFPage
from borb.pdf import PDF
from borb.pdf import Paragraph
from borb.pdf import SingleColumnLayout
from borb.io.read.types import Decimal
from borb.pdf import Table, TableCell
from borb.pdf import Barcode, BarcodeType
from borb.pdf import X11Color
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
from borb.pdf import FlexibleColumnWidthTable
# from borb.pdf import FixedColumnWidthTable
from borb.pdf import Page
from borb.pdf.page.page_size import PageSize

import datetime
import webbrowser


def get_pdf(cols: list, rows: list, end_line: str = "", horizontal: bool = False):
    document = Document()
    # page = PDFPage()
    if horizontal:
        page = Page(
            width=PageSize.A4_LANDSCAPE.value[0], height=PageSize.A4_LANDSCAPE.value[1]
        )
    else:
        page = Page()
    layout = SingleColumnLayout(page)
    font_path: Path = Path(__file__).parent / "DejaVuSerif.ttf"
    custom_font = TrueTypeFont.true_type_font_from_file(font_path)
    layout.add(Paragraph(f"Чек на оплату", font=custom_font))
    layout.add(Paragraph(f"Дата предьявления счета {datetime.datetime.now()}", font=custom_font))
    # layout.add(Paragraph(f"Тема отчета: {theme}", font=custom_font))

    table = FlexibleColumnWidthTable(number_of_rows=len(rows) + 1, number_of_columns=len(cols))

    for col in cols:
        table.add(TableCell(Paragraph(col, font_color=X11Color("White"), font=custom_font, font_size=Decimal(10)),
                            background_color=X11Color("SlateGray")))

    for row in rows:
        for cell in row:
            table.add(Paragraph(str(cell), font=custom_font, font_size=Decimal(10)))

    # table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
    layout.add(table)
    layout.add(Paragraph(end_line, font=custom_font))
    document.add_page(page)

    with open("temp_pdf.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, document)

    webbrowser.open("temp_pdf.pdf", new=0, autoraise=True)


if __name__ == "__main__":
    get_pdf("Тестовый отчет", ["1", "2", "3", "4"],
            rows=[("Русского текст аффф фффффф фффффф ффффффф ффф фффф фффф ффф", 12, 13, 14), (21, 22, 23, 24),
                  (31, 32, 33, 34)])