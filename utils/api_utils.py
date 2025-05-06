import asyncio

class RateLimiter:
    """
    A utility class to enforce rate limits for API calls
    """
    def __init__(self, rate_limit_per_minute: int):
        self.rate_limit = rate_limit_per_minute
        self.tokens = rate_limit_per_minute
        self.last_refill = asyncio.get_event_loop().time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquire a token to make an API call, waiting if necessary
        """
        async with self.lock:
            await self._refill()
            if self.tokens <= 0:
                # Calculate time until next token is available
                refill_time = 60 / self.rate_limit
                await asyncio.sleep(refill_time)
                await self._refill()
            
            self.tokens -= 1

    async def _refill(self):
        """
        Refill tokens based on elapsed time
        """
        now = asyncio.get_event_loop().time()
        elapsed = now - self.last_refill
        
        # Calculate how many tokens to add based on elapsed time
        new_tokens = int(elapsed * (self.rate_limit / 60))
        if new_tokens > 0:
            self.tokens = min(self.tokens + new_tokens, self.rate_limit)
            self.last_refill = now
