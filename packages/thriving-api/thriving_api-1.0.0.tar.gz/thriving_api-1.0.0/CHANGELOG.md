# Changelog

All notable changes to the Thriving API Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-14

### Added
- Initial release of the Thriving API Python SDK
- Complete API coverage for all 68 endpoints
- AI-powered stock analysis module
- Symbol data module (search, performance, quotes, OHLC, news)
- Company data module (fundamentals, earnings, details)
- Technical indicators module (50+ indicators)
- Options data module (options chains, contract details)
- Market data module (market status, trading hours)
- Comprehensive error handling and retry logic
- Intelligent rate limiting with adaptive behavior
- Full type safety with Pydantic models
- Async/await support for high-performance applications
- Extensive documentation and examples
- PyPI package distribution

### Features
- **AI Analysis**: Get buy/sell/hold recommendations with confidence scores
- **Real-Time Data**: Live quotes, OHLC data, and market status
- **Technical Analysis**: RSI, MACD, Bollinger Bands, and 50+ more indicators
- **Fundamentals**: P/E ratios, financial health, earnings data
- **Options Trading**: Complete options chains with Greeks and IV
- **News & Sentiment**: AI-powered sentiment analysis
- **Rate Limiting**: Prevents API quota exhaustion
- **Error Recovery**: Automatic retries with exponential backoff
- **Type Safety**: Full type hints and validation
- **Context Managers**: Proper resource management

### Technical Details
- Python 3.10+ support
- Built with httpx for modern async HTTP
- Pydantic v2 for data validation
- Comprehensive test coverage
- Black, isort, and mypy for code quality
- Sphinx documentation generation
- Pre-commit hooks for development

### API Modules
- `client.ai` - AI-powered analysis and recommendations
- `client.symbol` - Symbol search, quotes, performance, news
- `client.company` - Fundamentals, earnings, company details
- `client.technical` - Technical indicators and analysis
- `client.options` - Options chains and contract data
- `client.market` - Market status and trading hours

### Examples
- Basic usage patterns
- AI analysis workflows
- Batch processing
- Portfolio analysis
- Error handling
- Rate limiting management

## [Unreleased]

### Planned Features
- WebSocket support for real-time streaming
- Caching layer for improved performance
- Additional technical indicators
- Portfolio optimization tools
- Backtesting framework integration
- Enhanced documentation with tutorials
