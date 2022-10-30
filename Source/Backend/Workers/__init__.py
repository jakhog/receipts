from asyncio import CancelledError, create_task, gather
from hypercorn.logging import Logger

from ..Config import Configuration

from .OCR import OCRWorker

class Workers:
    def __init__(self, config: Configuration, logger: Logger):
        self.config = config
        self.ocr = OCRWorker(config, logger)

    async def process_startup(self, _scope, _event):
        print('Starting workers')
        self.tasks = [
            create_task(self.ocr.run()),
        ]

    async def process_shutdown(self, _scope, _event):
        print('Stopping workers')
        try:
            group = gather(*self.tasks, return_exceptions=True)
            group.cancel()
            await group
        except CancelledError:
            pass
