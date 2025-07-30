from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class OptimizationConfig:
    type: str
    defaultPricingMode: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

@dataclass
class OptimizationResult:
    type: str
    performed: bool
    estimatedSavings: float
    context: Dict[str, Any]

@dataclass
class OptimizationResponse:
    optimizedJob: Dict[str, Any]
    optimizationResults: List[OptimizationResult]
    estimatedSavings: float
    optimizationPerformed: bool 