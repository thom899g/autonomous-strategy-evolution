"""
Configuration and constants for the Autonomous Strategy Evolution system.
Centralized configuration to ensure consistency across all modules.
"""
import os
from typing import Dict, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class StrategyConfig:
    """Configuration for strategy generation and evaluation."""
    # RL Hyperparameters
    GAMMA: float = 0.99  # Discount factor
    LEARNING_RATE: float = 0.001
    MEMORY_SIZE: int = 10000
    BATCH_SIZE: int = 64
    TAU: float = 0.005  # Target network update rate
    
    # Strategy parameters
    INITIAL_CAPITAL: float = 10000.0
    MAX_POSITION_SIZE: float = 0.1  # 10% of capital per trade
    STOP_LOSS_PCT: float = 0.02  # 2% stop loss
    TAKE_PROFIT_PCT: float = 0.05  # 5% take profit
    
    # Evaluation metrics weights
    METRIC_WEIGHTS: Dict[str, float] = field(default_factory=lambda: {
        'sharpe_ratio': 0.3,
        'max_drawdown': -0.2,  # Negative weight (minimize)
        'win_rate': 0.25,
        'profit_factor': 0.25
    })

@dataclass
class FirebaseConfig:
    """Firebase configuration for state management."""
    # Firebase project ID (to be set from environment)
    PROJECT_ID: str = os.getenv('FIREBASE_PROJECT_ID', 'autonomous-trading-system')
    CREDENTIALS_PATH: str = os.getenv('FIREBASE_CREDENTIALS', './credentials/firebase-key.json')
    
    # Collection names
    COLLECTIONS: Dict[str, str] = field(default_factory=lambda: {
        'strategies': 'evolving_strategies',
        'performance': 'strategy_performance',
        'market_data': 'market_data_cache',
        'rl_agent': 'rl_agent_state'
    })

@dataclass
class DataConfig:
    """Data fetching and processing configuration."""
    DATA_SOURCES: list = field(default_factory=lambda: ['binance', 'kraken', 'coinbase'])
    TIME_FRAMES: list = field(default_factory=lambda: ['1h', '4h', '1d'])
    LOOKBACK_PERIOD: int = 100  # Candles to look back
    FEATURES: list = field(default_factory=lambda: [
        'open', 'high', 'low', 'close', 'volume',
        'rsi', 'macd', 'bb_upper', 'bb_lower', 'atr'
    ])

# Global configuration instance
STRATEGY_CONFIG = StrategyConfig()
FIREBASE_CONFIG = FirebaseConfig()
DATA_CONFIG = DataConfig()

# Logging configuration
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'INFO'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': f'logs/trading_system_{datetime.now().strftime("%Y%m%d")}.log',
            'formatter': 'detailed',
            'level': 'DEBUG'
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO'
    }
}