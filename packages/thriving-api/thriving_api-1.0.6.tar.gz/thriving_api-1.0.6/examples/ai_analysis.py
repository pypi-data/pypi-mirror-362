#!/usr/bin/env python3
"""
AI Analysis examples for the Thriving API Python SDK.

This example demonstrates advanced AI analysis functionality including
batch analysis, signal filtering, and trading decision support.
"""

import asyncio
import os
from typing import List, Dict, Any
from thriving_api import ThrivingAPI, SymbolNotFoundError


async def single_symbol_analysis():
    """Demonstrate detailed AI analysis for a single symbol."""
    print("=== Single Symbol AI Analysis ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        print("Please set THRIVING_API_KEY environment variable")
        return
    
    async with ThrivingAPI(api_key=api_key) as client:
        symbol = "AAPL"
        
        try:
            # Get AI analysis
            analysis = await client.ai.analyze_symbol(symbol)
            ai_data = analysis.analysis
            
            print(f"Analysis for {ai_data.symbol}:")
            print(f"  Action: {ai_data.action.upper()}")
            print(f"  Trade Score: {ai_data.trade_score:.1f}/100")
            print(f"  Confidence: {ai_data.get_confidence_percentage():.1f}%")
            print(f"  Current Price: ${ai_data.current_price:.2f}")
            
            if ai_data.optimal_stop_loss:
                print(f"  Suggested Stop Loss: ${ai_data.optimal_stop_loss:.2f}")
                print(f"  Stop Loss %: {ai_data.stop_loss_percentage:.2f}%")
            
            # Interpret the action
            interpretation = client.ai.interpret_action(ai_data.action)
            print(f"  Interpretation: {interpretation}")
            
            # Get confidence level
            confidence_level = client.ai.get_confidence_level(ai_data.confidence)
            print(f"  Confidence Level: {confidence_level}")
            
            # Get trade score level
            score_level = client.ai.get_trade_score_level(ai_data.trade_score)
            print(f"  Trade Score Level: {score_level}")
            
            # Check if signal is strong enough
            should_act = client.ai.should_act_on_signal(analysis, min_confidence=0.7, min_trade_score=60)
            print(f"  Should Act: {'✅ YES' if should_act else '❌ NO'}")
            
            # Additional analysis
            if ai_data.is_strong_signal():
                print("  🔥 This is a STRONG trading signal!")
            
            risk_level = ai_data.get_risk_level()
            print(f"  Risk Level: {risk_level}")
            
        except SymbolNotFoundError:
            print(f"❌ Symbol {symbol} not found")
        except Exception as e:
            print(f"❌ Error: {e}")


async def batch_symbol_analysis():
    """Demonstrate batch analysis of multiple symbols."""
    print("\n=== Batch Symbol Analysis ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    # Popular tech stocks
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "META", "AMZN", "NFLX"]
    
    async with ThrivingAPI(api_key=api_key) as client:
        print(f"Analyzing {len(symbols)} symbols...")
        
        # Analyze all symbols concurrently
        tasks = []
        for symbol in symbols:
            task = analyze_symbol_safe(client, symbol)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Process results
        successful_analyses = []
        failed_analyses = []
        
        for symbol, result in zip(symbols, results):
            if result:
                successful_analyses.append((symbol, result))
            else:
                failed_analyses.append(symbol)
        
        # Display results
        print(f"\nSuccessfully analyzed: {len(successful_analyses)}")
        print(f"Failed analyses: {len(failed_analyses)}")
        
        if failed_analyses:
            print(f"Failed symbols: {', '.join(failed_analyses)}")
        
        # Sort by trade score
        successful_analyses.sort(key=lambda x: x[1].analysis.trade_score, reverse=True)
        
        print("\n📊 Analysis Results (sorted by trade score):")
        print("-" * 80)
        print(f"{'Symbol':<8} {'Action':<6} {'Score':<6} {'Conf%':<6} {'Price':<8} {'Signal'}")
        print("-" * 80)
        
        for symbol, analysis in successful_analyses:
            ai_data = analysis.analysis
            signal_strength = "🔥" if ai_data.is_strong_signal() else "⚠️" if ai_data.trade_score > 50 else "❌"
            
            print(f"{symbol:<8} {ai_data.action.upper():<6} {ai_data.trade_score:>5.1f} "
                  f"{ai_data.get_confidence_percentage():>5.1f} ${ai_data.current_price:>6.2f} {signal_strength}")


async def analyze_symbol_safe(client: ThrivingAPI, symbol: str):
    """Safely analyze a symbol with error handling."""
    try:
        return await client.ai.analyze_symbol(symbol)
    except Exception as e:
        print(f"❌ Failed to analyze {symbol}: {e}")
        return None


async def filter_strong_signals():
    """Demonstrate filtering for strong trading signals."""
    print("\n=== Strong Signal Filtering ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    # Broader set of symbols
    symbols = [
        "AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "META", "AMZN", "NFLX",
        "AMD", "INTC", "CRM", "ORCL", "ADBE", "NOW", "SNOW", "PLTR"
    ]
    
    async with ThrivingAPI(api_key=api_key) as client:
        print(f"Screening {len(symbols)} symbols for strong signals...")
        
        # Analyze all symbols
        tasks = [analyze_symbol_safe(client, symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        
        # Filter for strong signals
        strong_buy_signals = []
        strong_sell_signals = []
        
        for symbol, result in zip(symbols, results):
            if not result:
                continue
            
            ai_data = result.analysis
            
            # Define strong signal criteria
            is_strong = (
                ai_data.confidence >= 0.75 and 
                ai_data.trade_score >= 70 and
                ai_data.action != "wait"
            )
            
            if is_strong:
                if ai_data.action == "buy":
                    strong_buy_signals.append((symbol, result))
                elif ai_data.action == "sell":
                    strong_sell_signals.append((symbol, result))
        
        # Display strong signals
        print(f"\n🟢 Strong BUY Signals ({len(strong_buy_signals)}):")
        if strong_buy_signals:
            for symbol, analysis in strong_buy_signals:
                ai_data = analysis.analysis
                print(f"  {symbol}: Score {ai_data.trade_score:.1f}, "
                      f"Confidence {ai_data.get_confidence_percentage():.1f}%, "
                      f"Price ${ai_data.current_price:.2f}")
        else:
            print("  No strong buy signals found")
        
        print(f"\n🔴 Strong SELL Signals ({len(strong_sell_signals)}):")
        if strong_sell_signals:
            for symbol, analysis in strong_sell_signals:
                ai_data = analysis.analysis
                print(f"  {symbol}: Score {ai_data.trade_score:.1f}, "
                      f"Confidence {ai_data.get_confidence_percentage():.1f}%, "
                      f"Price ${ai_data.current_price:.2f}")
        else:
            print("  No strong sell signals found")


async def custom_data_analysis():
    """Demonstrate AI analysis with custom data."""
    print("\n=== Custom Data Analysis ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    async with ThrivingAPI(api_key=api_key) as client:
        symbol = "TSLA"
        
        # Custom data to enhance analysis
        custom_data = {
            "risk_tolerance": "moderate",
            "time_horizon": "medium_term",
            "portfolio_size": "large",
            "sector_preference": "technology",
            "additional_context": "Looking for growth opportunities"
        }
        
        try:
            # Get enhanced analysis with custom data
            analysis = await client.ai.analyze_symbol_with_data(symbol, custom_data)
            ai_data = analysis.analysis
            
            print(f"Enhanced analysis for {symbol} with custom data:")
            print(f"  Action: {ai_data.action.upper()}")
            print(f"  Trade Score: {ai_data.trade_score:.1f}/100")
            print(f"  Confidence: {ai_data.get_confidence_percentage():.1f}%")
            print(f"  Current Price: ${ai_data.current_price:.2f}")
            
            # Compare with standard analysis
            standard_analysis = await client.ai.analyze_symbol(symbol)
            standard_data = standard_analysis.analysis
            
            print(f"\nComparison with standard analysis:")
            print(f"  Score difference: {ai_data.trade_score - standard_data.trade_score:+.1f}")
            print(f"  Confidence difference: {(ai_data.confidence - standard_data.confidence) * 100:+.1f}%")
            
            if ai_data.action != standard_data.action:
                print(f"  ⚠️  Action changed from {standard_data.action} to {ai_data.action}")
            
        except Exception as e:
            print(f"❌ Error: {e}")


async def portfolio_analysis():
    """Demonstrate portfolio-level AI analysis."""
    print("\n=== Portfolio Analysis ===")
    
    api_key = os.getenv("THRIVING_API_KEY")
    if not api_key:
        return
    
    # Sample portfolio
    portfolio = {
        "AAPL": {"shares": 100, "avg_cost": 150.00},
        "GOOGL": {"shares": 50, "avg_cost": 2500.00},
        "MSFT": {"shares": 75, "avg_cost": 300.00},
        "TSLA": {"shares": 25, "avg_cost": 800.00},
        "NVDA": {"shares": 30, "avg_cost": 400.00}
    }
    
    async with ThrivingAPI(api_key=api_key) as client:
        print("Analyzing portfolio positions...")
        
        portfolio_analysis = []
        
        for symbol, position in portfolio.items():
            try:
                analysis = await client.ai.analyze_symbol(symbol)
                ai_data = analysis.analysis
                
                # Calculate position value and P&L
                current_value = position["shares"] * ai_data.current_price
                cost_basis = position["shares"] * position["avg_cost"]
                unrealized_pnl = current_value - cost_basis
                unrealized_pnl_pct = (unrealized_pnl / cost_basis) * 100
                
                portfolio_analysis.append({
                    "symbol": symbol,
                    "analysis": analysis,
                    "position": position,
                    "current_value": current_value,
                    "unrealized_pnl": unrealized_pnl,
                    "unrealized_pnl_pct": unrealized_pnl_pct
                })
                
            except Exception as e:
                print(f"❌ Failed to analyze {symbol}: {e}")
        
        # Display portfolio analysis
        print("\n📈 Portfolio Analysis:")
        print("-" * 100)
        print(f"{'Symbol':<8} {'Shares':<8} {'Avg Cost':<10} {'Current':<10} {'Value':<12} {'P&L':<12} {'Action':<6}")
        print("-" * 100)
        
        total_value = 0
        total_pnl = 0
        
        for item in portfolio_analysis:
            ai_data = item["analysis"].analysis
            total_value += item["current_value"]
            total_pnl += item["unrealized_pnl"]
            
            pnl_str = f"${item['unrealized_pnl']:+,.0f} ({item['unrealized_pnl_pct']:+.1f}%)"
            
            print(f"{item['symbol']:<8} {item['position']['shares']:<8} "
                  f"${item['position']['avg_cost']:<9.2f} ${ai_data.current_price:<9.2f} "
                  f"${item['current_value']:<11,.0f} {pnl_str:<12} {ai_data.action.upper():<6}")
        
        print("-" * 100)
        print(f"{'TOTAL':<8} {'':<8} {'':<10} {'':<10} ${total_value:<11,.0f} ${total_pnl:+,.0f}")
        
        # Portfolio recommendations
        print(f"\n📋 Portfolio Recommendations:")
        
        sell_recommendations = [item for item in portfolio_analysis if item["analysis"].analysis.action == "sell"]
        buy_recommendations = [item for item in portfolio_analysis if item["analysis"].analysis.action == "buy"]
        
        if sell_recommendations:
            print("  🔴 Consider selling:")
            for item in sell_recommendations:
                ai_data = item["analysis"].analysis
                print(f"    {item['symbol']}: Score {ai_data.trade_score:.1f}, "
                      f"Confidence {ai_data.get_confidence_percentage():.1f}%")
        
        if buy_recommendations:
            print("  🟢 Consider buying more:")
            for item in buy_recommendations:
                ai_data = item["analysis"].analysis
                print(f"    {item['symbol']}: Score {ai_data.trade_score:.1f}, "
                      f"Confidence {ai_data.get_confidence_percentage():.1f}%")


async def main():
    """Run all AI analysis examples."""
    print("Thriving API Python SDK - AI Analysis Examples")
    print("=" * 60)
    
    await single_symbol_analysis()
    await batch_symbol_analysis()
    await filter_strong_signals()
    await custom_data_analysis()
    await portfolio_analysis()
    
    print("\n✅ All AI analysis examples completed!")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("THRIVING_API_KEY"):
        print("Please set your API key:")
        print("export THRIVING_API_KEY='your-api-key-here'")
        exit(1)
    
    # Run examples
    asyncio.run(main())
