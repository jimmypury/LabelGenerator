from .logger import logger

class LabelPage:
    """
    Label page class for creating and managing PDF pages
    """

    
    def __init__(self, width=210, height=297):
        """
        Initialize label page
        
        Args:
            width: Page width (mm)
            height: Page height (mm)
        """
        mm_to_point = 72 / 25.4
        self.width = width*mm_to_point
        self.height = height*mm_to_point
        self.elements = []
        self.background_color = None
        if width and height:
            logger.info(f"Created new label page, size: {width * 0.3528:.2f} mm × {height * 0.3528:.2f} mm")
        else:
            logger.info("Created new label page, with default size")
        
        
    def set_background_color(self, color):
        """
        Set page background color
        
        Args:
            color: Color, can be RGB tuple (r,g,b) or hex string '#RRGGBB'
        """
        if isinstance(color, str) and color.startswith('#'):
            # Convert hex color to RGB tuple
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            self.background_color = (r, g, b)
        else:
            self.background_color = color
        logger.debug(f"Page background color set: {self.background_color}")
        return self
    
    def set_size(self, width, height):
        """
        Set page size
        
        Args:
            width: Page width (mm)
            height: Page height (mm)
        """
        mm_to_point = 72 / 25.4

        self.width = width*mm_to_point
        self.height = height*mm_to_point
        logger.debug(f"Page size set: {width}x{height}")
        return self
    
    def add_element(self, element):
        """
        Add element to page
        
        Args:
            element: Page element object
        """
        self.elements.append(element)
        logger.debug(f"Element added to page, current element count: {len(self.elements)}")