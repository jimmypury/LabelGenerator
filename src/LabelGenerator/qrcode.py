import qrcode
from PIL import Image
from io import BytesIO
from enum import Enum
import reportlab.lib.colors as colors
from reportlab.lib.units import mm
from .logger import logger

class LabelQRCode:
    """
    QR code label element class for generating and placing QR codes on labels
    """
    
    class ERROR_LEVEL(Enum):
        """QR code error correction level enumeration"""
        LOW = qrcode.constants.ERROR_CORRECT_L      # Approx 7% error correction capability
        MEDIUM = qrcode.constants.ERROR_CORRECT_M   # Approx 15% error correction capability
        QUARTILE = qrcode.constants.ERROR_CORRECT_Q # Approx 25% error correction capability
        HIGH = qrcode.constants.ERROR_CORRECT_H     # Approx 30% error correction capability
    
    def __init__(self):
        """Initialize QR code label element"""
        self.x = 0
        self.y = 0
        self.width = 20 * mm
        self.height = 20 * mm
        self.data = ""
        self.color = (0, 0, 0)  # Default black
        self.error_correction = self.ERROR_LEVEL.MEDIUM  # Default medium error correction level
        self._qr_image = None
        self._last_data = None
        logger.info("Created new QR code element, ")
    
    def set_location(self, x, y):
        """
        Set QR code position on label
        
        :param x: X coordinate (points)
        :param y: Y coordinate (points)
        :return: self, for method chaining
        """
        self.x = x
        self.y = y
        logger.debug(f"QR code position set: ({x}, {y})")
        return self
    
    def set_size(self, width, height):
        """
        Set QR code size
        
        :param width: Width (points)
        :param height: Height (points)
        :return: self, for method chaining
        """
        self.width = width
        self.height = height
        logger.debug(f"QR code size set: {width}x{height}")
        return self
    
    def set_data(self, data):
        """
        Set QR code data
        
        :param data: Data to encode in QR code
        :return: self, for method chaining
        """
        self.data = data
        self._last_data = None  # Reset cache, force QR code regeneration
        logger.debug(f"QR code data set: {data}")
        return self
    
    def set_color(self, color):
        """
        Set QR code color
        
        :param color: RGB color tuple, e.g. (0, 0, 0) for black
        :return: self, for method chaining
        """
        self.color = color
        logger.debug(f"QR code color set: {color}")
        return self
    
    def set_error_correction(self, level):
        """
        Set QR code error correction level
        
        :param level: Error correction level, use value from ERROR_LEVEL enumeration
        :return: self, for method chaining
        """
        self.error_correction = level
        logger.debug(f"QR code error correction level set: {level}")
        return self
    
    def _generate_qr_code(self):
        """
        Generate QR code image based on settings
        
        :return: PIL Image object
        """
        logger.debug(f"Generating QR code image, data: '{self.data}'")
        try:
            qr = qrcode.QRCode(
                version=None,  # Auto-determine version
                error_correction=self.error_correction.value,
                box_size=10,   # Pixels per box (will be adjusted when drawing)
                border=0,      # Border width set to 0, we'll manage position ourselves
            )
            qr.add_data(self.data)
            qr.make(fit=True)
            
            # Create a black and white QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # If custom color needed, convert colors
            if self.color != (0, 0, 0):
                logger.debug(f"Custom QR code color: {self.color}")
                # Convert B&W image to RGB
                img = img.convert("RGB")
                
                # Get pixel data
                pixels = img.load()
                black_color = (0, 0, 0)
                width, height = img.size
                
                # Replace black pixels with specified color
                for i in range(width):
                    for j in range(height):
                        if pixels[i, j] == black_color:
                            pixels[i, j] = self.color
            
            self._qr_image = img
            self._last_data = self.data
            return img
        except Exception as e:
            logger.error(f"Failed to generate QR code image: {e}")
            raise
    
    def draw(self, canvas):
        """
        Draw QR code on the specified Canvas
        
        :param canvas: ReportLab Canvas object
        """
        logger.debug(f"Drawing QR code: '{self.data}', position: ({self.x}, {self.y})")
        try:
            # If data changed or QR code not yet generated, generate new one
            if not self._qr_image or self.data != self._last_data:
                self._generate_qr_code()
            
            # Convert PIL image to ReportLab format
            img_byte_arr = BytesIO()
            self._qr_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # drawImage x and y parameters are bottom-left coordinates
            # But our coordinates are top-left, so we need to convert
            draw_x = self.x
            draw_y = self.y - self.height
            
            # Draw image on canvas
            from reportlab.lib.utils import ImageReader
            img_reader = ImageReader(img_byte_arr)
            canvas.drawImage(img_reader, draw_x, draw_y, width=self.width, height=self.height)
            logger.debug("QR code drawn successfully")
        except Exception as e:
            logger.error(f"Error drawing QR code: {e}")
            raise
