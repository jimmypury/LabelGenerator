from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import platform
import glob
from .logger import logger
from .fonts import font_manager

class LabelText:
    """
    Text element class for creating and managing text in labels
    """
    
    def __init__(self):
        """
        Initialize text element
        """
        self.x = 0
        self.y = 0
        self.text = ""
        self.font_name = "Helvetica"
        self.font_size = 10
        self.font_style = None  # normal, bold, italic, bold-italic
        self.color = (0, 0, 0)  # Default black
        self.alignment = 'left'  # left, center, right
        logger.info("Created new text element")
        
    def set_location(self, x, y):
        """
        Set text position
        
        Args:
            x: x coordinate (points)
            y: y coordinate (points)
        """
        self.x = x
        self.y = y
        logger.debug(f"Text position set: ({x}, {y})")
        
    def set_text(self, text):
        """
        Set text content
        
        Args:
            text: Text content
        """
        self.text = text
        logger.debug(f"Text content set: {text}")
        
    def set_font(self, font_name, font_size, font_style=None):
        """
        Set text font
        
        Args:
            font_name: Font name
            font_size: Font size
            font_style: Font style (normal, bold, italic, bold-italic)
        """
        self.font_name = font_name
        self.font_size = font_size
        self.font_style = font_style
        logger.debug(f"Text font set: {font_name}, size: {font_size}, style: {font_style}")
        
        # Standard fonts don't need registration
        standard_fonts = [
            "Helvetica", "Courier", "Times-Roman", "Symbol", "ZapfDingbats"
        ]
        
        if font_name in standard_fonts:
            return
        
        # Use font manager to register font
        registered_name = font_manager.register_font(font_name, font_style)
        if registered_name:
            self.font_name = registered_name
        else:
            logger.warning(f"Unable to register font {font_name}, using default font")
            self.font_name = "Helvetica"
    
    def set_color(self, color):
        """
        Set text color
        
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
        logger.debug(f"Text color set: {self.color}")
    
    def set_alignment(self, alignment):
        """
        Set text alignment
        
        Args:
            alignment: Alignment (left, center, right)
        """
        self.alignment = alignment
        logger.debug(f"Text alignment set: {alignment}")
    
    def draw(self, canvas):
        """
        Draw text on PDF canvas
        
        Args:
            canvas: reportlab Canvas object
        """
        logger.debug(f"Drawing text: '{self.text}', position: ({self.x}, {self.y})")
        try:
            # Save current graphics state
            canvas.saveState()
            
            # Set text color
            canvas.setFillColorRGB(*[x/255 for x in self.color])
            
            # Set font
            font_name = self.font_name
            
            try:
                canvas.setFont(font_name, self.font_size)
            except Exception as e:
                # If setting font fails, try using basic font
                logger.warning(f"Failed to set font {font_name}: {e}, using basic font")
                # Try falling back to standard fonts
                for std_font in ["Helvetica", "Courier", "Times-Roman"]:
                    try:
                        canvas.setFont(std_font, self.font_size)
                        logger.debug(f"Successfully fell back to standard font: {std_font}")
                        break
                    except:
                        continue
            
            # Draw text according to alignment
            if self.alignment == 'left':
                canvas.drawString(self.x, self.y, self.text)
            elif self.alignment == 'center':
                canvas.drawCentredString(self.x, self.y, self.text)
            elif self.alignment == 'right':
                canvas.drawRightString(self.x, self.y, self.text)
            else:
                canvas.drawString(self.x, self.y, self.text)
            
            # Restore graphics state
            canvas.restoreState()
        except Exception as e:
            logger.error(f"Error drawing text: {e}")
            raise
    
    @classmethod
    def add_font_directory(cls, directory):
        """
        Add custom font directory
        
        Args:
            directory: Font directory path
        """
        font_manager.add_font_directory(directory)