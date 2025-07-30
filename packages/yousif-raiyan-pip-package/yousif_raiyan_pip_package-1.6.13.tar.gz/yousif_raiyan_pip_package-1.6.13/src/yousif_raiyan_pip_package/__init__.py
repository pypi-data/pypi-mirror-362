__version__ = "1.6.13"

from .eeg_graph_representation import EEGGraphProcessor
from .edf_loader import EDFLoader
from .trigger_detector import TriggerDetector
from .analyzer import Analyzer

__all__ = ["EEGGraphProcessor",
           "EDFLoader",
           "TriggerDetector",
           "Analyzer"]