from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import platform
import glob
from .logger import logger

class FontManager:
    """Font manager for finding and registering system fonts"""
    
    _instance = None
    
    # Font name mapping for common fonts and their file names
    COMMON_FONT_MAPPING = {
        # Microsoft fonts
        "microsoft yahei": {"regular": "msyh.ttc", "bold": "msyhbd.ttc"},
        "microsoftyahei": {"regular": "msyh.ttc", "bold": "msyhbd.ttc"},
        "msyh": {"regular": "msyh.ttc", "bold": "msyhbd.ttc"},
        
        # Consolas
        "consolas": {"regular": "consola.ttf", "bold": "consolab.ttf", 
                    "italic": "consolai.ttf", "bolditalic": "consolaz.ttf"},
        
        # Arial
        "arial": {"regular": "arial.ttf", "bold": "arialbd.ttf", 
                 "italic": "ariali.ttf", "bolditalic": "arialbi.ttf"},
        
        # Times New Roman
        "times new roman": {"regular": "times.ttf", "bold": "timesbd.ttf",
                          "italic": "timesi.ttf", "bolditalic": "timesbi.ttf"},
        "timesnewroman": {"regular": "times.ttf", "bold": "timesbd.ttf",
                        "italic": "timesi.ttf", "bolditalic": "timesbi.ttf"},
        
        # Courier New
        "courier new": {"regular": "cour.ttf", "bold": "courbd.ttf",
                      "italic": "couri.ttf", "bolditalic": "courbi.ttf"},
        "couriernew": {"regular": "cour.ttf", "bold": "courbd.ttf",
                     "italic": "couri.ttf", "bolditalic": "courbi.ttf"},
        
        # SimSun and SimHei (Chinese fonts)
        "simsun": {"regular": "simsun.ttc"},
        "simhei": {"regular": "simhei.ttf"},
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.fonts = {}
        self.fonts_by_family = {}
        self.system_font_dirs = self._get_system_font_dirs()
        self.custom_font_dirs = []
        
        # Basic font directory to start with
        logger.info(f"System font directories: {self.system_font_dirs}")
        
        # Initiate font scanning
        self._scan_fonts()
        
        # Log the number of fonts found
        logger.info(f"Font scanning complete. Found {len(self.fonts)} fonts.")
    
    def _get_system_font_dirs(self):
        """Get default font directories for the current operating system"""
        font_dirs = []
        
        if platform.system() == "Windows":
            windows_dir = os.environ.get('WINDIR', 'C:/Windows')
            font_dirs.append(os.path.join(windows_dir, 'Fonts'))
            # Add Office font directory if exists
            program_files = os.environ.get('PROGRAMFILES', 'C:/Program Files')
            office_font_dir = os.path.join(program_files, 'Microsoft Office', 'Root', 'Fonts')
            if os.path.exists(office_font_dir):
                font_dirs.append(office_font_dir)
        
        elif platform.system() == "Darwin":  # macOS
            font_dirs.extend([
                '/System/Library/Fonts',
                '/Library/Fonts',
                os.path.expanduser('~/Library/Fonts')
            ])
        
        elif platform.system() == "Linux":
            font_dirs.extend([
                '/usr/share/fonts',
                '/usr/local/share/fonts',
                os.path.expanduser('~/.fonts')
            ])
        
        return [d for d in font_dirs if os.path.exists(d)]
    
    def add_font_directory(self, directory):
        """Add custom font directory"""
        if os.path.exists(directory) and directory not in self.custom_font_dirs:
            self.custom_font_dirs.append(directory)
            self._scan_directory(directory)
            logger.info(f"Added font directory: {directory}")
    
    def _scan_fonts(self):
        """Scan all system and custom font directories"""
        for directory in self.system_font_dirs + self.custom_font_dirs:
            self._scan_directory(directory)
    
    def _scan_directory(self, directory):
        """Scan specified directory for font files"""
        # Supported font extensions
        font_extensions = ['*.ttf', '*.ttc', '*.otf']
        
        try:
            for ext in font_extensions:
                pattern = os.path.join(directory, '**', ext)
                # Add recursive=True to properly scan subdirectories
                for font_path in glob.glob(pattern, recursive=True):
                    self._register_font_path(font_path)
                    
            # Log how many fonts found in this directory
            directory_fonts = [f for f in self.fonts.values() if f['path'].startswith(directory)]
            logger.debug(f"Found {len(directory_fonts)} fonts in {directory}")
        except Exception as e:
            logger.warning(f"Error scanning directory {directory}: {e}")
    
    def _register_font_path(self, font_path):
        """Record font file path information"""
        try:
            # Get basic font name from filename
            font_name = os.path.splitext(os.path.basename(font_path))[0]
            
            # Normalize font name
            normalized_name = font_name.lower().replace(' ', '')
            
            # Record font information
            if normalized_name not in self.fonts:
                self.fonts[normalized_name] = {
                    'path': font_path,
                    'name': font_name,
                    'registered': False
                }
                
                # Group fonts by family
                # Remove style suffixes to get family name
                family_name = font_name
                for suffix in ['bold', 'italic', 'oblique', 'regular', 'light', 'medium', 'black']:
                    family_name = family_name.lower().replace(suffix, '').strip()
                
                if family_name not in self.fonts_by_family:
                    self.fonts_by_family[family_name] = []
                    
                self.fonts_by_family[family_name].append(normalized_name)
                
        except Exception as e:
            logger.warning(f"Error processing font file {font_path}: {e}")
    
    def _find_font_in_windows_by_filename(self, font_name, style=None):
        """Find font by filename in Windows font directory"""
        if platform.system() != "Windows":
            return None
            
        # Normalize font name for lookup
        normalized_name = font_name.lower().replace(' ', '')
        
        # Check if we have a mapping for this font
        if normalized_name in self.COMMON_FONT_MAPPING:
            # Get the appropriate filename based on style
            style_key = "regular"
            if style:
                if style.lower() == "bold":
                    style_key = "bold"
                elif style.lower() == "italic":
                    style_key = "italic"
                elif style.lower() == "bold-italic":
                    style_key = "bolditalic"
            
            # Get filename from mapping
            if style_key in self.COMMON_FONT_MAPPING[normalized_name]:
                filename = self.COMMON_FONT_MAPPING[normalized_name][style_key]
                
                # Check all font directories
                for font_dir in self.system_font_dirs:
                    full_path = os.path.join(font_dir, filename)
                    if os.path.exists(full_path):
                        return full_path
        
        return None
    
    def get_font_path(self, font_name, font_style=None):
        """
        Get file path for the specified font
        
        Args:
            font_name: Font name
            font_style: Font style (normal, bold, italic, bold-italic)
            
        Returns:
            Found font path, or None if not found
        """
        # Normalize font name
        normalized_name = font_name.lower().replace(' ', '')
        
        # Log what we're looking for
        logger.debug(f"Searching for font: {font_name} ({font_style})")
        
        # 1. First try direct file match by common font mapping
        direct_match = self._find_font_in_windows_by_filename(font_name, font_style)
        if direct_match:
            logger.debug(f"Found direct file match: {direct_match}")
            return direct_match
        
        # 2. Try to match styled font name
        if font_style:
            styled_name = None
            if font_style.lower() == 'bold':
                styled_name = f"{normalized_name}bold"
            elif font_style.lower() == 'italic':
                styled_name = f"{normalized_name}italic"
            elif font_style.lower() == 'bold-italic':
                styled_name = f"{normalized_name}bolditalic"
                
            if styled_name and styled_name in self.fonts:
                logger.debug(f"Found styled font: {styled_name}")
                return self.fonts[styled_name]['path']
        
        # 3. Try to match basic font name
        if normalized_name in self.fonts:
            logger.debug(f"Found basic font: {normalized_name}")
            return self.fonts[normalized_name]['path']
        
        # 4. Fuzzy matching, check if font name is part of any font
        for name, info in self.fonts.items():
            if normalized_name in name:
                logger.debug(f"Found font by fuzzy match: {name}")
                return info['path']
        
        # 5. Try to find by font family
        family_name = normalized_name
        if family_name in self.fonts_by_family:
            # Prioritize style-matching font
            for font_key in self.fonts_by_family[family_name]:
                if font_style and font_style.lower() in font_key:
                    logger.debug(f"Found font in family with style: {font_key}")
                    return self.fonts[font_key]['path']
            
            # If no style match found, return first font in family
            if self.fonts_by_family[family_name]:
                first_font = self.fonts_by_family[family_name][0]
                logger.debug(f"Found first font in family: {first_font}")
                return self.fonts[first_font]['path']
        
        # If we get here, font wasn't found
        logger.warning(f"Font not found after all search methods: {font_name} ({font_style})")
        return None
    
    def register_font(self, font_name, font_style=None):
        """
        Register font in ReportLab
        
        Args:
            font_name: Font name
            font_style: Font style (normal, bold, italic, bold-italic)
            
        Returns:
            Registered font name on success, None on failure
        """
        # Get font path
        font_path = self.get_font_path(font_name, font_style)
        
        if not font_path:
            # Try to register standard Windows font directly
            if platform.system() == "Windows":
                logger.info(f"Attempting direct registration for {font_name}")
                try:
                    # For common Windows fonts, try registering directly
                    reg_name = font_name.replace(" ", "")
                    if font_style:
                        if font_style.lower() == 'bold':
                            reg_name = f"{reg_name}-Bold"
                        elif font_style.lower() == 'italic':
                            reg_name = f"{reg_name}-Italic"
                        elif font_style.lower() == 'bold-italic':
                            reg_name = f"{reg_name}-BoldItalic"
                    
                    # Check if already registered
                    if reg_name in pdfmetrics.getRegisteredFontNames():
                        logger.debug(f"Font already registered: {reg_name}")
                        return reg_name
                    
                    # Attempt to find the font file
                    font_path = self._find_font_in_windows_by_filename(font_name, font_style)
                    if font_path and os.path.exists(font_path):
                        pdfmetrics.registerFont(TTFont(reg_name, font_path))
                        logger.info(f"Directly registered font: {reg_name}, path: {font_path}")
                        return reg_name
                except Exception as e:
                    logger.warning(f"Direct registration failed for {font_name}: {e}")
            
            logger.warning(f"Font not found: {font_name} ({font_style})")
            return None
            
        try:
            # Build registration name
            reg_name = font_name.replace(" ", "")
            
            # Append style suffix if specified
            if font_style:
                if font_style.lower() == 'bold':
                    reg_name = f"{reg_name}-Bold"
                elif font_style.lower() == 'italic':
                    reg_name = f"{reg_name}-Italic"
                elif font_style.lower() == 'bold-italic':
                    reg_name = f"{reg_name}-BoldItalic"
            
            # Check if font is already registered
            if reg_name not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(reg_name, font_path))
                logger.debug(f"Successfully registered font: {reg_name}, path: {font_path}")
                
                # Update registration status
                normalized_name = font_name.lower().replace(' ', '')
                if normalized_name in self.fonts:
                    self.fonts[normalized_name]['registered'] = True
            
            return reg_name
            
        except Exception as e:
            logger.warning(f"Failed to register font {font_name}: {e}")
            return None
    
    def list_available_fonts(self):
        """Return a list of all available fonts"""
        return sorted(list(self.fonts.keys()))
    
    def list_registered_fonts(self):
        """Return a list of all registered fonts"""
        return sorted(pdfmetrics.getRegisteredFontNames())

# Create a global font manager instance for easy import and use
font_manager = FontManager()
