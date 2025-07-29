"""
AI analysis module for the Thriving API SDK.

This module provides access to AI-powered analysis endpoints including
stock analysis and trading recommendations.
"""

from typing import Optional, Dict, Any

from ..base_client import BaseClient
from ..models.ai import AIAnalysisResponse
from ..exceptions import ValidationError, SymbolNotFoundError


class AIModule:
    """AI analysis endpoints wrapper."""
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize AI module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def analyze_symbol(self, symbol: str) -> AIAnalysisResponse:
        """
        Get AI-powered analysis and trading recommendations for a stock symbol.
        
        This endpoint provides comprehensive AI analysis using proprietary machine 
        learning models that process 100+ technical indicators, market sentiment, 
        company earnings data, and historical price patterns.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA", "NVDA")
            
        Returns:
            AIAnalysisResponse: AI analysis results with trading recommendations
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> analysis = await client.ai.analyze_symbol("AAPL")
            >>> print(f"Action: {analysis.analysis.action}")
            >>> print(f"Confidence: {analysis.analysis.get_confidence_percentage():.1f}%")
            >>> print(f"Trade Score: {analysis.analysis.trade_score:.1f}/100")
        """
        # Validate symbol format
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")
        
        symbol = symbol.upper().strip()
        if not symbol.replace(".", "").replace("-", "").isalnum() or len(symbol) > 10:
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        try:
            response_data = await self.client.get(f"/analyze/{symbol}")
            return AIAnalysisResponse(**response_data)
        except Exception as e:
            # Check if it's a symbol not found error
            if "not found" in str(e).lower() or "invalid" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def analyze_symbol_with_data(
        self, 
        symbol: str, 
        custom_data: Optional[Dict[str, Any]] = None
    ) -> AIAnalysisResponse:
        """
        Get AI analysis with custom data input (POST endpoint).
        
        This endpoint allows you to provide additional data for the AI analysis,
        which can improve the accuracy of recommendations.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA", "NVDA")
            custom_data: Optional custom data to enhance analysis
            
        Returns:
            AIAnalysisResponse: AI analysis results with trading recommendations
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> custom_data = {"risk_tolerance": "moderate", "time_horizon": "long"}
            >>> analysis = await client.ai.analyze_symbol_with_data("AAPL", custom_data)
            >>> print(f"Recommendation: {analysis.get_recommendation_summary()}")
        """
        # Validate symbol format
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")
        
        symbol = symbol.upper().strip()
        if not symbol.replace(".", "").replace("-", "").isalnum() or len(symbol) > 10:
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        # Prepare request data
        request_data = custom_data or {}
        
        try:
            response_data = await self.client.post(
                f"/symbol/{symbol}/analyze", 
                json_data=request_data
            )
            return AIAnalysisResponse(**response_data)
        except Exception as e:
            # Check if it's a symbol not found error
            if "not found" in str(e).lower() or "invalid" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate symbol format.
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            bool: True if symbol format is valid
        """
        if not symbol or not isinstance(symbol, str):
            return False
        
        symbol = symbol.upper().strip()
        return (
            symbol.replace(".", "").replace("-", "").isalnum() and 
            1 <= len(symbol) <= 10
        )
    
    def interpret_action(self, action: str) -> str:
        """
        Get human-readable interpretation of AI action.
        
        Args:
            action: AI action ("buy", "sell", "wait")
            
        Returns:
            str: Human-readable interpretation
        """
        interpretations = {
            "buy": "The AI recommends BUYING this stock based on positive signals",
            "sell": "The AI recommends SELLING this stock based on negative signals", 
            "wait": "The AI recommends WAITING/HOLDING - signals are mixed or unclear"
        }
        
        return interpretations.get(action.lower(), f"Unknown action: {action}")
    
    def get_confidence_level(self, confidence: float) -> str:
        """
        Get confidence level description.
        
        Args:
            confidence: Confidence value (0-1)
            
        Returns:
            str: Confidence level description
        """
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.8:
            return "High"
        elif confidence >= 0.7:
            return "Moderate"
        elif confidence >= 0.6:
            return "Low"
        else:
            return "Very Low"
    
    def get_trade_score_level(self, trade_score: float) -> str:
        """
        Get trade score level description.
        
        Args:
            trade_score: Trade score (0-100)
            
        Returns:
            str: Trade score level description
        """
        if trade_score >= 80:
            return "Very Strong"
        elif trade_score >= 70:
            return "Strong"
        elif trade_score >= 60:
            return "Moderate"
        elif trade_score >= 40:
            return "Weak"
        else:
            return "Very Weak"
    
    def should_act_on_signal(
        self, 
        analysis: AIAnalysisResponse, 
        min_confidence: float = 0.7,
        min_trade_score: float = 60
    ) -> bool:
        """
        Determine if you should act on the AI signal based on thresholds.
        
        Args:
            analysis: AI analysis response
            min_confidence: Minimum confidence threshold (0-1)
            min_trade_score: Minimum trade score threshold (0-100)
            
        Returns:
            bool: True if signal meets thresholds and action is not "wait"
        """
        return (
            analysis.analysis.confidence >= min_confidence and
            analysis.analysis.trade_score >= min_trade_score and
            analysis.analysis.action != "wait"
        )
