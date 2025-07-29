"""
Symbol data models for the Thriving API SDK.

This module contains Pydantic models for symbol-related endpoints
including search, performance, quotes, OHLC data, and news.
"""

from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

from .base import (
    BaseResponse, SymbolMixin, TimestampMixin, MarketDataMixin, 
    MetadataMixin, PriceType, VolumeType
)


class SymbolMatch(BaseModel):
    """Individual symbol match from search results."""
    
    symbol: str = Field(..., description="Stock symbol")
    name: str = Field(..., description="Company name")
    type: str = Field(..., description="Security type (e.g., 'Equity')")
    region: Optional[str] = Field(None, description="Market region")
    market_open: Optional[str] = Field(None, description="Market open time")
    market_close: Optional[str] = Field(None, description="Market close time")
    timezone: Optional[str] = Field(None, description="Market timezone")
    currency: Optional[str] = Field(None, description="Trading currency")
    match_score: Optional[float] = Field(None, description="Search relevance score")
    
    @validator('match_score')
    def validate_match_score(cls, v):
        """Validate match score is within expected range."""
        if v is not None and not 0 <= v <= 1:
            raise ValueError('Match score must be between 0 and 1')
        return v


class SymbolSearchResults(BaseModel):
    """Search results container."""
    
    query: str = Field(..., description="Original search query")
    total_matches: int = Field(..., description="Total number of matches found")
    matches: List[SymbolMatch] = Field(..., description="List of symbol matches")
    
    def get_best_match(self) -> Optional[SymbolMatch]:
        """Get the best matching symbol."""
        if not self.matches:
            return None
        
        # Sort by match score if available, otherwise return first
        if self.matches[0].match_score is not None:
            return max(self.matches, key=lambda x: x.match_score or 0)
        return self.matches[0]
    
    def get_exact_matches(self) -> List[SymbolMatch]:
        """Get exact symbol matches."""
        return [
            match for match in self.matches 
            if match.symbol.upper() == self.query.upper()
        ]


class SymbolSearchResponse(BaseResponse, MetadataMixin):
    """Response model for symbol search endpoint."""
    
    results: SymbolSearchResults = Field(..., description="Search results")


class PerformanceResponse(BaseResponse, MetadataMixin):
    """Response model for market performance endpoint."""
    
    performance: Dict[str, str] = Field(..., description="Performance data by time period")
    symbol: Optional[str] = Field(None, description="Stock symbol")
    
    def get_performance_float(self, period: str) -> Optional[float]:
        """Get performance as float for a specific period."""
        perf_str = self.performance.get(period)
        if not perf_str:
            return None
        
        try:
            # Remove percentage sign and convert to float
            return float(perf_str.rstrip('%'))
        except (ValueError, AttributeError):
            return None
    
    def get_all_periods(self) -> List[str]:
        """Get all available time periods."""
        return list(self.performance.keys())


class OHLCData(BaseModel, MarketDataMixin, TimestampMixin):
    """OHLC (Open, High, Low, Close) data point."""
    
    adj_close: Optional[PriceType] = Field(None, description="Adjusted closing price")
    div_amount: Optional[PriceType] = Field(None, description="Dividend amount")
    ce: Optional[Union[str, float]] = Field(None, description="Corporate events indicator")
    
    def get_adj_close(self) -> Optional[float]:
        """Get adjusted close as float."""
        return float(self.adj_close) if self.adj_close is not None else None
    
    def get_div_amount(self) -> Optional[float]:
        """Get dividend amount as float."""
        return float(self.div_amount) if self.div_amount is not None else None


class LiveQuoteResponse(BaseResponse, MetadataMixin):
    """Response model for live quote endpoint."""
    
    symbol: List[OHLCData] = Field(..., description="Array of OHLC data points")
    
    def get_latest_quote(self) -> Optional[OHLCData]:
        """Get the most recent quote data."""
        return self.symbol[0] if self.symbol else None
    
    def get_previous_quote(self) -> Optional[OHLCData]:
        """Get the previous quote data."""
        return self.symbol[1] if len(self.symbol) > 1 else None
    
    def get_price_change(self) -> Optional[float]:
        """Calculate price change from previous close."""
        latest = self.get_latest_quote()
        previous = self.get_previous_quote()
        
        if not latest or not previous:
            return None
        
        latest_close = latest.get_close()
        previous_close = previous.get_close()
        
        if latest_close is None or previous_close is None:
            return None
        
        return latest_close - previous_close
    
    def get_price_change_percentage(self) -> Optional[float]:
        """Calculate percentage price change."""
        change = self.get_price_change()
        previous = self.get_previous_quote()
        
        if change is None or not previous:
            return None
        
        previous_close = previous.get_close()
        if previous_close is None or previous_close == 0:
            return None
        
        return (change / previous_close) * 100


class OHLCResponse(BaseResponse, MetadataMixin):
    """Response model for OHLC daily data endpoint."""
    
    symbol: List[OHLCData] = Field(..., description="Array of daily OHLC data")
    
    def get_latest_data(self) -> Optional[OHLCData]:
        """Get the most recent OHLC data."""
        return self.symbol[0] if self.symbol else None
    
    def get_data_for_date(self, date_str: str) -> Optional[OHLCData]:
        """Get OHLC data for a specific date."""
        for data_point in self.symbol:
            if data_point.date == date_str:
                return data_point
        return None
    
    def get_date_range(self, start_date: str, end_date: str) -> List[OHLCData]:
        """Get OHLC data for a date range."""
        return [
            data_point for data_point in self.symbol
            if start_date <= (data_point.date or "") <= end_date
        ]


class TickerSentiment(BaseModel):
    """Sentiment data for a specific ticker."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    relevance_score: str = Field(..., description="Relevance score as string")
    ticker_sentiment_score: str = Field(..., description="Sentiment score as string")
    ticker_sentiment_label: str = Field(..., description="Sentiment label")
    
    def get_relevance_score(self) -> Optional[float]:
        """Get relevance score as float."""
        try:
            return float(self.relevance_score)
        except (ValueError, TypeError):
            return None
    
    def get_sentiment_score(self) -> Optional[float]:
        """Get sentiment score as float."""
        try:
            return float(self.ticker_sentiment_score)
        except (ValueError, TypeError):
            return None


class NewsTopic(BaseModel):
    """News topic with relevance score."""
    
    topic: str = Field(..., description="Topic name")
    relevance_score: str = Field(..., description="Topic relevance score")
    
    def get_relevance_score(self) -> Optional[float]:
        """Get relevance score as float."""
        try:
            return float(self.relevance_score)
        except (ValueError, TypeError):
            return None


class NewsItem(BaseModel):
    """Individual news article."""
    
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    time_published: float = Field(..., description="Publication timestamp")
    authors: List[str] = Field(..., description="Article authors")
    summary: str = Field(..., description="Article summary")
    banner_image: Optional[str] = Field(None, description="Banner image URL")
    source: str = Field(..., description="News source")
    category_within_source: str = Field(..., description="Source category")
    source_domain: str = Field(..., description="Source domain")
    topics: List[NewsTopic] = Field(..., description="Article topics")
    overall_sentiment_score: float = Field(..., description="Overall sentiment score")
    overall_sentiment_label: str = Field(..., description="Overall sentiment label")
    ticker_sentiment: List[TickerSentiment] = Field(..., description="Per-ticker sentiment")
    
    def get_published_datetime(self) -> datetime:
        """Get publication time as datetime object."""
        return datetime.fromtimestamp(self.time_published)
    
    def get_sentiment_for_ticker(self, ticker: str) -> Optional[TickerSentiment]:
        """Get sentiment data for a specific ticker."""
        for sentiment in self.ticker_sentiment:
            if sentiment.ticker.upper() == ticker.upper():
                return sentiment
        return None


class NewsFeed(BaseModel):
    """News feed container."""
    
    items: str = Field(..., description="Number of items as string")
    sentiment_score_definition: str = Field(..., description="Sentiment score definition")
    relevance_score_definition: str = Field(..., description="Relevance score definition")
    feed: List[NewsItem] = Field(..., description="List of news articles")
    
    def get_items_count(self) -> int:
        """Get number of items as integer."""
        try:
            return int(self.items)
        except (ValueError, TypeError):
            return len(self.feed)
    
    def get_recent_articles(self, hours: int = 24) -> List[NewsItem]:
        """Get articles from the last N hours."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        return [
            article for article in self.feed
            if article.time_published >= cutoff_time
        ]
    
    def get_articles_by_sentiment(self, sentiment_label: str) -> List[NewsItem]:
        """Get articles with specific sentiment label."""
        return [
            article for article in self.feed
            if article.overall_sentiment_label.lower() == sentiment_label.lower()
        ]


class NewsResponse(BaseResponse, MetadataMixin):
    """Response model for symbol news endpoint."""

    news: NewsFeed = Field(..., description="News feed data")

    def get_latest_article(self) -> Optional[NewsItem]:
        """Get the most recent news article."""
        if not self.news.feed:
            return None
        return max(self.news.feed, key=lambda x: x.time_published)

    def get_sentiment_summary(self) -> Dict[str, int]:
        """Get summary of sentiment distribution."""
        sentiment_counts = {}
        for article in self.news.feed:
            label = article.overall_sentiment_label
            sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        return sentiment_counts
