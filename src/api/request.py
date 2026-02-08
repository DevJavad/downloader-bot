from aiohttp import ClientSession, ClientTimeout
from typing import Optional, Literal, Union
import logging


logger = logging.getLogger(__name__)


class Request:
    def __init__(self, timeout: Optional[Union[int, float]] = 20):
        self.timeout = timeout
        self.session: Optional[ClientSession] = None

    async def connect(self):
        if self.session is None:
            timeout = ClientTimeout(self.timeout)
            self.session = ClientSession(timeout=timeout)

            logger.info("create a new connection, timeout: %s", self.timeout)

    async def disconnect(self):
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

            logger.info("close a connection")

    async def request(
        self,
        method: Literal["POST", "GET"],
        url: str,
        return_type: Literal["JSON", "TEXT", "BYTES"],
        payload: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Union[dict, None]:
        logger.info("URL: %s", url)
        try:
            async with self.session.request(
                method,
                url,
                data=payload,
                headers=headers
            ) as response:
                status = response.status
                logger.info("status response: %s", status)
                if status != 200:
                    return None
                if return_type == "JSON":
                    return await response.json()
                elif return_type == "TEXT":
                    return await response.text()
                elif return_type == "BYTES":
                    return await response.read()

        except Exception as error:
            logger.error("request error: %s", error)
            return None