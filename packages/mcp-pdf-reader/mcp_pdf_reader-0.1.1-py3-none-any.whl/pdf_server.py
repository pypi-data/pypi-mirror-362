import os, json, base64, fitz, logging
from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mcp-pdf-server')

mcp = FastMCP("PDF Reader", version="1.0.0", description="MCP server for PDF reading")

pdf_resources = {}
pdf_cache = {}


@mcp.tool()
def read_pdf_text(file_path: str, start_page: int = 1, end_page: Optional[int] = None) -> str:
    """
    Output PDF text content per page in markdown format.
    Args:
        file_path: Path to the PDF file
        start_page: Start page (1-based)
        end_page: End page (inclusive)
    Returns:
        Markdown formatted string
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    doc = fitz.open(file_path)
    total_pages = len(doc)

    if start_page < 1:
        start_page = 1
    if end_page is None or end_page > total_pages:
        end_page = total_pages
    if start_page > end_page:
        start_page, end_page = end_page, start_page

    markdown = ""
    for page_num in range(start_page - 1, end_page):
        page = doc[page_num]
        page_text = page.get_text().strip()
        markdown += f"---------- page {page_num + 1} ----------\n"
        markdown += page_text + "\n"
    markdown += f"---------- total {end_page - start_page + 1} ----------\n"

    doc.close()
    return markdown


@mcp.tool()
def read_by_ocr(file_path: str, start_page: int = 1, end_page: Optional[int] = None,
        language: str = "eng", dpi: int = 300) -> Dict[str, Any]:
    """
    Read text from PDF file using OCR.
    Args:
        file_path: Path to the PDF file
        start_page: Start page (1-based)
        end_page: End page (inclusive)
        language: OCR language code
        dpi: OCR DPI
    Returns:
        Dict with extracted text, page_count, extracted_pages
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    doc = fitz.open(file_path)
    total_pages = len(doc)

    if start_page < 1:
        start_page = 1
    if end_page is None or end_page > total_pages:
        end_page = total_pages
    if start_page > end_page:
        start_page, end_page = end_page, start_page

    text_content = ""
    for page_num in range(start_page - 1, end_page):
        page = doc[page_num]
        try:
            textpage = page.get_textpage_ocr(flags=3, language=language, dpi=dpi, full=True)
            page_text = page.get_text(textpage=textpage)
        except Exception as e:
            logger.warning(f"OCR failed on page {page_num + 1}, fallback to normal text: {e}")
            page_text = page.get_text()

        text_content += page_text + "\n\n"

    doc.close()

    return {"text": text_content, "page_count": total_pages,
        "extracted_pages": list(range(start_page, end_page + 1))}


@mcp.tool()
def read_pdf_images(file_path: str, page_number: int=1) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract images from a specific page in PDF.
    Args:
        file_path: Path to the PDF file
        page_number: Page number (1-based)
    Returns:
        Dict with list of images (base64 format)
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    doc = fitz.open(file_path)
    total_pages = len(doc)

    if page_number < 1 or page_number > total_pages:
        raise ValueError(f"Page number {page_number} out of range (1-{total_pages})")

    page = doc[page_number - 1]
    image_list = page.get_images(full=True)

    images = []
    for idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_data = base_image["image"]
        image_ext = base_image["ext"]
        image_b64 = base64.b64encode(image_data).decode('utf-8')

        images.append({"image_id": f"p{page_number}_img{idx}", "width": base_image["width"],
            "height": base_image["height"], "format": image_ext, "image_b64": image_b64})

    doc.close()

    return {"images": images}


if __name__ == "__main__":
    # 读取环境变量 PDF_DIR，如果没有则用默认路径
    PDF_DIR = os.environ.get("PDF_DIR")
    if os.path.exists(PDF_DIR):
        os.chdir(PDF_DIR)
    logger.info("Starting MCP PDF Server...")
    logger.info(f"Current directory: {os.getcwd()}")
    mcp.run()
