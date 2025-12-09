import aiohttp
import random
from typing import Optional
import os

class APIHandler:
    """Robust API handler with fallback support and error handling"""

    # Fallback images when API fails
    FALLBACK_IMAGES = {
        'cat': [
            'https://images.unsplash.com/photo-1574158622682-e40ad16ae15f',
            'https://images.unsplash.com/photo-1519052537078-e6302a4968d4',
            'https://images.unsplash.com/photo-1495360010541-f48722b34f7d',
            'https://images.unsplash.com/photo-1513360371669-4a0eb51e8ae2',
            'https://images.unsplash.com/photo-1478098711619-69891b0ec21a',
        ],
        'dog': [
            'https://images.unsplash.com/photo-1633722715463-d30628519e1a',
            'https://images.unsplash.com/photo-1611003228941-98852ba62227',
            'https://images.unsplash.com/photo-1558788353-f76d92427f16',
            'https://images.unsplash.com/photo-1601758228578-851cda313e11',
            'https://images.unsplash.com/photo-1587300003388-59208cc962cb',
        ],
        'fox': [
            'https://images.unsplash.com/photo-1434694686742-92029fba1ee3',
            'https://images.unsplash.com/photo-1432405972618-c60b0225b8f9',
            'https://images.unsplash.com/photo-1506361197048-46a72bb97d31',
        ],
        'duck': [
            'https://images.unsplash.com/photo-1444464666175-1cff627ceab26',
            'https://images.unsplash.com/photo-1444989908331-a149ce67b396',
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19',
        ],
        'rabbit': [
            'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4',
            'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4',
            'https://images.unsplash.com/photo-1585110396000-c9ffd4d4b3f4',
        ],
        'raccoon': [
            'https://images.unsplash.com/photo-1567270762171-79799e56aea1',
            'https://images.unsplash.com/photo-1567270762171-79799e56aea1',
            'https://images.unsplash.com/photo-1567270762171-79799e56aea1',
        ],
        'owl': [
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
        ],
        'penguin': [
            'https://images.unsplash.com/photo-1551629146-8d3d89e68da0',
            'https://images.unsplash.com/photo-1551629146-8d3d89e68da0',
            'https://images.unsplash.com/photo-1551629146-8d3d89e68da0',
        ],
        'panda': [
            'https://images.unsplash.com/photo-1525382455947-f319bc05fb35',
            'https://images.unsplash.com/photo-1525382455947-f319bc05fb35',
            'https://images.unsplash.com/photo-1525382455947-f319bc05fb35',
        ],
        'koala': [
            'https://images.unsplash.com/photo-1459262838948-3e2de6c3638f',
            'https://images.unsplash.com/photo-1459262838948-3e2de6c3638f',
            'https://images.unsplash.com/photo-1459262838948-3e2de6c3638f',
        ],
        'sloth': [
            'https://images.unsplash.com/photo-1551324894-4f4f1a7f0d6e',
            'https://images.unsplash.com/photo-1551324894-4f4f1a7f0d6e',
            'https://images.unsplash.com/photo-1551324894-4f4f1a7f0d6e',
        ],
        'hedgehog': [
            'https://images.unsplash.com/photo-1539571696357-5a69c006ae30',
            'https://images.unsplash.com/photo-1539571696357-5a69c006ae30',
            'https://images.unsplash.com/photo-1539571696357-5a69c006ae30',
        ],
        'otter': [
            'https://images.unsplash.com/photo-1591229728215-2a83dbd60066',
            'https://images.unsplash.com/photo-1591229728215-2a83dbd60066',
            'https://images.unsplash.com/photo-1591229728215-2a83dbd60066',
        ],
        'squirrel': [
            'https://images.unsplash.com/photo-1446824653969-c8398aa337df',
            'https://images.unsplash.com/photo-1446824653969-c8398aa337df',
            'https://images.unsplash.com/photo-1446824653969-c8398aa337df',
        ],
        'deer': [
            'https://images.unsplash.com/photo-1484406566174-9da000fda645',
            'https://images.unsplash.com/photo-1484406566174-9da000fda645',
            'https://images.unsplash.com/photo-1484406566174-9da000fda645',
        ],
        'bear': [
            'https://images.unsplash.com/photo-1528127269029-c3ee1f0b2c14',
            'https://images.unsplash.com/photo-1528127269029-c3ee1f0b2c14',
            'https://images.unsplash.com/photo-1528127269029-c3ee1f0b2c14',
        ],
        'wolf': [
            'https://images.unsplash.com/photo-1501706362039-c06b2d715385',
            'https://images.unsplash.com/photo-1501706362039-c06b2d715385',
            'https://images.unsplash.com/photo-1501706362039-c06b2d715385',
        ],
        'eagle': [
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
            'https://images.unsplash.com/photo-1540573133985-87b6da97af72',
        ],
        'dolphin': [
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0',
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0',
            'https://images.unsplash.com/photo-1505142468610-359e7d316be0',
        ],
    }

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        self.session = session
        self.cat_api_key = os.getenv('CATS_API_KEY', '')
        self.dog_api_key = os.getenv('DOGS_API_KEY', '')

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self) -> None:
        """Close session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def get_cat_image(self) -> Optional[str]:
        """Get cat image with fallback"""
        try:
            session = await self.get_session()
            
            # Try primary API
            url = 'https://api.thecatapi.com/v1/images/search'
            headers = {}
            if self.cat_api_key:
                headers['x-api-key'] = self.cat_api_key
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and len(data) > 0:
                        return data[0].get('url')
        except Exception as e:
            print(f"Cat API error: {e}")
        
        # Fallback to cached image
        return random.choice(self.FALLBACK_IMAGES['cat'])

    async def get_dog_image(self) -> Optional[str]:
        """Get dog image with fallback"""
        try:
            session = await self.get_session()
            
            # Try primary API
            url = 'https://api.thedogapi.com/v1/images/search'
            headers = {}
            if self.dog_api_key:
                headers['x-api-key'] = self.dog_api_key
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and len(data) > 0:
                        return data[0].get('url')
        except Exception as e:
            print(f"Dog API error: {e}")
        
        # Fallback to cached image
        return random.choice(self.FALLBACK_IMAGES['dog'])

    async def get_fox_image(self) -> Optional[str]:
        """Get fox image with fallback"""
        try:
            session = await self.get_session()
            async with session.get('https://randomfox.ca/floof/', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and 'image' in data:
                        return data['image']
        except Exception as e:
            print(f"Fox API error: {e}")
        
        return random.choice(self.FALLBACK_IMAGES['fox'])

    async def get_duck_image(self) -> Optional[str]:
        """Get duck image with fallback"""
        try:
            session = await self.get_session()
            async with session.get('https://random-d.uk/api/random', timeout=aiohttp.ClientTimeout(total=5)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and 'url' in data:
                        return data['url']
        except Exception as e:
            print(f"Duck API error: {e}")
        
        return random.choice(self.FALLBACK_IMAGES['duck'])

    def get_static_image(self, animal: str) -> str:
        """Get static fallback image for any animal"""
        if animal in self.FALLBACK_IMAGES:
            return random.choice(self.FALLBACK_IMAGES[animal])
        # Generic fallback
        return 'https://images.unsplash.com/photo-1446824653969-c8398aa337df'
