"""
Supabase configuration stub - external services are now optional
This module is kept for backward compatibility but functionality is disabled
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()

# Supabase is now optional and disabled by default
SUPABASE_AVAILABLE = False


class SupabaseConfig:
    """Stub configuration handler - Supabase is now optional."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize stub configuration."""
        console.print("[yellow]⚠️  Supabase functionality is disabled in self-contained mode[/yellow]")
        raise ValueError("Supabase is not available in self-contained mode")


class SupabaseStorageHandler:
    """Stub storage handler - Supabase is now optional."""
    
    def __init__(self, config):
        """Initialize stub storage handler."""
        console.print("[yellow]⚠️  Supabase storage functionality is disabled in self-contained mode[/yellow]")
        raise ValueError("Supabase storage is not available in self-contained mode")
