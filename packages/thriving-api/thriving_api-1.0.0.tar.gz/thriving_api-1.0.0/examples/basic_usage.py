#!/usr/bin/env python3
"""
Basic usage examples for the Thriving API Python SDK.

This example demonstrates the fundamental usage patterns of the SDK
including initialization, basic API calls, and error handling.
"""

import asyncio
import os
from thriving_api import ThrivingAPI, AuthenticationError, SymbolNotFoundError


async def basic_ai_analysis():
    """Demonstrate basic AI analysis functionality."""
    print("=== AI Analysis Example ===")
    
    # Get API key from environment variable
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        print("Please set THRIVING_API_KEY environment variable")
        return
    
    try:
        # Initialize client with context manager (recommended)
        async with ThrivingAPI(api_key=api_key) as client:
            # Analyze Apple stock
            print("Analyzing AAPL...")
            analysis = await client.ai.analyze_symbol("AAPL")
            
            # Display results
            print(f"Symbol: {analysis.analysis.symbol}")
            print(f"Action: {analysis.analysis.action.upper()}")
            print(f"Trade Score: {analysis.analysis.trade_score:.1f}/100")
            print(f"Confidence: {analysis.analysis.get_confidence_percentage():.1f}%")
            
            if analysis.analysis.optimal_stop_loss:
                print(f"Suggested Stop Loss: ${analysis.analysis.optimal_stop_loss:.2f}")
            
            # Get recommendation summary
            print(f"Summary: {analysis.get_recommendation_summary()}")
            
            # Check if signal is strong enough to act on
            if analysis.should_act(min_confidence=0.7):
                print("✅ Strong signal - consider taking action")
            else:
                print("⚠️  Weak signal - proceed with caution")
                
    except AuthenticationError:
        print("❌ Authentication failed - check your API key")
    except SymbolNotFoundError as e:
        print(f"❌ Symbol not found: {e.symbol}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def symbol_search_example():
    """Demonstrate symbol search functionality."""
    print("\n=== Symbol Search Example ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    async with ThrivingAPI(api_key=api_key) as client:
        # Search for Apple
        print("Searching for 'Apple'...")
        results = await client.symbol.search("Apple")
        
        print(f"Found {results.results.total_matches} matches:")
        
        # Show top 3 matches
        for i, match in enumerate(results.results.matches[:3], 1):
            print(f"{i}. {match.symbol} - {match.name}")
            print(f"   Type: {match.type}, Region: {match.region}")
            if match.match_score:
                print(f"   Match Score: {match.match_score:.2f}")
        
        # Get best match
        best_match = results.results.get_best_match()
        if best_match:
            print(f"\nBest match: {best_match.symbol} - {best_match.name}")


async def market_data_example():
    """Demonstrate market data retrieval."""
    print("\n=== Market Data Example ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    async with ThrivingAPI(api_key=api_key) as client:
        symbol = "AAPL"
        
        # Get live quote
        print(f"Getting live quote for {symbol}...")
        quote = await client.symbol.get_live_quote(symbol, "1min")
        latest = quote.get_latest_quote()
        
        if latest:
            print(f"Current Price: ${latest.get_close():.2f}")
            print(f"Volume: {latest.get_volume():,}")
            print(f"High: ${latest.get_high():.2f}")
            print(f"Low: ${latest.get_low():.2f}")
            print(f"Date: {latest.date}")
        
        # Get performance data
        print(f"\nGetting performance data for {symbol}...")
        performance = await client.symbol.get_performance(symbol, "1yr")
        
        print("Performance:")
        for period in performance.get_all_periods():
            perf = performance.get_performance_float(period)
            if perf is not None:
                print(f"  {period}: {perf:+.2f}%")


async def error_handling_example():
    """Demonstrate error handling patterns."""
    print("\n=== Error Handling Example ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    async with ThrivingAPI(api_key=api_key) as client:
        # Try to analyze an invalid symbol
        try:
            await client.ai.analyze_symbol("INVALID123")
        except SymbolNotFoundError as e:
            print(f"✅ Caught symbol not found error: {e.symbol}")
        
        # Try invalid interval
        try:
            await client.symbol.get_performance("AAPL", "invalid_interval")
        except Exception as e:
            print(f"✅ Caught validation error: {e}")


async def client_stats_example():
    """Demonstrate client statistics and monitoring."""
    print("\n=== Client Statistics Example ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    # Initialize client without context manager to show stats
    client = ThrivingAPI(api_key=api_key)
    
    try:
        # Make some API calls
        await client.ai.analyze_symbol("AAPL")
        await client.symbol.search("Tesla")
        await client.symbol.get_live_quote("TSLA", "1min")
        
        # Get client statistics
        stats = client.get_stats()
        print("Client Statistics:")
        print(f"  Total requests: {stats['total_requests']}")
        print(f"  Successful requests: {stats['successful_requests']}")
        print(f"  Failed requests: {stats['failed_requests']}")
        
        # Get rate limiting info
        if client.is_rate_limiting_enabled():
            rate_info = client.get_rate_limit_info()
            print(f"  Current rate: {rate_info['current_rate']:.1f} req/sec")
            print(f"  Available tokens: {rate_info['available_tokens']:.1f}")
        
    finally:
        await client.close()


async def main():
    """Run all examples."""
    print("Thriving API Python SDK - Basic Usage Examples")
    print("=" * 50)
    
    await basic_ai_analysis()
    await symbol_search_example()
    await market_data_example()
    await error_handling_example()
    await client_stats_example()
    
    print("\n✅ All examples completed!")


if __name__ == "__main__":
    # Set up API key
    if not os.getenv("THRIVING_API_KEY"):
        print("Please set your API key:")
        print("export THRIVING_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("THRIVING_API_KEY=your-api-key-here")
        exit(1)
    
    # Run examples
    asyncio.run(main())
