"""
Data updater for Pokemon random battle data.
"""

import json
import logging
import requests
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import time

from .formats import FORMATS

logger = logging.getLogger(__name__)


class DataUpdater:
    """
    Handles updating Pokemon random battle data from GitHub.
    """
    
    def __init__(self, cache_dir: Path):
        """
        Initialize DataUpdater.
        
        Args:
            cache_dir: Directory to store cached data
        """
        self.cache_dir = cache_dir
        self.github_raw_base = "https://raw.githubusercontent.com/pkmn/randbats/main/data"
        self.github_api_base = "https://api.github.com/repos/pkmn/randbats/contents/data"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'localsets/0.1.0'
        })
    
    def _download_format_stats(self, format_name: str) -> bool:
        """Download stats data for a format from GitHub."""
        try:
            url = f"{self.github_raw_base}/stats/{format_name}_stats.json"
            response = self.session.get(url, timeout=30)
            if response.status_code == 404:
                # Not all formats have stats data
                logger.info(f"No stats data for {format_name}")
                return False
            response.raise_for_status()
            data = response.json()
            cache_file = self.cache_dir / f"{format_name}_stats.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to download stats for {format_name}: {e}")
            return False

    def update_formats(self, formats: List[str]) -> List[str]:
        """
        Update data for specified formats, including stats.
        """
        updated_formats = []
        for format_name in formats:
            if format_name not in FORMATS:
                logger.warning(f"Unknown format: {format_name}")
                continue
            try:
                updated = False
                if self._update_format(format_name):
                    updated = True
                # Always try to update stats (no metadata for stats)
                if self._download_format_stats(format_name):
                    updated = True
                if updated:
                    updated_formats.append(format_name)
                    logger.info(f"Updated {format_name} (sets and/or stats)")
                else:
                    logger.warning(f"No update needed for {format_name}")
            except Exception as e:
                logger.error(f"Failed to update {format_name}: {e}")
        return updated_formats
    
    def _update_format(self, format_name: str) -> bool:
        """
        Update a single format.
        
        Args:
            format_name: Format name to update
            
        Returns:
            True if updated, False if no update needed
        """
        # Get current metadata
        current_metadata = self._get_current_metadata(format_name)
        if current_metadata is None:
            logger.warning(f"No current metadata for {format_name}")
            return False
        
        # Get remote metadata
        remote_metadata = self._get_remote_metadata(format_name)
        if remote_metadata is None:
            logger.warning(f"Failed to get remote metadata for {format_name}")
            return False
        
        # Check if update is needed
        if self._is_update_needed(current_metadata, remote_metadata):
            # Download new data
            if self._download_format_data(format_name):
                # Save new metadata
                self._save_metadata(format_name, remote_metadata)
                return True
        
        return False
    
    def _get_current_metadata(self, format_name: str) -> Optional[Dict[str, Any]]:
        """Get current metadata for a format."""
        metadata_file = self.cache_dir / f"{format_name}_metadata.json"
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read metadata for {format_name}: {e}")
            return None
    
    def _get_remote_metadata(self, format_name: str) -> Optional[Dict[str, Any]]:
        """Get remote metadata for a format."""
        try:
            url = f"{self.github_api_base}/{format_name}.json"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get remote metadata for {format_name}: {e}")
            return None
    
    def _is_update_needed(self, current: Dict[str, Any], remote: Dict[str, Any]) -> bool:
        """Check if update is needed based on metadata."""
        # Compare SHA
        current_sha = current.get('sha')
        remote_sha = remote.get('sha')
        
        if current_sha != remote_sha:
            return True
        
        # Compare timestamps if available
        current_updated = current.get('updated_at')
        remote_updated = remote.get('updated_at')
        
        if current_updated and remote_updated:
            try:
                current_time = datetime.fromisoformat(current_updated.replace('Z', '+00:00'))
                remote_time = datetime.fromisoformat(remote_updated.replace('Z', '+00:00'))
                return remote_time > current_time
            except Exception:
                pass
        
        return False
    
    def _download_format_data(self, format_name: str) -> bool:
        """Download format data from GitHub."""
        try:
            url = f"{self.github_raw_base}/{format_name}.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Validate JSON
            data = response.json()
            
            # Save to cache
            cache_file = self.cache_dir / f"{format_name}.json"
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to download data for {format_name}: {e}")
            return False
    
    def _save_metadata(self, format_name: str, metadata: Dict[str, Any]):
        """Save metadata for a format."""
        try:
            metadata_file = self.cache_dir / f"{format_name}_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metadata for {format_name}: {e}")
    
    def force_update(self, formats: List[str]) -> List[str]:
        """
        Force update of formats and stats regardless of metadata.
        
        Args:
            formats: List of format names to update
            
        Returns:
            List of successfully updated formats
        """
        updated_formats = []
        
        for format_name in formats:
            if format_name not in FORMATS:
                continue
            
            try:
                updated = False
                if self._download_format_data(format_name):
                    # Get and save metadata
                    metadata = self._get_remote_metadata(format_name)
                    if metadata:
                        self._save_metadata(format_name, metadata)
                    updated = True
                if self._download_format_stats(format_name):
                    updated = True
                if updated:
                    updated_formats.append(format_name)
                    logger.info(f"Force updated {format_name} (sets and/or stats)")
                    
            except Exception as e:
                logger.error(f"Failed to force update {format_name}: {e}")
        
        return updated_formats
    
    def get_update_status(self, format_name: str) -> Dict[str, Any]:
        """
        Get update status for a format.
        
        Args:
            format_name: Format name
            
        Returns:
            Dictionary with update status information
        """
        status = {
            'format': format_name,
            'has_local_data': False,
            'has_remote_data': False,
            'needs_update': False,
            'last_update': None,
            'local_sha': None,
            'remote_sha': None
        }
        
        # Check local data
        cache_file = self.cache_dir / f"{format_name}.json"
        metadata_file = self.cache_dir / f"{format_name}_metadata.json"
        
        if cache_file.exists() and metadata_file.exists():
            status['has_local_data'] = True
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    status['local_sha'] = metadata.get('sha')
                    status['last_update'] = metadata.get('updated_at')
            except Exception:
                pass
        
        # Check remote data
        try:
            remote_metadata = self._get_remote_metadata(format_name)
            if remote_metadata:
                status['has_remote_data'] = True
                status['remote_sha'] = remote_metadata.get('sha')
                
                # Check if update is needed
                if status['has_local_data']:
                    current_metadata = self._get_current_metadata(format_name)
                    if current_metadata:
                        status['needs_update'] = self._is_update_needed(
                            current_metadata, remote_metadata
                        )
        except Exception:
            pass
        
        return status
    
    def get_stats_file(self, format_name: str) -> Path:
        """Get the path to the cached stats file for a format."""
        return self.cache_dir / f"{format_name}_stats.json"

    def get_stats_data(self, format_name: str) -> Optional[Dict[str, Any]]:
        """Load stats data for a format from cache."""
        stats_file = self.get_stats_file(format_name)
        if not stats_file.exists():
            return None
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read stats for {format_name}: {e}")
            return None
    
    def cleanup_old_data(self, keep_formats: Optional[List[str]] = None):
        """
        Clean up old data files.
        
        Args:
            keep_formats: List of formats to keep (if None, keeps all)
        """
        if keep_formats is None:
            keep_formats = FORMATS
        
        for file_path in self.cache_dir.glob("*.json"):
            format_name = file_path.stem
            if format_name.endswith('_metadata'):
                format_name = format_name[:-9]  # Remove _metadata suffix
            
            if format_name not in keep_formats:
                try:
                    file_path.unlink()
                    logger.info(f"Cleaned up {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to clean up {file_path.name}: {e}") 

__all__ = ['DataUpdater'] 