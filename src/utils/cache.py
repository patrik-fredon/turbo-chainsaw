"""
Icon caching system for Fredon Menu
"""

import os
import hashlib
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Tuple, Any
from PIL import Image, ImageOps
import gi

gi.require_version('GdkPixbuf', '2.0')
from gi.repository import GdkPixbuf

from menu.models import IconCache, IconFormat

logger = logging.getLogger(__name__)


class IconCacheManager:
    """Manages loading and caching of icon files."""

    def __init__(self, cache_dir: Optional[str] = None, max_size_mb: int = 50):
        """
        Initialize icon cache manager.

        Args:
            cache_dir: Directory for cache storage. If None, uses default.
            max_size_mb: Maximum cache size in megabytes.
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/fredon-menu")

        self.cache_dir = Path(cache_dir)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.memory_cache: Dict[str, IconCache] = {}
        self.access_times: Dict[str, float] = {}

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load existing cache index
        self._load_cache_index()

    def _load_cache_index(self):
        """Load cache index from disk."""
        index_file = self.cache_dir / "cache_index.json"
        try:
            if index_file.exists():
                import json
                with open(index_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct IconCache objects
                    for key, value in data.items():
                        format_type = IconFormat(value['format'])
                        self.memory_cache[key] = IconCache(
                            data=bytes.fromhex(value['data']),
                            format=format_type,
                            size=tuple(value['size']),
                            last_modified=value['last_modified']
                        )
                        self.access_times[key] = value.get('access_time', time.time())
                logger.info(f"Loaded {len(self.memory_cache)} cached icons")
        except Exception as e:
            logger.error(f"Error loading cache index: {e}")
            self.memory_cache.clear()
            self.access_times.clear()

    def _save_cache_index(self):
        """Save cache index to disk."""
        index_file = self.cache_dir / "cache_index.json"
        try:
            import json
            data = {}
            for key, cache in self.memory_cache.items():
                data[key] = {
                    'data': cache.data.hex(),
                    'format': cache.format.value,
                    'size': list(cache.size),
                    'last_modified': cache.last_modified,
                    'access_time': self.access_times.get(key, time.time())
                }
            with open(index_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Error saving cache index: {e}")

    def _get_cache_key(self, icon_path: str, size: Tuple[int, int]) -> str:
        """Generate cache key for icon."""
        path_hash = hashlib.md5(icon_path.encode()).hexdigest()
        size_str = f"{size[0]}x{size[1]}"
        return f"{path_hash}_{size_str}"

    def _get_file_mtime(self, file_path: str) -> float:
        """Get file modification time."""
        try:
            return os.path.getmtime(file_path)
        except OSError:
            return 0

    def _enforce_cache_size_limit(self):
        """Enforce cache size limit using LRU eviction."""
        total_size = sum(len(cache.data) for cache in self.memory_cache.values())

        if total_size <= self.max_size_bytes:
            return

        # Sort by access time (oldest first)
        sorted_items = sorted(
            self.access_times.items(),
            key=lambda x: x[1]
        )

        # Remove oldest items until under limit
        removed_count = 0
        for key, _ in sorted_items:
            if total_size <= self.max_size_bytes * 0.8:  # Leave 20% headroom
                break

            if key in self.memory_cache:
                total_size -= len(self.memory_cache[key].data)
                del self.memory_cache[key]
                del self.access_times[key]
                removed_count += 1

        if removed_count > 0:
            logger.info(f"Evicted {removed_count} old icons from cache")

    def load_icon(self, icon_path: str, size: Tuple[int, int] = (64, 64)) -> Optional[IconCache]:
        """
        Load icon with caching support.

        Args:
            icon_path: Path to icon file
            size: Desired size (width, height)

        Returns:
            IconCache or None if loading failed
        """
        if not icon_path:
            return None

        # Check if file exists
        if not os.path.exists(icon_path):
            logger.warning(f"Icon file not found: {icon_path}")
            return self._load_fallback_icon(size)

        cache_key = self._get_cache_key(icon_path, size)
        file_mtime = self._get_file_mtime(icon_path)

        # Check memory cache
        if cache_key in self.memory_cache:
            cache = self.memory_cache[cache_key]
            if cache.last_modified >= file_mtime:
                self.access_times[cache_key] = time.time()
                return cache
            else:
                # File was modified, remove from cache
                del self.memory_cache[cache_key]
                del self.access_times[cache_key]

        # Load and process icon
        try:
            # Determine format
            _, ext = os.path.splitext(icon_path)
            if ext.lower() == '.png':
                format_type = IconFormat.PNG
            elif ext.lower() == '.svg':
                format_type = IconFormat.SVG
            elif ext.lower() == '.ico':
                format_type = IconFormat.ICO
            else:
                format_type = IconFormat.FALLBACK

            # Load image
            if format_type == IconFormat.SVG:
                # Handle SVG (rasterize)
                cache = self._load_svg_icon(icon_path, size)
            else:
                # Handle raster images
                cache = self._load_raster_icon(icon_path, size, format_type)

            if cache:
                cache.last_modified = file_mtime
                self.memory_cache[cache_key] = cache
                self.access_times[cache_key] = time.time()

                # Enforce cache size limit
                self._enforce_cache_size_limit()

                return cache

        except Exception as e:
            logger.error(f"Error loading icon {icon_path}: {e}")

        # Return fallback icon on failure
        return self._load_fallback_icon(size)

    def _load_raster_icon(self, icon_path: str, size: Tuple[int, int],
                         format_type: IconFormat) -> Optional[IconCache]:
        """Load raster icon (PNG, ICO, etc.)."""
        try:
            with Image.open(icon_path) as img:
                # Convert to RGBA if necessary
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Resize with high quality
                img = ImageOps.contain(img, size, method=Image.Resampling.LANCZOS)

                # Convert to PNG bytes
                import io
                output = io.BytesIO()
                img.save(output, format='PNG')
                data = output.getvalue()

                return IconCache(
                    data=data,
                    format=IconFormat.PNG,
                    size=img.size,
                    last_modified=time.time()
                )
        except Exception as e:
            logger.error(f"Error loading raster icon {icon_path}: {e}")
            return None

    def _load_svg_icon(self, icon_path: str, size: Tuple[int, int]) -> Optional[IconCache]:
        """Load SVG icon and rasterize to desired size."""
        try:
            # Use GDK Pixbuf for SVG rendering
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                icon_path, size[0], size[1], True
            )

            # Convert to PNG bytes
            import io
            output = io.BytesIO()
            pixbuf.savev(output, 'png', [], [])
            data = output.getvalue()

            return IconCache(
                data=data,
                format=IconFormat.PNG,
                size=(pixbuf.get_width(), pixbuf.get_height()),
                last_modified=time.time()
            )
        except Exception as e:
            logger.error(f"Error loading SVG icon {icon_path}: {e}")
            return None

    def _load_fallback_icon(self, size: Tuple[int, int]) -> Optional[IconCache]:
        """Load fallback icon when requested icon cannot be loaded."""
        fallback_path = Path(__file__).parent.parent / "data" / "icons" / "fallback.png"

        if fallback_path.exists():
            return self._load_raster_icon(str(fallback_path), size, IconFormat.PNG)

        # Create a simple fallback icon programmatically
        try:
            img = Image.new('RGBA', size, (64, 64, 64, 200))
            # Add a simple border
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            draw.rectangle([2, 2, size[0]-3, size[1]-3], outline=(128, 128, 128, 255), width=2)

            import io
            output = io.BytesIO()
            img.save(output, format='PNG')
            data = output.getvalue()

            return IconCache(
                data=data,
                format=IconFormat.PNG,
                size=size,
                last_modified=time.time()
            )
        except Exception as e:
            logger.error(f"Error creating fallback icon: {e}")
            return None

    def get_gdk_pixbuf(self, icon_path: str, size: Tuple[int, int] = (64, 64)) -> Optional[GdkPixbuf.Pixbuf]:
        """
        Get GDK Pixbuf for icon (for GTK integration).

        Args:
            icon_path: Path to icon file
            size: Desired size (width, height)

        Returns:
            GdkPixbuf.Pixbuf or None if loading failed
        """
        cache = self.load_icon(icon_path, size)
        if cache:
            try:
                import io
                loader = GdkPixbuf.PixbufLoader()
                loader.write(cache.data)
                loader.close()
                return loader.get_pixbuf()
            except Exception as e:
                logger.error(f"Error creating GDK Pixbuf: {e}")
        return None

    def clear_cache(self):
        """Clear all cached icons."""
        self.memory_cache.clear()
        self.access_times.clear()
        try:
            # Remove cache directory
            import shutil
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Cleared icon cache")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_size = sum(len(cache.data) for cache in self.memory_cache.values())
        return {
            'cache_entries': len(self.memory_cache),
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'max_size_mb': self.max_size_bytes / (1024 * 1024),
            'cache_dir': str(self.cache_dir),
        }

    def save_cache(self):
        """Save cache index to disk."""
        self._save_cache_index()

    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            self.save_cache()
        except:
            pass  # Ignore errors during cleanup