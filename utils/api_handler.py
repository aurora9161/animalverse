import aiohttp
import random
import asyncio
from typing import Optional, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('AnimalVerse')

class APIHandler:
    """Robust API handler with retries, caching, rate limiting, and fallbacks"""

    # Fallback images for all animals (multiple per animal for variety)
    FALLBACK_IMAGES = {
        'cat': [
            'https://images.unsplash.com/photo-1574158622682-e40ad6b78b3b?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1519052537078-e6302a4968d4?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1503631285353-30e3147e37c5?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1457257cdd26-f3ee03348e95?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=500&h=500&fit=crop',
        ],
        'dog': [
            'https://images.unsplash.com/photo-1633722715463-d30628519b67?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1552053831-71594a27c62d?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1587300411515-9a1b1a8c8e12?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1558788353-f76d92427f16?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1601003834285-6b71ef06f367?w=500&h=500&fit=crop',
        ],
        'fox': [
            'https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?w=500&h=500&fit=crop',
        ],
        'duck': [
            'https://images.unsplash.com/photo-1624995997946-a1c2e315a42f?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1444464666175-1cff627ceab26?w=500&h=500&fit=crop',
        ],
        'rabbit': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1585397743397-ee0f5a9cd78f?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1535241749838-299277b6305f?w=500&h=500&fit=crop',
        ],
        'raccoon': [
            'https://images.unsplash.com/photo-1577781210272-61ef8da1b73f?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1567270762171-79799e56aea1?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1497752531616-c3afd9760a11?w=500&h=500&fit=crop',
        ],
        'owl': [
            'https://images.unsplash.com/photo-1539350881572-88f9c8b88cd3?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1568641755937-b00d6f7c19bb?w=500&h=500&fit=crop',
        ],
        'penguin': [
            'https://images.unsplash.com/photo-1551717743-49959800b1f6?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1551629146-8d3d89e68da0?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=500&h=500&fit=crop',
        ],
        'panda': [
            'https://images.unsplash.com/photo-1564349537286-e23505d75a0e?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1525382455947-f319bc05fb35?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1519834785169-98be25ec3f84?w=500&h=500&fit=crop',
        ],
        'koala': [
            'https://images.unsplash.com/photo-1534188753412-3be32fe000c9?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1459262838948-3e2de6c3638f?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=500&h=500&fit=crop',
        ],
        'sloth': [
            'https://images.unsplash.com/photo-1551324894-4f4f1a7f0d6e?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=500&h=500&fit=crop',
        ],
        'hedgehog': [
            'https://images.unsplash.com/photo-1522069169874-c58ec4b76be5?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1539571696357-5a69c006ae30?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1580069690842-659ad2dd8f7d?w=500&h=500&fit=crop',
        ],
        'otter': [
            'https://images.unsplash.com/photo-1606856110002-d0991ce78b1c?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1591229728215-2a83dbd60066?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1604651367919-33e0c369ee1e?w=500&h=500&fit=crop',
        ],
        'squirrel': [
            'https://images.unsplash.com/photo-1446824653969-c8398aa337df?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1501706362039-c06b2d715385?w=500&h=500&fit=crop',
        ],
        'deer': [
            'https://images.unsplash.com/photo-1484406566174-9da000fda645?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1434694686742-92029fba1ee3?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1545131493-0d5fdb2b5fa3?w=500&h=500&fit=crop',
        ],
        'bear': [
            'https://images.unsplash.com/photo-1551315679-9c6ae9dec224?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1528127269029-c3ee1f0b2c14?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=500&h=500&fit=crop',
        ],
        'wolf': [
            'https://images.unsplash.com/photo-1501706362039-c06b2d715385?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1554256505-a3a7a7ae1a0f?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=500&h=500&fit=crop',
        ],
        'eagle': [
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1579033461380-adb47c3eb938?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1568641755937-b00d6f7c19bb?w=500&h=500&fit=crop',
        ],
        'dolphin': [
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=500&h=500&fit=crop',
            'https://images.unsplash.com/photo-1566316284037-86b9e7c6c6ec?w=500&h=500&fit=crop',
        ],
    }

    def __init__(self, timeout: int = 5, retry_count: int = 3, cache_hours: int = 1):
        """Initialize API handler with configuration"""
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.retry_count = retry_count
        self.cache_duration = timedelta(hours=cache_hours)
        self.cache: Dict[str, Dict] = {}  # {key: {'image': url, 'timestamp': datetime}}
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests
        self.rate_limit_wait = 0  # Rate limit delay

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self.session

    async def close(self) -> None:
        """Close session safely"""
        try:
            if self.session and not self.session.closed:
                await self.session.close()
            self.session = None
        except Exception as e:
            logger.error(f'Error closing session: {e}')

    def _get_cache(self, key: str) -> Optional[str]:
        """Get cached image if still valid"""
        if key in self.cache:
            data = self.cache[key]
            if datetime.now() - data['timestamp'] < self.cache_duration:
                return data['image']
            else:
                del self.cache[key]
        return None

    def _set_cache(self, key: str, image_url: str) -> None:
        """Cache image URL"""
        self.cache[key] = {'image': image_url, 'timestamp': datetime.now()}

    async def _fetch_with_retry(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """Fetch URL with retry logic"""
        async with self.request_semaphore:
            for attempt in range(self.retry_count):
                try:
                    session = await self.get_session()
                    async with session.get(url, headers=headers or {}) as resp:
                        if resp.status == 200:
                            return await resp.text()
                        elif resp.status == 429:  # Rate limited
                            retry_after = int(resp.headers.get('Retry-After', 60))
                            logger.warning(f'Rate limited, waiting {retry_after}s')
                            await asyncio.sleep(min(retry_after, 5))
                        else:
                            logger.debug(f'HTTP {resp.status} on attempt {attempt + 1}')
                except asyncio.TimeoutError:
                    logger.debug(f'Timeout on attempt {attempt + 1}/{self.retry_count}')
                    if attempt < self.retry_count - 1:
                        await asyncio.sleep(0.5)
                except Exception as e:
                    logger.debug(f'Request error: {e}')
                    if attempt < self.retry_count - 1:
                        await asyncio.sleep(0.5)
        return None

    async def get_cat_image(self, api_key: str = '') -> str:
        """Get cat image with caching and fallback"""
        # Check cache first
        cached = self._get_cache('cat')
        if cached:
            return cached

        # Try API if key provided
        if api_key:
            try:
                url = 'https://api.thecatapi.com/v1/images/search'
                headers = {'x-api-key': api_key}
                response = await self._fetch_with_retry(url, headers)
                if response:
                    import json
                    data = json.loads(response)
                    if data and len(data) > 0 and 'url' in data[0]:
                        image_url = data[0]['url']
                        self._set_cache('cat', image_url)
                        return image_url
            except Exception as e:
                logger.debug(f'Cat API error: {e}')

        # Fallback
        fallback = random.choice(self.FALLBACK_IMAGES['cat'])
        self._set_cache('cat', fallback)
        return fallback

    async def get_dog_image(self, api_key: str = '') -> str:
        """Get dog image with caching and fallback"""
        # Check cache first
        cached = self._get_cache('dog')
        if cached:
            return cached

        # Try API if key provided
        if api_key:
            try:
                url = 'https://api.thedogapi.com/v1/images/search'
                headers = {'x-api-key': api_key}
                response = await self._fetch_with_retry(url, headers)
                if response:
                    import json
                    data = json.loads(response)
                    if data and len(data) > 0 and 'url' in data[0]:
                        image_url = data[0]['url']
                        self._set_cache('dog', image_url)
                        return image_url
            except Exception as e:
                logger.debug(f'Dog API error: {e}')

        # Fallback
        fallback = random.choice(self.FALLBACK_IMAGES['dog'])
        self._set_cache('dog', fallback)
        return fallback

    async def get_fox_image(self) -> str:
        """Get fox image with fallback"""
        cached = self._get_cache('fox')
        if cached:
            return cached

        try:
            response = await self._fetch_with_retry('https://randomfox.ca/floof/')
            if response:
                import json
                data = json.loads(response)
                if 'image' in data:
                    image_url = data['image']
                    self._set_cache('fox', image_url)
                    return image_url
        except Exception as e:
            logger.debug(f'Fox API error: {e}')

        fallback = random.choice(self.FALLBACK_IMAGES['fox'])
        self._set_cache('fox', fallback)
        return fallback

    async def get_duck_image(self) -> str:
        """Get duck image with fallback"""
        cached = self._get_cache('duck')
        if cached:
            return cached

        try:
            response = await self._fetch_with_retry('https://random-d.uk/api/random')
            if response:
                import json
                data = json.loads(response)
                if 'url' in data:
                    image_url = data['url']
                    self._set_cache('duck', image_url)
                    return image_url
        except Exception as e:
            logger.debug(f'Duck API error: {e}')

        fallback = random.choice(self.FALLBACK_IMAGES['duck'])
        self._set_cache('duck', fallback)
        return fallback

    def get_static_image(self, animal: str) -> str:
        """Get fallback image for any animal (no API)"""
        animal_lower = animal.lower()
        if animal_lower in self.FALLBACK_IMAGES:
            return random.choice(self.FALLBACK_IMAGES[animal_lower])
        # Default fallback
        return random.choice(self.FALLBACK_IMAGES['cat'])

    def clear_cache(self) -> None:
        """Clear all cached images"""
        self.cache.clear()
        logger.info('API cache cleared')
