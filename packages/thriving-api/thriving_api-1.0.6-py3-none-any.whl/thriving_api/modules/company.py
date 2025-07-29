"""
Company data module for the Thriving API SDK.

This module provides access to company-related endpoints including
fundamentals, earnings, and company details.
"""

from ..base_client import BaseClient
from ..models.company import FundamentalsResponse, EarningsResponse, CompanyDetailsResponse
from ..exceptions import ValidationError, SymbolNotFoundError


class CompanyModule:
    """Company data endpoints wrapper."""
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize Company module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def get_fundamentals(self, symbol: str) -> FundamentalsResponse:
        """
        Get comprehensive financial fundamentals and key metrics for a company.
        
        This endpoint provides essential financial data including valuation metrics,
        profitability ratios, financial health indicators, growth metrics, and
        dividend information.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            FundamentalsResponse: Company fundamental data
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> fundamentals = await client.company.get_fundamentals("AAPL")
            >>> print(f"P/E Ratio: {fundamentals.fundamentals.get_pe_ratio()}")
            >>> print(f"Market Cap: ${fundamentals.fundamentals.get_market_cap():,}")
            >>> print(f"ROE: {fundamentals.fundamentals.roe}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/fundamentals/{symbol}")
            return FundamentalsResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_earnings(self, symbol: str) -> EarningsResponse:
        """
        Get earnings data including quarterly and annual earnings history.
        
        This endpoint provides detailed earnings information including reported
        vs estimated EPS, earnings surprises, and historical earnings trends.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            EarningsResponse: Company earnings data
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> earnings = await client.company.get_earnings("AAPL")
            >>> latest = earnings.earnings.get_latest_quarterly()
            >>> if latest:
            ...     print(f"Latest EPS: ${latest.get_reported_eps()}")
            ...     print(f"Beat estimates: {latest.beat_estimates()}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/earnings/{symbol}")
            return EarningsResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    async def get_details(self, symbol: str) -> CompanyDetailsResponse:
        """
        Get detailed company profile and information.
        
        This endpoint provides comprehensive company information including
        business description, sector/industry classification, contact information,
        and key personnel details.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            CompanyDetailsResponse: Company profile and details
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> details = await client.company.get_details("AAPL")
            >>> company = details.details
            >>> print(f"Company: {company.name}")
            >>> print(f"Sector: {company.sector}")
            >>> print(f"Industry: {company.industry}")
            >>> print(f"Employees: {company.get_employee_count():,}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/details/{symbol}")
            return CompanyDetailsResponse(**response_data)
        except Exception as e:
            if "not found" in str(e).lower():
                raise SymbolNotFoundError(symbol) from e
            raise
    
    def _validate_symbol(self, symbol: str) -> bool:
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
    
    def analyze_financial_health(self, fundamentals: FundamentalsResponse) -> dict:
        """
        Analyze financial health based on fundamental metrics.
        
        Args:
            fundamentals: Company fundamentals response
            
        Returns:
            dict: Financial health analysis
        """
        company = fundamentals.fundamentals
        analysis = {
            "overall_score": None,
            "strengths": [],
            "weaknesses": [],
            "recommendations": []
        }
        
        # Calculate financial strength score
        strength_score = company.get_financial_strength_score()
        if strength_score:
            analysis["overall_score"] = strength_score
            
            if strength_score >= 80:
                analysis["recommendations"].append("Strong financial position")
            elif strength_score >= 60:
                analysis["recommendations"].append("Moderate financial health")
            else:
                analysis["recommendations"].append("Weak financial position - proceed with caution")
        
        # Analyze specific metrics
        if company.current_ratio:
            try:
                ratio = float(company.current_ratio)
                if ratio > 2.0:
                    analysis["strengths"].append("Strong liquidity (high current ratio)")
                elif ratio < 1.0:
                    analysis["weaknesses"].append("Poor liquidity (low current ratio)")
            except (ValueError, TypeError):
                pass
        
        if company.debt_to_equity:
            try:
                ratio = float(company.debt_to_equity)
                if ratio < 0.3:
                    analysis["strengths"].append("Low debt levels")
                elif ratio > 1.0:
                    analysis["weaknesses"].append("High debt levels")
            except (ValueError, TypeError):
                pass
        
        if company.is_profitable():
            analysis["strengths"].append("Profitable company")
        elif company.is_profitable() is False:
            analysis["weaknesses"].append("Company is not profitable")
        
        return analysis
