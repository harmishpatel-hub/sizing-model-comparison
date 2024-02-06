from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self) -> None:
        # logo = f'./Logo/En'
        logo = f"src/component/Logo/Entegra-Logo.png"
        self.image(logo, x=10, y=5, w=45, h=21)
        self.ln(15)
        return super().header()
    
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0,10, f'Page {self.page_no()}', 0, 0, 'C')
        return super().footer()
    
    def set_title(self, title: str) -> None:
        self.set_font('Arial', 'B', 14)
        # self.set_fill_color(109, 159, 245)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'C', 1)
        self.ln(2)
        return super().set_title(title)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(255, 255, 255)
        self.cell(0, 6, label, 0, 1, 'C', 1)
        self.ln(2)
    
    def write_content(self, txt, title):
        # self.add_page()
        self.chapter_title(title)
        self.set_font('Arial', '', 11)
        self.write(5, txt)
    
    def image_content(self, path, title):
        self.add_page()
        self.chapter_title(title)
        self.image(path, x=5, y=50, w=200, h=150)

    def stats_write(self, key_string, _list):
        stat_string = _list[key_string]
        # _list.pop(key_string)
        self.write_content(stat_string, key_string)


def downloadPDF(report, subheader, string):
    pdfOutput = PDF('P', 'mm', 'A4')
    pdfOutput.alias_nb_pages()
    temp_path = 'plots/'
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    pdfOutput.add_page()
    pdfOutput.set_title(subheader)

    # for chart in report:
    #     report[chart].write_image(f'{temp_path}{chart}.png')
    #     pdfOutput.image_content(f'{temp_path}{chart}.png', chart)

    return pdfOutput