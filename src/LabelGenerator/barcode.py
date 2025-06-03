from reportlab.graphics.barcode import code39, code128, usps
from reportlab.graphics.barcode import eanbc, qr, ecc200datamatrix
from reportlab.lib.units import mm
from .logger import logger

class LabelBarcode:
    """
    Barcode element class for creating and managing barcodes in labels
    """
    
    class TEXT:
        """Barcode text position enumeration"""
        NONE = 0
        TOP = 1
        BOTTOM = 2
    
    def __init__(self):
        """Initialize barcode element"""
        self.x = 0
        self.y = 0
        self.width = 50 * mm
        self.height = 10 * mm
        self.data = "1234567890"
        self.barcode_type = "code128"
        self.color = (0, 0, 0)  # Default black
        self.show_text = False
        self.text_location = self.TEXT.BOTTOM
        self.text_color = (0, 0, 0)
        self.text_size = 8
        logger.info(f"Created new barcode element, type: {self.barcode_type}")
        
    def set_location(self, x, y):
        """
        Set barcode position
        
        Args:
            x: x coordinate (points)
            y: y coordinate (points)
        """
        self.x = x
        self.y = y
        logger.debug(f"Barcode position set: ({x}, {y})")
        
    def set_size(self, width, height):
        """
        Set barcode size
        
        Args:
            width: Width (points)
            height: Height (points)
        """
        self.width = width
        self.height = height
        logger.debug(f"Barcode size set: {width}x{height}")
        
    def set_data(self, data):
        """
        Set barcode data
        
        Args:
            data: Barcode data
        """
        self.data = data
        logger.debug(f"Barcode data set: {data}")
        
    def set_barcode_type(self, barcode_type):
        """
        Set barcode type
        
        Args:
            barcode_type: Barcode type (code39, code128, ean13, ean8, upca, usps, etc)
        """
        self.barcode_type = barcode_type
        logger.debug(f"Barcode type set: {barcode_type}")
        
    def set_color(self, color):
        """
        Set barcode color
        
        Args:
            color: Color, can be RGB tuple (r,g,b) or hex string '#RRGGBB'
        """
        if isinstance(color, str) and color.startswith('#'):
            # Convert hex color to RGB tuple
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.color = (r, g, b)
        else:
            self.color = color
        logger.debug(f"Barcode color set: {self.color}")
            
    def enable_text(self, show=True):
        """
        Enable barcode text
        
        Args:
            show: Whether to show text
        """
        self.show_text = show
        logger.debug(f"Barcode text display set: {show}")
        
    def set_text_location(self, location):
        """
        Set barcode text position
        
        Args:
            location: Text position (TEXT.NONE, TEXT.TOP, TEXT.BOTTOM)
        """
        self.text_location = location
        logger.debug(f"Barcode text position set: {location}")
        
    def set_text_color(self, color):
        """
        Set barcode text color
        
        Args:
            color: Color, can be RGB tuple (r,g,b) or hex string '#RRGGBB'
        """
        if isinstance(color, str) and color.startswith('#'):
            # Convert hex color to RGB tuple
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.text_color = (r, g, b)
        else:
            self.text_color = color
        logger.debug(f"Barcode text color set: {self.text_color}")
            
    def set_text_size(self, size):
        """
        Set barcode text size
        
        Args:
            size: Text size
        """
        self.text_size = size
        logger.debug(f"Barcode text size set: {size}")
        
    def draw(self, canvas):
        """
        Draw barcode on PDF canvas
        
        Args:
            canvas: reportlab Canvas object
        """
        logger.debug(f"Drawing barcode: '{self.data}', type: {self.barcode_type}, position: ({self.x}, {self.y})")
        try:
            # Save current graphics state
            canvas.saveState()
            
            # Create barcode
            if self.barcode_type.lower() == 'code39':
                barcode = code39.Standard39(self.data, barWidth=self.width/150, barHeight=self.height)
            elif self.barcode_type.lower() == 'code128':
                barcode = code128.Code128(self.data, barWidth=self.width/150, barHeight=self.height)
            elif self.barcode_type.lower() == 'ean13':
                barcode = eanbc.Ean13BarcodeWidget(self.data, barWidth=self.width/150, barHeight=self.height)
            elif self.barcode_type.lower() == 'ean8':
                barcode = eanbc.Ean8BarcodeWidget(self.data, barWidth=self.width/150, barHeight=self.height)
            elif self.barcode_type.lower() == 'upca':
                barcode = eanbc.Ean13BarcodeWidget("0" + self.data, barWidth=self.width/150, barHeight=self.height)
            elif self.barcode_type.lower() == 'datamatrix':
                barcode = ecc200datamatrix.ECC200DataMatrix(self.data)
            else:
                # Default to Code128
                logger.warning(f"Unknown barcode type: {self.barcode_type}, using default type code128")
                barcode = code128.Code128(self.data, barWidth=self.width/150, barHeight=self.height)
            
            # Set barcode color
            canvas.setFillColorRGB(*[x/255 for x in self.color])
            canvas.setStrokeColorRGB(*[x/255 for x in self.color])
            
            # Draw barcode - different types of barcodes have different drawing methods
            if isinstance(barcode, code128.Code128) or isinstance(barcode, code39.Standard39):
                # These types use direct drawing method
                barcode.drawOn(canvas, self.x, self.y)
            elif hasattr(barcode, 'draw'):
                try:
                    # For components with draw method
                    from reportlab.graphics import renderPDF
                    d = barcode.getBounds()
                    width = d[2] - d[0]
                    height = d[3] - d[1]
                    renderPDF.draw(barcode, canvas, self.x, self.y, self.width/width, self.height/height)
                except Exception as e:
                    # Fallback method
                    logger.error(f"Failed to draw barcode component: {e}, using text fallback")
                    canvas.drawString(self.x, self.y, f"BARCODE: {self.data}")
            else:
                # For barcode types that don't support direct drawing
                logger.warning(f"Barcode type not directly drawable: {self.barcode_type}, using text instead")
                try:
                    canvas.drawString(self.x, self.y, f"BARCODE: {self.data}")
                except Exception as e:
                    logger.error(f"Barcode text fallback also failed: {e}")
            
            # If text display is enabled
            if self.show_text:
                # Set text color
                canvas.setFillColorRGB(*[x/255 for x in self.text_color])
                canvas.setFont("Helvetica", self.text_size)
                
                # Draw text according to position
                text_width = canvas.stringWidth(self.data, "Helvetica", self.text_size)
                if self.text_location == self.TEXT.TOP:
                    canvas.drawCentredString(self.x + self.width/2, self.y + self.height + 2, self.data)
                elif self.text_location == self.TEXT.BOTTOM:
                    canvas.drawCentredString(self.x + self.width/2, self.y - self.text_size - 2, self.data)
                logger.debug(f"Drew barcode text: '{self.data}'")
            
            # Restore graphics state
            canvas.restoreState()
        except Exception as e:
            logger.error(f"Error drawing barcode: {e}")
            raise
