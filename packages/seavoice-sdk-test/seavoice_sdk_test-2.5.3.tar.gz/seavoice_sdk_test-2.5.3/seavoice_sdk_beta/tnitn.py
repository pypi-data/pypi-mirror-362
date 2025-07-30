"""Tools for Text Normalisation and Inverse Text Normalisation"""

import asyncio
import json
import os

import websockets

from seavoice_sdk_beta.logger import default_logger

logger = default_logger


class ITNClient:
    def __init__(self, itn_host_url: str, lang: str):
        if lang.lower().startswith("zh"):
            self.itn_url = f"{itn_host_url}/zh-TW"
        elif lang.lower().startswith("en"):
            self.itn_url = f"{itn_host_url}/en-XX"
        else:
            raise Exception(f"{lang} not supported for ITN.")
        self.itn_results = asyncio.Queue()

    async def connect(self):
        self.websocket = await websockets.connect(self.itn_url)  # type: ignore
        asyncio.create_task(self._receive_results())
        logger.debug(f"Established connection to ITN server at {self.itn_url}")

    async def _receive_results(self):
        async for message in self.websocket:
            itn_result = json.loads(message)
            await self.itn_results.put(itn_result)
            logger.debug("Received result from ITN server.")

    async def send_text(self, text: str, is_final: bool, is_batch: bool = False):
        await self.websocket.send(json.dumps({"text": text, "is_final": is_final, "is_batch": is_batch}))
        logger.debug("Sent text to ITN server.")

    async def get_oldest_itn_result(self) -> str:
        result = await asyncio.wait_for(self.itn_results.get(), timeout=int(os.getenv("ITN_TIMEOUT", 5)))
        logger.debug("Obtained ITN result from queue.")
        return result

    async def close(self):
        await self.websocket.close()
        logger.debug("ITN client connection closed.")
