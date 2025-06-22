"""
Fonts API Integration for CodeMaster Pro

Learning Notes:
- This module demonstrates Google Fonts API integration
- Shows font management and styling systems
- Implements font preview and download functionality
- Demonstrates UI enhancement through typography
"""

import requests
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import tempfile
from urllib.parse import urljoin
from utils.config import Config

class FontsAPI:
    """
    Google Fonts API integration for typography enhancement.
    
    This class provides:
    1. Google Fonts catalog browsing
    2. Font preview and download
    3. Font pairing suggestions
    4. Typography recommendations for coding
    5. Local font cache management
    """
    
    def __init__(self, config: Config):
        """Initialize fonts API with configuration."""
        
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # API configuration
        self.api_key = config.get_api_key('fonts')
        self.base_url = config.get('api_endpoints', {}).get('fonts',
                                 'https://www.googleapis.com/webfonts/v1')
        
        # Font cache directory
        self.cache_dir = Path.home() / '.codemaster_pro' / 'fonts'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Local font cache
        self.font_cache = {}
        self.load_cached_fonts()
        
        # Coding-friendly font categories
        self.coding_fonts = [
            'Fira Code', 'Source Code Pro', 'JetBrains Mono', 'Roboto Mono',
            'Ubuntu Mono', 'Inconsolata', 'PT Mono', 'Space Mono', 'IBM Plex Mono'
        ]
        
        print(f"🔤 Fonts API initialized - Cache: {self.cache_dir}")
    
    def get_font_families(self, sort: str = 'popularity') -> List[Dict[str, Any]]:
        """
        Get list of Google Fonts families.
        
        Learning Notes:
        - API pagination and data fetching
        - Font metadata processing
        - Caching strategies for large datasets
        """
        
        # Check if we have cached font data
        cache_file = self.cache_dir / 'font_families.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    if self._is_cache_valid(cached_data):
                        return cached_data['families']
            except Exception as e:
                self.logger.error(f"Error loading cached fonts: {e}")
        
        # Fetch from API if no valid cache
        if not self.api_key:
            return self._get_fallback_fonts()
        
        try:
            url = f"{self.base_url}/webfonts"
            params = {
                'key': self.api_key,
                'sort': sort
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            families = self._process_font_families(data.get('items', []))
            
            # Cache the results
            cache_data = {
                'families': families,
                'cached_at': self._get_current_timestamp(),
                'sort': sort
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            self.logger.info(f"Fetched {len(families)} font families")
            return families
            
        except Exception as e:
            self.logger.error(f"Fonts API request failed: {e}")
            return self._get_fallback_fonts()
    
    def get_coding_fonts(self) -> List[Dict[str, Any]]:
        """
        Get fonts specifically recommended for coding.
        
        Learning Notes:
        - Content filtering and categorization
        - Domain-specific recommendations
        - Font characteristic analysis
        """
        
        all_fonts = self.get_font_families()
        coding_fonts = []
        
        # Filter fonts suitable for coding
        for font in all_fonts:
            family_name = font.get('family', '')
            category = font.get('category', '')
            
            # Check if it's a known coding font
            if any(coding_font.lower() in family_name.lower() for coding_font in self.coding_fonts):
                font['recommended_for_coding'] = True
                coding_fonts.append(font)
            # Check if it's monospace
            elif category == 'monospace':
                font['recommended_for_coding'] = True
                coding_fonts.append(font)
            # Check for mono keyword in name
            elif 'mono' in family_name.lower() or 'code' in family_name.lower():
                font['recommended_for_coding'] = True
                coding_fonts.append(font)
        
        # Add coding-specific metadata
        for font in coding_fonts:
            font.update(self._get_coding_font_features(font['family']))
        
        return coding_fonts
    
    def get_font_details(self, family_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific font family.
        
        Learning Notes:
        - Detailed API data fetching
        - Font specification parsing
        - Typography metadata analysis
        """
        
        try:
            # Check cache first
            cache_key = f"details_{family_name.replace(' ', '_')}"
            if cache_key in self.font_cache:
                return self.font_cache[cache_key]
            
            # Find font in the families list
            families = self.get_font_families()
            font_data = None
            
            for family in families:
                if family['family'].lower() == family_name.lower():
                    font_data = family
                    break
            
            if not font_data:
                return self._get_default_font_details(family_name)
            
            # Enhance with additional details
            details = {
                'family': font_data['family'],
                'category': font_data['category'],
                'variants': font_data.get('variants', []),
                'subsets': font_data.get('subsets', []),
                'version': font_data.get('version', ''),
                'last_modified': font_data.get('lastModified', ''),
                'popularity': families.index(font_data) + 1,
                'files': font_data.get('files', {}),
                'download_urls': self._get_download_urls(font_data),
                'preview_text': self._get_preview_text(font_data['category']),
                'characteristics': self._analyze_font_characteristics(font_data),
                'usage_recommendations': self._get_usage_recommendations(font_data)
            }
            
            # Cache the details
            self.font_cache[cache_key] = details
            
            return details
            
        except Exception as e:
            self.logger.error(f"Error getting font details for {family_name}: {e}")
            return self._get_default_font_details(family_name)
    
    def get_font_pairings(self, primary_font: str) -> List[Dict[str, Any]]:
        """
        Get font pairing suggestions for a primary font.
        
        Learning Notes:
        - Typography pairing algorithms
        - Design principles in code
        - Aesthetic recommendation systems
        """
        
        primary_details = self.get_font_details(primary_font)
        primary_category = primary_details.get('category', 'sans-serif')
        
        pairings = []
        all_fonts = self.get_font_families()
        
        # Pairing rules based on typography principles
        pairing_rules = {
            'serif': ['sans-serif', 'display'],
            'sans-serif': ['serif', 'monospace'],
            'monospace': ['sans-serif', 'serif'],
            'display': ['serif', 'sans-serif'],
            'handwriting': ['serif', 'sans-serif']
        }
        
        target_categories = pairing_rules.get(primary_category, ['sans-serif'])
        
        for font in all_fonts[:50]:  # Limit to top 50 fonts for performance
            if (font['category'] in target_categories and 
                font['family'] != primary_font):
                
                pairing = {
                    'secondary_font': font['family'],
                    'category': font['category'],
                    'contrast_level': self._calculate_contrast(primary_details, font),
                    'harmony_score': self._calculate_harmony(primary_details, font),
                    'use_case': self._suggest_use_case(primary_details, font)
                }
                pairings.append(pairing)
        
        # Sort by harmony score
        pairings.sort(key=lambda x: x['harmony_score'], reverse=True)
        
        return pairings[:10]  # Return top 10 pairings
    
    def generate_font_preview(self, font_family: str, text: str, size: int = 14) -> str:
        """
        Generate CSS for font preview.
        
        Learning Notes:
        - CSS generation in Python
        - Font loading and rendering
        - Dynamic styling creation
        """
        
        font_details = self.get_font_details(font_family)
        google_fonts_url = self._get_google_fonts_css_url(font_family)
        
        css = f"""
        @import url('{google_fonts_url}');
        
        .font-preview-{font_family.replace(' ', '-').lower()} {{
            font-family: '{font_family}', {font_details.get('category', 'sans-serif')};
            font-size: {size}px;
            line-height: 1.4;
            margin: 10px 0;
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            background: #f9f9f9;
        }}
        
        .font-preview-{font_family.replace(' ', '-').lower()}:hover {{
            background: #f0f0f0;
            border-color: #c0c0c0;
        }}
        """
        
        return css
    
    def get_system_fonts(self) -> List[Dict[str, Any]]:
        """
        Get list of commonly available system fonts.
        
        Learning Notes:
        - System font detection
        - Cross-platform font compatibility
        - Fallback font management
        """
        
        system_fonts = [
            {
                'family': 'Arial',
                'category': 'sans-serif',
                'system': True,
                'platforms': ['Windows', 'macOS', 'Linux'],
                'suitable_for_coding': False
            },
            {
                'family': 'Times New Roman',
                'category': 'serif',
                'system': True,
                'platforms': ['Windows', 'macOS'],
                'suitable_for_coding': False
            },
            {
                'family': 'Courier New',
                'category': 'monospace',
                'system': True,
                'platforms': ['Windows', 'macOS', 'Linux'],
                'suitable_for_coding': True
            },
            {
                'family': 'Helvetica',
                'category': 'sans-serif',
                'system': True,
                'platforms': ['macOS', 'Linux'],
                'suitable_for_coding': False
            },
            {
                'family': 'Monaco',
                'category': 'monospace',
                'system': True,
                'platforms': ['macOS'],
                'suitable_for_coding': True
            },
            {
                'family': 'Consolas',
                'category': 'monospace',
                'system': True,
                'platforms': ['Windows'],
                'suitable_for_coding': True
            },
            {
                'family': 'DejaVu Sans Mono',
                'category': 'monospace',
                'system': True,
                'platforms': ['Linux'],
                'suitable_for_coding': True
            }
        ]
        
        return system_fonts
    
    def _process_font_families(self, families_data: List[Dict]) -> List[Dict[str, Any]]:
        """Process and enhance font families data from API."""
        
        processed = []
        
        for family in families_data:
            processed_family = {
                'family': family.get('family', ''),
                'category': family.get('category', 'sans-serif'),
                'variants': family.get('variants', []),
                'subsets': family.get('subsets', []),
                'version': family.get('version', ''),
                'lastModified': family.get('lastModified', ''),
                'files': family.get('files', {}),
                'popularity_rank': len(processed) + 1,
                'suitable_for_ui': self._is_suitable_for_ui(family),
                'suitable_for_headings': self._is_suitable_for_headings(family),
                'suitable_for_body': self._is_suitable_for_body(family)
            }
            processed.append(processed_family)
        
        return processed
    
    def _get_coding_font_features(self, font_family: str) -> Dict[str, Any]:
        """Get coding-specific features for a font."""
        
        features = {
            'ligatures_support': False,
            'zero_distinction': False,
            'readability_score': 7,  # Default score out of 10
            'best_sizes': [10, 11, 12, 13, 14],
            'recommended_line_height': 1.4
        }
        
        # Known features for specific fonts
        font_lower = font_family.lower()
        
        if 'fira code' in font_lower:
            features.update({
                'ligatures_support': True,
                'zero_distinction': True,
                'readability_score': 9,
                'best_sizes': [10, 11, 12, 13, 14, 15, 16]
            })
        elif 'jetbrains mono' in font_lower:
            features.update({
                'ligatures_support': True,
                'zero_distinction': True,
                'readability_score': 9,
                'best_sizes': [10, 11, 12, 13, 14, 15]
            })
        elif 'source code pro' in font_lower:
            features.update({
                'zero_distinction': True,
                'readability_score': 8,
                'best_sizes': [10, 11, 12, 13, 14]
            })
        elif 'inconsolata' in font_lower:
            features.update({
                'readability_score': 8,
                'best_sizes': [11, 12, 13, 14, 15]
            })
        
        return features
    
    def _get_fallback_fonts(self) -> List[Dict[str, Any]]:
        """Return fallback font list when API is unavailable."""
        
        return [
            {
                'family': 'Arial',
                'category': 'sans-serif',
                'variants': ['regular'],
                'fallback': True
            },
            {
                'family': 'Times New Roman',
                'category': 'serif',
                'variants': ['regular'],
                'fallback': True
            },
            {
                'family': 'Courier New',
                'category': 'monospace',
                'variants': ['regular'],
                'fallback': True,
                'recommended_for_coding': True
            }
        ]
    
    def _is_cache_valid(self, cached_data: Dict) -> bool:
        """Check if cached font data is still valid."""
        
        try:
            from datetime import datetime, timedelta
            cached_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
            return datetime.now() - cached_time < timedelta(days=7)  # Cache for 7 days
        except:
            return False
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def load_cached_fonts(self) -> None:
        """Load cached font details from disk."""
        
        cache_file = self.cache_dir / 'font_details_cache.json'
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.font_cache = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading font cache: {e}")
                self.font_cache = {}
    
    def save_font_cache(self) -> None:
        """Save font details cache to disk."""
        
        cache_file = self.cache_dir / 'font_details_cache.json'
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.font_cache, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving font cache: {e}")
    
    def _get_google_fonts_css_url(self, font_family: str) -> str:
        """Generate Google Fonts CSS URL for a font family."""
        
        base_url = "https://fonts.googleapis.com/css2"
        family_param = font_family.replace(' ', '+')
        return f"{base_url}?family={family_param}:wght@400;700&display=swap"
    
    def _is_suitable_for_ui(self, font_data: Dict) -> bool:
        """Determine if font is suitable for UI elements."""
        return font_data.get('category') in ['sans-serif', 'display']
    
    def _is_suitable_for_headings(self, font_data: Dict) -> bool:
        """Determine if font is suitable for headings."""
        return font_data.get('category') in ['serif', 'sans-serif', 'display']
    
    def _is_suitable_for_body(self, font_data: Dict) -> bool:
        """Determine if font is suitable for body text."""
        return font_data.get('category') in ['serif', 'sans-serif'] 