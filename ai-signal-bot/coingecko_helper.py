import requests
import logging
from typing import Dict, Optional, List
from config import Config

logger = logging.getLogger(__name__)

class CoinGeckoHelper:
    """Helper class for CoinGecko API interactions"""
    
    def __init__(self):
        self.base_url = Config.COINGECKO_BASE_URL
        self.api_key = Config.COINGECKO_API_KEY
        self.headers = {}
        
        if self.api_key:
            self.headers['x-cg-demo-api-key'] = self.api_key
    
    def get_coin_list(self) -> Dict[str, str]:
        """
        Get mapping of coin symbols/names to CoinGecko IDs
        Returns a dictionary with symbol -> coin_id mappings
        """
        try:
            url = f"{self.base_url}/coins/list"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            coins_data = response.json()
            
            # Create mappings for both symbol and name
            coin_mapping = {}
            for coin in coins_data:
                # Map by symbol (e.g., 'btc' -> 'bitcoin')
                coin_mapping[coin['symbol'].lower()] = coin['id']
                # Map by name (e.g., 'bitcoin' -> 'bitcoin')
                coin_mapping[coin['name'].lower().replace(' ', '-')] = coin['id']
            
            logger.info(f"Loaded {len(coin_mapping)} coin mappings")
            return coin_mapping
            
        except requests.RequestException as e:
            logger.error(f"Error fetching coin list: {e}")
            return {}
    
    def find_coin_id(self, ticker: str) -> Optional[str]:
        """
        Find CoinGecko coin ID from ticker symbol or name
        
        Args:
            ticker: Coin symbol (e.g., 'BTC', 'arb') or name
            
        Returns:
            CoinGecko coin ID if found, None otherwise
        """
        ticker_lower = ticker.lower().strip()
        coin_mapping = self.get_coin_list()
        
        # Direct symbol match
        if ticker_lower in coin_mapping:
            return coin_mapping[ticker_lower]
        
        # Try some common variations
        variations = [
            ticker_lower,
            f"{ticker_lower}-",
            f"-{ticker_lower}",
            ticker_lower.replace('usdt', '').replace('usd', ''),
        ]
        
        for variation in variations:
            if variation in coin_mapping:
                return coin_mapping[variation]
        
        # Search in coin names (partial match)
        #for name, coin_id in coin_mapping.items():
        #    if ticker_lower in name or name in ticker_lower:
        #        return coin_id
        
        logger.warning(f"Could not find coin ID for ticker: {ticker}")
        return None
    
    def get_current_price(self, coin_id: str, vs_currencies: List[str] = None) -> Optional[Dict]:
        """
        Get current price for a coin
        
        Args:
            coin_id: CoinGecko coin ID
            vs_currencies: List of currencies (default: ['usd', 'sgd'])
            
        Returns:
            Price data dictionary or None if error
        """
        if vs_currencies is None:
            vs_currencies = ['usd', 'sgd']
        
        try:
            currencies_str = ','.join(vs_currencies)
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': currencies_str,
                'include_24hr_change': 'true',
                'include_last_updated_at': 'true'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if coin_id in data:
                logger.info(f"Successfully fetched price for {coin_id}")
                return data[coin_id]
            else:
                logger.error(f"No price data found for coin: {coin_id}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error fetching price for {coin_id}: {e}")
            return None
    
    def get_price_history(self, coin_id: str, days: int = 7) -> Optional[Dict]:
        """
        Get historical price data for a coin
        
        Args:
            coin_id: CoinGecko coin ID
            days: Number of days of history (default: 7)
            
        Returns:
            Historical price data or None if error
        """
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 1 else 'hourly'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched {days}-day history for {coin_id}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching price history for {coin_id}: {e}")
            return None
    
    def analyze_ticker(self, ticker: str) -> Dict:
        """
        Complete analysis pipeline for a ticker
        
        Args:
            ticker: Coin ticker/symbol
            
        Returns:
            Dictionary with coin data or error information
        """
        result = {
            'success': False,
            'ticker': ticker,
            'coin_id': None,
            'current_price': None,
            'error': None
        }
        
        # Find coin ID
        coin_id = self.find_coin_id(ticker)
        if not coin_id:
            result['error'] = f"Could not find coin with ticker '{ticker}'. Please check the ticker symbol."
            return result
        
        result['coin_id'] = coin_id
        
        # Get current price
        price_data = self.get_current_price(coin_id)
        if not price_data:
            result['error'] = f"Could not fetch price data for {ticker.upper()}"
            return result
        
        result['current_price'] = price_data
        result['success'] = True
        
        return result
    
    def get_coin_sector(self, coin_id: str) -> str:
        """Fetch the primary sector/category for a coin"""
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'false',
                'community_data': 'false',
                'developer_data': 'false',
                'sparkline': 'false'
            }
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            categories = data.get('categories', [])
            return categories[0] if categories else 'Unknown'
        except requests.RequestException as e:
            logger.error(f"Error fetching sector for {coin_id}: {e}")
            return 'Unknown'

    def get_top_movers(self) -> List[Dict]:
        """Get top 10 coins filtered by market cap, volume and 24h change"""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': 'sgd',
                'order': 'market_cap_desc',
                'per_page': 250,
                'page': 1,
                'price_change_percentage': '24h'
            }
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            filtered = []
            for coin in data:
                market_cap = coin.get('market_cap') or 0
                volume = coin.get('total_volume') or 0
                pct_change = coin.get('price_change_percentage_24h') or 0
                if (
                    10_000_000 <= market_cap <= 100_000_000 and
                    10 <= pct_change <= 50 and
                    10_000_000 <= volume <= 100_000_000
                ):
                    sector = self.get_coin_sector(coin['id'])
                    filtered.append({
                        'symbol': coin['symbol'].upper(),
                        'current_price': coin.get('current_price'),
                        'price_change_24h': coin.get('price_change_24h'),
                        'price_change_percentage_24h': pct_change,
                        'sector': sector
                    })

            filtered.sort(key=lambda x: x['price_change_percentage_24h'], reverse=True)
            return filtered[:10]
        except requests.RequestException as e:
            logger.error(f"Error fetching top movers: {e}")
            return []