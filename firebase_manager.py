"""
Firebase state management for the trading system.
Handles all database operations, state persistence, and real-time updates.
"""
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.document import DocumentReference

from config import FIREBASE_CONFIG

# Initialize logger
logger = logging.getLogger(__name__)

class FirebaseManager:
    """Manages Firebase connections and operations for the trading system."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Firebase connection.
        
        Args:
            config: Firebase configuration dictionary
        
        Raises:
            FileNotFoundError: If Firebase credentials file doesn't exist
            ValueError: If Firebase initialization fails
        """
        self.config = config or FIREBASE_CONFIG
        self._db: Optional[FirestoreClient] = None
        self._initialized = False