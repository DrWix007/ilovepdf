# fileName : plugins/dm/callBack/file_process/zoomPDF.py
# copyright ©️ 2021 nabilanavab

file_name = "plugins/dm/callBack/file_process/zoomPDF.py"
__author_name__ = "Nabil A Navab: @nabilanavab"

# LOGGING INFO: DEBUG
from logger import logger

import fitz

async def zoomPDF(input_file: str, cDIR: str) -> ( bool, str ):
    try:
        output_path = f"{cDIR}/outPut.pdf"
        with fitz.open(input_file) as iNPUT:
            with fitz.open() as oUTPUT:        # empty output PDF
                for pages in iNPUT:
                    r  = pages.rect
                    d =  fitz.Rect(pages.cropbox_position, pages.cropbox_position)
                    r1 = r / 2 # top left rect
                    r2 = r1 + (r1.width, 0, r1.width, 0) # top right rect
                    r3 = r1 + (0, r1.height, 0, r1.height) # bottom left rect
                    r4 = fitz.Rect(r1.br, r.br) # bottom right rect
                    rect_list = [r1, r2, r3, r4] # put them in a list
                    
                    for rx in rect_list: # run thru rect list
                        rx += d # add the CropBox displacement
                        page = oUTPUT.new_page(-1, width = rx.width, height = rx.height)
                        page.show_pdf_page(page.rect, iNPUT, pages.number, clip = rx)
                oUTPUT.save(output_path, garbage = 3, deflate = True)
        return True, output_path
    
    except Exception as Error:
        logger.exception("🐞 %s: %s" %(file_name, Error), exc_info = True)
        return False, Error

# Author: @nabilanavab