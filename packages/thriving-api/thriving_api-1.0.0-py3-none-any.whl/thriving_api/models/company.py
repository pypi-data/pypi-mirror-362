"""
Company data models for the Thriving API SDK.

This module contains Pydantic models for company-related endpoints
including fundamentals, earnings, and company details.
"""

from typing import Optional, Union, Dict, Any, List
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .base import (
    BaseResponse, SymbolMixin, TimestampMixin, MetadataMixin,
    PriceType, PercentageType
)


class CompanyFundamentals(BaseModel, SymbolMixin):
    """Company fundamental data model."""
    
    # Valuation Metrics
    market_cap: Optional[Union[str, int]] = Field(None, description="Market capitalization")
    enterprise_value: Optional[Union[str, int]] = Field(None, description="Enterprise value")
    pe_ratio: Optional[Union[str, float]] = Field(None, description="Price-to-earnings ratio")
    pb_ratio: Optional[Union[str, float]] = Field(None, description="Price-to-book ratio")
    ps_ratio: Optional[Union[str, float]] = Field(None, description="Price-to-sales ratio")
    ev_ebitda: Optional[Union[str, float]] = Field(None, description="EV/EBITDA ratio")
    
    # Profitability Metrics
    roe: Optional[PercentageType] = Field(None, description="Return on equity")
    roa: Optional[PercentageType] = Field(None, description="Return on assets")
    profit_margin: Optional[PercentageType] = Field(None, description="Profit margin")
    operating_margin: Optional[PercentageType] = Field(None, description="Operating margin")
    ebitda_margin: Optional[PercentageType] = Field(None, description="EBITDA margin")
    
    # Financial Health
    debt_to_equity: Optional[Union[str, float]] = Field(None, description="Debt-to-equity ratio")
    current_ratio: Optional[Union[str, float]] = Field(None, description="Current ratio")
    quick_ratio: Optional[Union[str, float]] = Field(None, description="Quick ratio")
    
    # Growth Metrics
    revenue_growth: Optional[PercentageType] = Field(None, description="Revenue growth rate")
    earnings_growth: Optional[PercentageType] = Field(None, description="Earnings growth rate")
    book_value_growth: Optional[PercentageType] = Field(None, description="Book value growth")
    
    # Dividend Information
    dividend_yield: Optional[PercentageType] = Field(None, description="Dividend yield")
    payout_ratio: Optional[PercentageType] = Field(None, description="Dividend payout ratio")
    dividend_per_share: Optional[PriceType] = Field(None, description="Dividend per share")
    
    # Share Information
    shares_outstanding: Optional[Union[str, int]] = Field(None, description="Shares outstanding")
    float_shares: Optional[Union[str, int]] = Field(None, description="Float shares")
    
    # Financial Statement Data
    total_revenue: Optional[Union[str, int]] = Field(None, description="Total revenue")
    net_income: Optional[Union[str, int]] = Field(None, description="Net income")
    total_assets: Optional[Union[str, int]] = Field(None, description="Total assets")
    total_debt: Optional[Union[str, int]] = Field(None, description="Total debt")
    cash_and_equivalents: Optional[Union[str, int]] = Field(None, description="Cash and cash equivalents")
    
    def get_market_cap(self) -> Optional[int]:
        """Get market cap as integer."""
        return int(self.market_cap) if self.market_cap else None
    
    def get_pe_ratio(self) -> Optional[float]:
        """Get P/E ratio as float."""
        return float(self.pe_ratio) if self.pe_ratio else None
    
    def get_debt_to_equity(self) -> Optional[float]:
        """Get debt-to-equity ratio as float."""
        return float(self.debt_to_equity) if self.debt_to_equity else None
    
    def get_dividend_yield_percent(self) -> Optional[float]:
        """Get dividend yield as percentage."""
        if self.dividend_yield is None:
            return None
        try:
            value = float(str(self.dividend_yield).rstrip('%'))
            return value if '%' in str(self.dividend_yield) else value * 100
        except (ValueError, TypeError):
            return None
    
    def is_profitable(self) -> Optional[bool]:
        """Check if company is profitable based on net income."""
        if self.net_income is None:
            return None
        try:
            return float(self.net_income) > 0
        except (ValueError, TypeError):
            return None
    
    def get_financial_strength_score(self) -> Optional[float]:
        """Calculate a simple financial strength score (0-100)."""
        score = 0
        factors = 0
        
        # Current ratio (good if > 1.5)
        if self.current_ratio:
            try:
                ratio = float(self.current_ratio)
                score += min(25, ratio * 16.67)  # Max 25 points
                factors += 1
            except (ValueError, TypeError):
                pass
        
        # Debt to equity (good if < 0.5)
        if self.debt_to_equity:
            try:
                ratio = float(self.debt_to_equity)
                score += max(0, 25 - (ratio * 50))  # Max 25 points
                factors += 1
            except (ValueError, TypeError):
                pass
        
        # ROE (good if > 15%)
        if self.roe:
            try:
                roe_val = float(str(self.roe).rstrip('%'))
                score += min(25, roe_val * 1.67)  # Max 25 points
                factors += 1
            except (ValueError, TypeError):
                pass
        
        # Profit margin (good if > 10%)
        if self.profit_margin:
            try:
                margin = float(str(self.profit_margin).rstrip('%'))
                score += min(25, margin * 2.5)  # Max 25 points
                factors += 1
            except (ValueError, TypeError):
                pass
        
        return score / factors if factors > 0 else None


class FundamentalsResponse(BaseResponse, MetadataMixin):
    """Response model for company fundamentals endpoint."""
    
    fundamentals: CompanyFundamentals = Field(..., description="Company fundamental data")
    
    def get_valuation_summary(self) -> Dict[str, Optional[float]]:
        """Get key valuation metrics."""
        return {
            "pe_ratio": self.fundamentals.get_pe_ratio(),
            "pb_ratio": float(self.fundamentals.pb_ratio) if self.fundamentals.pb_ratio else None,
            "ps_ratio": float(self.fundamentals.ps_ratio) if self.fundamentals.ps_ratio else None,
            "market_cap": self.fundamentals.get_market_cap(),
        }


class EarningsData(BaseModel):
    """Individual earnings data point."""
    
    fiscal_date_ending: str = Field(..., description="Fiscal period end date")
    reported_date: Optional[str] = Field(None, description="Earnings report date")
    reported_eps: Optional[Union[str, float]] = Field(None, description="Reported earnings per share")
    estimated_eps: Optional[Union[str, float]] = Field(None, description="Estimated earnings per share")
    surprise: Optional[Union[str, float]] = Field(None, description="Earnings surprise")
    surprise_percentage: Optional[Union[str, float]] = Field(None, description="Surprise percentage")
    
    def get_reported_eps(self) -> Optional[float]:
        """Get reported EPS as float."""
        return float(self.reported_eps) if self.reported_eps else None
    
    def get_estimated_eps(self) -> Optional[float]:
        """Get estimated EPS as float."""
        return float(self.estimated_eps) if self.estimated_eps else None
    
    def get_surprise(self) -> Optional[float]:
        """Get earnings surprise as float."""
        return float(self.surprise) if self.surprise else None
    
    def beat_estimates(self) -> Optional[bool]:
        """Check if earnings beat estimates."""
        surprise = self.get_surprise()
        return surprise > 0 if surprise is not None else None


class CompanyEarnings(BaseModel, SymbolMixin):
    """Company earnings data model."""
    
    annual_earnings: List[EarningsData] = Field(..., description="Annual earnings data")
    quarterly_earnings: List[EarningsData] = Field(..., description="Quarterly earnings data")
    
    def get_latest_quarterly(self) -> Optional[EarningsData]:
        """Get the most recent quarterly earnings."""
        if not self.quarterly_earnings:
            return None
        return max(self.quarterly_earnings, key=lambda x: x.fiscal_date_ending)
    
    def get_latest_annual(self) -> Optional[EarningsData]:
        """Get the most recent annual earnings."""
        if not self.annual_earnings:
            return None
        return max(self.annual_earnings, key=lambda x: x.fiscal_date_ending)
    
    def get_earnings_trend(self, periods: int = 4) -> Optional[str]:
        """Analyze earnings trend over recent periods."""
        if len(self.quarterly_earnings) < periods:
            return None
        
        recent_earnings = sorted(
            self.quarterly_earnings, 
            key=lambda x: x.fiscal_date_ending, 
            reverse=True
        )[:periods]
        
        beats = sum(1 for e in recent_earnings if e.beat_estimates())
        
        if beats >= periods * 0.75:
            return "Strong"
        elif beats >= periods * 0.5:
            return "Moderate"
        else:
            return "Weak"


class EarningsResponse(BaseResponse, MetadataMixin):
    """Response model for company earnings endpoint."""
    
    earnings: CompanyEarnings = Field(..., description="Company earnings data")


class CompanyDetails(BaseModel, SymbolMixin):
    """Company details and profile information."""
    
    name: Optional[str] = Field(None, description="Company name")
    description: Optional[str] = Field(None, description="Company description")
    sector: Optional[str] = Field(None, description="Business sector")
    industry: Optional[str] = Field(None, description="Industry classification")
    country: Optional[str] = Field(None, description="Country of incorporation")
    currency: Optional[str] = Field(None, description="Reporting currency")
    exchange: Optional[str] = Field(None, description="Primary exchange")
    
    # Contact Information
    address: Optional[str] = Field(None, description="Company address")
    website: Optional[str] = Field(None, description="Company website")
    phone: Optional[str] = Field(None, description="Company phone number")
    
    # Key Personnel
    ceo: Optional[str] = Field(None, description="Chief Executive Officer")
    employees: Optional[Union[str, int]] = Field(None, description="Number of employees")
    
    # Business Information
    fiscal_year_end: Optional[str] = Field(None, description="Fiscal year end month")
    latest_quarter: Optional[str] = Field(None, description="Latest reported quarter")
    
    def get_employee_count(self) -> Optional[int]:
        """Get employee count as integer."""
        return int(self.employees) if self.employees else None


class CompanyDetailsResponse(BaseResponse, MetadataMixin):
    """Response model for company details endpoint."""
    
    details: CompanyDetails = Field(..., description="Company details and profile")
