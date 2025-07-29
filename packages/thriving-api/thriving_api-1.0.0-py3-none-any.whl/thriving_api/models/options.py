"""
Options data models for the Thriving API SDK.

This module contains Pydantic models for options-related endpoints
including options chains, contract details, and historical data.
"""

from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime, date

from .base import (
    BaseResponse, SymbolMixin, TimestampMixin, MetadataMixin,
    PriceType, VolumeType
)


class OptionContract(BaseModel):
    """Individual option contract data."""
    
    # Contract Identification
    contract_symbol: str = Field(..., description="Option contract symbol")
    strike: Union[str, float] = Field(..., description="Strike price")
    expiration_date: str = Field(..., description="Expiration date")
    option_type: str = Field(..., description="Option type (call/put)")
    
    # Pricing Data
    last_price: Optional[Union[str, float]] = Field(None, description="Last traded price")
    bid: Optional[Union[str, float]] = Field(None, description="Bid price")
    ask: Optional[Union[str, float]] = Field(None, description="Ask price")
    change: Optional[Union[str, float]] = Field(None, description="Price change")
    percent_change: Optional[Union[str, float]] = Field(None, description="Percentage change")
    
    # Volume and Interest
    volume: Optional[Union[str, int]] = Field(None, description="Trading volume")
    open_interest: Optional[Union[str, int]] = Field(None, description="Open interest")
    
    # Greeks
    delta: Optional[Union[str, float]] = Field(None, description="Delta")
    gamma: Optional[Union[str, float]] = Field(None, description="Gamma")
    theta: Optional[Union[str, float]] = Field(None, description="Theta")
    vega: Optional[Union[str, float]] = Field(None, description="Vega")
    rho: Optional[Union[str, float]] = Field(None, description="Rho")
    
    # Volatility
    implied_volatility: Optional[Union[str, float]] = Field(None, description="Implied volatility")
    
    # Additional Data
    theoretical_value: Optional[Union[str, float]] = Field(None, description="Theoretical option value")
    intrinsic_value: Optional[Union[str, float]] = Field(None, description="Intrinsic value")
    time_value: Optional[Union[str, float]] = Field(None, description="Time value")
    
    @validator('option_type')
    def validate_option_type(cls, v):
        """Validate option type is call or put."""
        if v.lower() not in ['call', 'put']:
            raise ValueError('Option type must be "call" or "put"')
        return v.lower()
    
    def get_strike(self) -> Optional[float]:
        """Get strike price as float."""
        try:
            return float(self.strike)
        except (ValueError, TypeError):
            return None
    
    def get_last_price(self) -> Optional[float]:
        """Get last price as float."""
        try:
            return float(self.last_price) if self.last_price else None
        except (ValueError, TypeError):
            return None
    
    def get_bid(self) -> Optional[float]:
        """Get bid price as float."""
        try:
            return float(self.bid) if self.bid else None
        except (ValueError, TypeError):
            return None
    
    def get_ask(self) -> Optional[float]:
        """Get ask price as float."""
        try:
            return float(self.ask) if self.ask else None
        except (ValueError, TypeError):
            return None
    
    def get_volume(self) -> Optional[int]:
        """Get volume as integer."""
        try:
            return int(self.volume) if self.volume else None
        except (ValueError, TypeError):
            return None
    
    def get_open_interest(self) -> Optional[int]:
        """Get open interest as integer."""
        try:
            return int(self.open_interest) if self.open_interest else None
        except (ValueError, TypeError):
            return None
    
    def get_delta(self) -> Optional[float]:
        """Get delta as float."""
        try:
            return float(self.delta) if self.delta else None
        except (ValueError, TypeError):
            return None
    
    def get_implied_volatility(self) -> Optional[float]:
        """Get implied volatility as float."""
        try:
            return float(self.implied_volatility) if self.implied_volatility else None
        except (ValueError, TypeError):
            return None
    
    def get_bid_ask_spread(self) -> Optional[float]:
        """Calculate bid-ask spread."""
        bid = self.get_bid()
        ask = self.get_ask()
        
        if bid is None or ask is None:
            return None
        
        return ask - bid
    
    def get_bid_ask_spread_percentage(self) -> Optional[float]:
        """Calculate bid-ask spread as percentage of mid-price."""
        bid = self.get_bid()
        ask = self.get_ask()
        
        if bid is None or ask is None or bid + ask == 0:
            return None
        
        mid_price = (bid + ask) / 2
        spread = ask - bid
        
        return (spread / mid_price) * 100 if mid_price > 0 else None
    
    def get_moneyness(self, underlying_price: float) -> str:
        """Determine option moneyness relative to underlying price."""
        strike = self.get_strike()
        if strike is None:
            return "Unknown"
        
        if self.option_type == "call":
            if underlying_price > strike:
                return "In-the-money"
            elif underlying_price < strike:
                return "Out-of-the-money"
            else:
                return "At-the-money"
        else:  # put
            if underlying_price < strike:
                return "In-the-money"
            elif underlying_price > strike:
                return "Out-of-the-money"
            else:
                return "At-the-money"
    
    def get_expiration_datetime(self) -> Optional[datetime]:
        """Get expiration date as datetime object."""
        try:
            return datetime.strptime(self.expiration_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None
    
    def days_to_expiration(self) -> Optional[int]:
        """Calculate days until expiration."""
        exp_date = self.get_expiration_datetime()
        if exp_date is None:
            return None
        
        today = datetime.now().date()
        exp_date_only = exp_date.date()
        
        return (exp_date_only - today).days
    
    def is_liquid(self, min_volume: int = 10, min_open_interest: int = 50) -> bool:
        """Check if option contract is liquid based on volume and open interest."""
        volume = self.get_volume() or 0
        open_interest = self.get_open_interest() or 0
        
        return volume >= min_volume or open_interest >= min_open_interest


class OptionsData(BaseModel, SymbolMixin):
    """Options chain data container."""
    
    calls: List[OptionContract] = Field(..., description="Call option contracts")
    puts: List[OptionContract] = Field(..., description="Put option contracts")
    underlying_price: Optional[float] = Field(None, description="Current underlying stock price")
    
    def get_all_contracts(self) -> List[OptionContract]:
        """Get all option contracts (calls and puts)."""
        return self.calls + self.puts
    
    def get_contracts_by_expiration(self, expiration_date: str) -> List[OptionContract]:
        """Get all contracts for a specific expiration date."""
        return [
            contract for contract in self.get_all_contracts()
            if contract.expiration_date == expiration_date
        ]
    
    def get_contracts_by_strike(self, strike_price: float, tolerance: float = 0.01) -> List[OptionContract]:
        """Get all contracts for a specific strike price."""
        contracts = []
        for contract in self.get_all_contracts():
            contract_strike = contract.get_strike()
            if contract_strike is not None and abs(contract_strike - strike_price) <= tolerance:
                contracts.append(contract)
        return contracts
    
    def get_liquid_contracts(self, min_volume: int = 10, min_open_interest: int = 50) -> List[OptionContract]:
        """Get all liquid option contracts."""
        return [
            contract for contract in self.get_all_contracts()
            if contract.is_liquid(min_volume, min_open_interest)
        ]
    
    def get_expiration_dates(self) -> List[str]:
        """Get all unique expiration dates."""
        dates = set()
        for contract in self.get_all_contracts():
            dates.add(contract.expiration_date)
        return sorted(list(dates))
    
    def get_strike_prices(self) -> List[float]:
        """Get all unique strike prices."""
        strikes = set()
        for contract in self.get_all_contracts():
            strike = contract.get_strike()
            if strike is not None:
                strikes.add(strike)
        return sorted(list(strikes))
    
    def get_atm_contracts(self, tolerance: float = 2.0) -> List[OptionContract]:
        """Get at-the-money contracts within tolerance."""
        if self.underlying_price is None:
            return []
        
        return self.get_contracts_by_strike(self.underlying_price, tolerance)
    
    def get_option_chain_summary(self) -> Dict[str, Any]:
        """Get summary statistics for the options chain."""
        all_contracts = self.get_all_contracts()
        liquid_contracts = self.get_liquid_contracts()
        
        total_volume = sum(
            contract.get_volume() or 0 
            for contract in all_contracts
        )
        
        total_open_interest = sum(
            contract.get_open_interest() or 0 
            for contract in all_contracts
        )
        
        return {
            "total_contracts": len(all_contracts),
            "call_contracts": len(self.calls),
            "put_contracts": len(self.puts),
            "liquid_contracts": len(liquid_contracts),
            "expiration_dates": len(self.get_expiration_dates()),
            "strike_prices": len(self.get_strike_prices()),
            "total_volume": total_volume,
            "total_open_interest": total_open_interest,
            "underlying_price": self.underlying_price,
        }


class OptionsChainResponse(BaseResponse, MetadataMixin):
    """Response model for options chain endpoint."""
    
    options: OptionsData = Field(..., description="Options chain data")
    
    def get_most_active_contracts(self, limit: int = 10) -> List[OptionContract]:
        """Get most active contracts by volume."""
        all_contracts = self.options.get_all_contracts()
        
        # Sort by volume (descending)
        sorted_contracts = sorted(
            all_contracts,
            key=lambda x: x.get_volume() or 0,
            reverse=True
        )
        
        return sorted_contracts[:limit]
    
    def get_highest_iv_contracts(self, limit: int = 10) -> List[OptionContract]:
        """Get contracts with highest implied volatility."""
        all_contracts = self.options.get_all_contracts()
        
        # Filter contracts with IV data and sort by IV (descending)
        contracts_with_iv = [
            contract for contract in all_contracts
            if contract.get_implied_volatility() is not None
        ]
        
        sorted_contracts = sorted(
            contracts_with_iv,
            key=lambda x: x.get_implied_volatility() or 0,
            reverse=True
        )
        
        return sorted_contracts[:limit]
