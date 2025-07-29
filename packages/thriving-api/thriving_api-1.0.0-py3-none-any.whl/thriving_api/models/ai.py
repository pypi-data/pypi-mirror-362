"""
AI analysis models for the Thriving API SDK.

This module contains Pydantic models for AI-powered analysis endpoints.
"""

from typing import Optional, Union, Literal
from pydantic import BaseModel, Field, validator

from .base import BaseResponse, SymbolMixin, TimestampMixin, MetadataMixin


class AIAnalysis(BaseModel, SymbolMixin, TimestampMixin):
    """AI analysis data model."""
    
    action: Literal["buy", "sell", "wait"] = Field(
        ..., 
        description="AI-recommended action: buy, sell, or wait"
    )
    
    last_action_date: Optional[int] = Field(
        None, 
        description="Unix timestamp of last action recommendation"
    )
    
    trade_score: float = Field(
        ..., 
        description="AI trade score (0-100), higher indicates stronger signal"
    )
    
    confidence: float = Field(
        ..., 
        description="Confidence level (0-1), higher indicates more certainty"
    )
    
    current_price: Optional[float] = Field(
        None, 
        description="Current stock price at time of analysis"
    )
    
    optimal_stop_loss: Optional[float] = Field(
        None, 
        description="AI-recommended stop loss price"
    )
    
    stop_loss_percentage: Optional[float] = Field(
        None, 
        description="Stop loss as percentage below current price"
    )
    
    analysis_time: Optional[int] = Field(
        None, 
        description="Unix timestamp when analysis was performed"
    )
    
    interval: Optional[str] = Field(
        None, 
        description="Time interval used for analysis (e.g., 'daily')"
    )
    
    # Additional AI metrics that might be included
    momentum_score: Optional[float] = Field(
        None, 
        description="Momentum indicator score"
    )
    
    volatility_score: Optional[float] = Field(
        None, 
        description="Volatility assessment score"
    )
    
    risk_score: Optional[float] = Field(
        None, 
        description="Risk assessment score"
    )
    
    @validator('trade_score')
    def validate_trade_score(cls, v):
        """Validate trade score is within expected range."""
        if not 0 <= v <= 100:
            raise ValueError('Trade score must be between 0 and 100')
        return v
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Validate confidence is within expected range."""
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v
    
    @validator('stop_loss_percentage')
    def validate_stop_loss_percentage(cls, v):
        """Validate stop loss percentage is reasonable."""
        if v is not None and (v < -50 or v > 0):
            raise ValueError('Stop loss percentage should be negative and reasonable')
        return v
    
    def get_confidence_percentage(self) -> float:
        """Get confidence as percentage (0-100)."""
        return self.confidence * 100
    
    def get_risk_level(self) -> str:
        """Get risk level based on various scores."""
        if self.risk_score is not None:
            if self.risk_score < 30:
                return "Low"
            elif self.risk_score < 70:
                return "Medium"
            else:
                return "High"
        
        # Fallback based on confidence and volatility
        if self.confidence > 0.8:
            return "Low"
        elif self.confidence > 0.5:
            return "Medium"
        else:
            return "High"
    
    def is_strong_signal(self, min_confidence: float = 0.7, min_trade_score: float = 60) -> bool:
        """Check if this is a strong trading signal."""
        return (
            self.confidence >= min_confidence and 
            self.trade_score >= min_trade_score and
            self.action in ["buy", "sell"]
        )


class AIAnalysisResponse(BaseResponse, MetadataMixin):
    """Response model for AI analysis endpoint."""
    
    analysis: AIAnalysis = Field(..., description="AI analysis results")
    
    def get_recommendation_summary(self) -> str:
        """Get a human-readable recommendation summary."""
        analysis = self.analysis
        confidence_pct = analysis.get_confidence_percentage()
        
        action_text = {
            "buy": "BUY",
            "sell": "SELL", 
            "wait": "HOLD/WAIT"
        }.get(analysis.action, analysis.action.upper())
        
        return (
            f"{action_text} {analysis.symbol} "
            f"(Score: {analysis.trade_score:.1f}/100, "
            f"Confidence: {confidence_pct:.1f}%)"
        )
    
    def should_act(self, min_confidence: float = 0.7) -> bool:
        """Determine if action should be taken based on confidence."""
        return (
            self.analysis.confidence >= min_confidence and 
            self.analysis.action != "wait"
        )
