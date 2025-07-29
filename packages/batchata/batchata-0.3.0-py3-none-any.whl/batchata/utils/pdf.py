"""
PDF Utilities Module

Provides utility functions for creating test PDFs.
"""

import re
from pathlib import Path
from typing import List


def create_pdf(pages: List[str]) -> bytes:
    """
    Create a PDF with the given pages.
    
    Args:
        pages: List of text content for each page
        
    Returns:
        PDF file as bytes
    """
    if not pages:
        raise ValueError("At least one page is required")
    
    num_pages = len(pages)
    
    # Build page objects
    page_objects = []
    content_objects = []
    
    for i, page_content in enumerate(pages):
        page_num = i + 3  # Pages start from object 3
        content_num = page_num + num_pages  # Content objects after page objects
        
        page_objects.append(f"{page_num} 0 obj")
        page_objects.append(f"<< /Type /Page /Parent 2 0 R /Resources {2 + num_pages + num_pages + 1} 0 R /MediaBox [0 0 612 792] /Contents {content_num} 0 R >>")
        page_objects.append("endobj")
        
        # Split content into lines and position each line separately
        lines = page_content.split('\n')
        line_commands = []
        for i, line in enumerate(lines):
            if i == 0:
                line_commands.append(f"72 720 Td")
            else:
                line_commands.append(f"0 -15 Td")  # Move down 15 points for each line
            line_commands.append(f"({line}) Tj")
        
        stream_content = f"""BT
/F1 12 Tf
{chr(10).join(line_commands)}
ET"""
        
        content_objects.append(f"{content_num} 0 obj")
        content_objects.append(f"<< /Length {len(stream_content)} >>")
        content_objects.append("stream")
        content_objects.append(stream_content)
        content_objects.append("endstream")
        content_objects.append("endobj")
    
    # Build page references for Pages object
    page_refs = " ".join([f"{i + 3} 0 R" for i in range(num_pages)])
    
    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [{page_refs}] /Count {num_pages} >>
endobj
{chr(10).join(page_objects)}
{2 + num_pages + num_pages + 1} 0 obj
<< /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >>
endobj
{chr(10).join(content_objects)}
xref
0 {2 + num_pages + num_pages + 2}
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n"""

    # Add xref entries (simplified)
    for i in range(num_pages + num_pages + 1):
        pdf_content += f"\n{1000 + i * 100:010d} 00000 n"
    
    pdf_content += f"""
trailer
<< /Size {2 + num_pages + num_pages + 2} /Root 1 0 R >>
startxref
{5000 + sum(len(p) for p in pages)}
%%EOF"""
    
    return pdf_content.encode('latin-1')


# --- regex helpers -----------------------------------------------------------
_PAGE_SPLIT    = re.compile(br'/Type\s*/Page\b')
_TEXT_PATTERN  = re.compile(br'(?:BT\b.*?ET)|(?:\([^)]+\)\s*T[Jj])', re.S)
_FONT_PATTERN  = re.compile(br'/Font\b')
_IMAGE_PATTERN = re.compile(br'/Subtype\s*/Image\b')

def is_textual_pdf(
    path: str | Path,
    text_page_thresh: float = 0.2,   # ≤20% blank pages ⇒ treat as textual
    font_ratio_thresh: float = 0.05  # ≥0.05 fonts per page ⇒ textual
) -> float:
    """
    Heuristic: classify a PDF as textual (machine‑readable) without external deps.
    
    Returns:
        float: textual score from 0.0 (no text) to 1.0 (fully textual)
               0.8+ is pretty textual, <0.1 shows warning, 0.0 raises error with citations
    
    Args:
        text_page_thresh: max fraction of pages allowed to lack text operators
        font_ratio_thresh: min avg '/Font' hits per page signalling embedded fonts
    """
    data = Path(path).read_bytes()

    pages = _PAGE_SPLIT.split(data)[1:]
    if not pages:
        return 0.0                     # can't detect pages → assume not textual

    textful_pages = sum(bool(_TEXT_PATTERN.search(p)) for p in pages)
    textless_ratio = 1 - textful_pages / len(pages)
    textual_ratio = 1 - textless_ratio

    font_hits   = len(_FONT_PATTERN.findall(data))
    font_ratio  = font_hits / max(len(pages), 1)

    # Calculate textual score
    # Base score from text content ratio
    score = textual_ratio
    
    # Boost score if fonts are embedded (indicates real text)
    if font_ratio >= font_ratio_thresh:
        score = min(1.0, score + 0.2)
    
    return score