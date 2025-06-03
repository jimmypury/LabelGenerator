from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from .logger import logger

class LabelDocument:
    """
    Label document class for creating and managing PDF label documents
    """
    
    def __init__(self, pagesize=A4):
        """
        Initialize label document
        
        Args:
            pagesize: Page size, default is A4
        """
        self.pages = []
        self.pagesize = pagesize
        # ReportLab uses points as units, 1 point = 1/72 inch, approx 0.35mm
        width_mm = round(self.pagesize[0] * 25.4 / 72, 1)
        height_mm = round(self.pagesize[1] * 25.4 / 72, 1)
        logger.info(f"Created new label document, size: {width_mm} mm × {height_mm} mm")
        
    def add_page(self, page):
        """
        Add page to document
        
        Args:
            page: LabelPage object
        """
        self.pages.append(page)
        logger.debug(f"Page added to document, current page count: {len(self.pages)}")
        
    def export_pdf(self, filename):
        """
        Export document as PDF file
        
        Args:
            filename: Output PDF filename
        """
        logger.info(f"Starting PDF export: {filename}")
        
        try:
            # Ensure directory exists
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                logger.debug(f"Creating directory: {directory}")
                os.makedirs(directory)
                
            # Create PDF canvas
            c = canvas.Canvas(filename, pagesize=self.pagesize)
            
            # Process each page
            for i, page in enumerate(self.pages):
                logger.debug(f"Processing page {i+1}...")
                # Set page size
                c.setPageSize((page.width, page.height))
                
                # Draw page background
                if page.background_color:
                    logger.debug(f"Drawing page background, color: {page.background_color}")
                    c.setFillColorRGB(*[x/255 for x in page.background_color])
                    c.rect(0, 0, page.width, page.height, fill=1, stroke=0)
                
                # Draw all elements on the page
                for j, element in enumerate(page.elements):
                    logger.debug(f"Drawing element {j+1} on page {i+1}")
                    # Save current graphics state
                    c.saveState()
                    
                    # Coordinate conversion - convert from top-left to ReportLab's bottom-left
                    # If element uses top-left coordinate system, we only need to convert y coordinate
                    y_position = page.height - element.y
                    
                    # Temporarily save original coordinates
                    original_x, original_y = element.x, element.y
                    
                    # Set converted coordinates
                    element.y = y_position
                    
                    try:
                        # Draw element
                        element.draw(c)
                    except Exception as e:
                        logger.error(f"Failed to draw element: {e}")
                    
                    # Restore original coordinates (for potential reuse of element)
                    element.x, element.y = original_x, original_y
                    
                    # Restore graphics state
                    c.restoreState()
                
                # End current page, start new page
                c.showPage()
            
            # Save PDF
            c.save()
            logger.info(f"PDF exported successfully: {filename}")
            return filename
        except Exception as e:
            logger.exception(f"PDF export failed: {e}")
            raise