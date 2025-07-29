"""
Options data module for the Thriving API SDK.

This module provides access to options-related endpoints including
options chains, contract details, and historical data.
"""

from ..base_client import BaseClient
from ..models.options import OptionsChainResponse
from ..exceptions import ValidationError, SymbolNotFoundError


class OptionsModule:
    """Options data endpoints wrapper."""
    
    def __init__(self, client: BaseClient) -> None:
        """
        Initialize Options module.
        
        Args:
            client: Base HTTP client instance
        """
        self.client = client
    
    async def get_chain(self, symbol: str) -> OptionsChainResponse:
        """
        Get comprehensive options chain data for a stock symbol.
        
        This endpoint provides detailed options information including all available
        option contracts (calls and puts), strike prices, expiration dates,
        bid/ask prices, volume, open interest, Greeks, and implied volatility.
        
        Args:
            symbol: Stock symbol (e.g., "AAPL", "TSLA")
            
        Returns:
            OptionsChainResponse: Complete options chain data
            
        Raises:
            ValidationError: If symbol format is invalid
            SymbolNotFoundError: If symbol is not found
            ThrivingAPIError: For other API errors
            
        Example:
            >>> client = ThrivingAPI(api_key="your-api-key")
            >>> options = await client.options.get_chain("AAPL")
            >>> 
            >>> # Get summary
            >>> summary = options.options.get_option_chain_summary()
            >>> print(f"Total contracts: {summary['total_contracts']}")
            >>> print(f"Call contracts: {summary['call_contracts']}")
            >>> print(f"Put contracts: {summary['put_contracts']}")
            >>> 
            >>> # Get most active contracts
            >>> active = options.get_most_active_contracts(limit=5)
            >>> for contract in active:
            ...     print(f"{contract.contract_symbol}: Volume {contract.get_volume()}")
            >>> 
            >>> # Get liquid contracts only
            >>> liquid = options.options.get_liquid_contracts()
            >>> print(f"Liquid contracts: {len(liquid)}")
        """
        # Validate symbol
        if not self._validate_symbol(symbol):
            raise ValidationError(f"Invalid symbol format: {symbol}")
        
        symbol = symbol.upper().strip()
        
        try:
            response_data = await self.client.get(f"/options/{symbol}")
            return OptionsChainResponse(**response_data)
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
    
    def analyze_options_flow(self, options_response: OptionsChainResponse) -> dict:
        """
        Analyze options flow and activity.
        
        Args:
            options_response: Options chain response
            
        Returns:
            dict: Options flow analysis
        """
        options_data = options_response.options
        analysis = {
            "total_volume": 0,
            "total_open_interest": 0,
            "call_volume": 0,
            "put_volume": 0,
            "call_put_ratio": None,
            "most_active_strikes": [],
            "high_iv_contracts": [],
            "liquidity_analysis": {}
        }
        
        # Calculate volumes
        for contract in options_data.calls:
            volume = contract.get_volume() or 0
            analysis["call_volume"] += volume
            analysis["total_volume"] += volume
        
        for contract in options_data.puts:
            volume = contract.get_volume() or 0
            analysis["put_volume"] += volume
            analysis["total_volume"] += volume
        
        # Calculate call/put ratio
        if analysis["put_volume"] > 0:
            analysis["call_put_ratio"] = analysis["call_volume"] / analysis["put_volume"]
        
        # Get most active strikes
        strike_volumes = {}
        for contract in options_data.get_all_contracts():
            strike = contract.get_strike()
            volume = contract.get_volume() or 0
            if strike and volume > 0:
                strike_volumes[strike] = strike_volumes.get(strike, 0) + volume
        
        # Sort by volume and get top 5
        sorted_strikes = sorted(strike_volumes.items(), key=lambda x: x[1], reverse=True)
        analysis["most_active_strikes"] = sorted_strikes[:5]
        
        # Get high IV contracts
        analysis["high_iv_contracts"] = options_response.get_highest_iv_contracts(limit=5)
        
        # Liquidity analysis
        liquid_contracts = options_data.get_liquid_contracts()
        analysis["liquidity_analysis"] = {
            "total_contracts": len(options_data.get_all_contracts()),
            "liquid_contracts": len(liquid_contracts),
            "liquidity_ratio": len(liquid_contracts) / len(options_data.get_all_contracts()) if options_data.get_all_contracts() else 0
        }
        
        return analysis
    
    def find_optimal_strikes(self, options_response: OptionsChainResponse, strategy: str = "covered_call") -> list:
        """
        Find optimal strike prices for common options strategies.
        
        Args:
            options_response: Options chain response
            strategy: Strategy type ("covered_call", "cash_secured_put", "straddle")
            
        Returns:
            list: Recommended contracts for the strategy
        """
        options_data = options_response.options
        
        if strategy == "covered_call":
            # Find liquid call options with good premium
            candidates = []
            for contract in options_data.calls:
                if (contract.is_liquid() and 
                    contract.get_last_price() and 
                    contract.get_last_price() > 0.5):  # Minimum premium
                    candidates.append(contract)
            
            # Sort by premium (descending)
            return sorted(candidates, key=lambda x: x.get_last_price() or 0, reverse=True)[:5]
        
        elif strategy == "cash_secured_put":
            # Find liquid put options with good premium
            candidates = []
            for contract in options_data.puts:
                if (contract.is_liquid() and 
                    contract.get_last_price() and 
                    contract.get_last_price() > 0.5):  # Minimum premium
                    candidates.append(contract)
            
            # Sort by premium (descending)
            return sorted(candidates, key=lambda x: x.get_last_price() or 0, reverse=True)[:5]
        
        elif strategy == "straddle":
            # Find ATM options with high IV
            if not options_data.underlying_price:
                return []
            
            atm_contracts = options_data.get_atm_contracts(tolerance=5.0)
            
            # Filter for high IV and liquidity
            candidates = []
            for contract in atm_contracts:
                iv = contract.get_implied_volatility()
                if contract.is_liquid() and iv and iv > 0.3:  # High IV threshold
                    candidates.append(contract)
            
            return sorted(candidates, key=lambda x: x.get_implied_volatility() or 0, reverse=True)[:10]
        
        return []
