from asyncio import sleep, to_thread
from hypercorn.logging import Logger
import os
from time import perf_counter
from PIL import Image
from pytesseract import image_to_data, Output

from ..Config import Configuration

class OCRWorker:
    def __init__(self, config: Configuration, logger: Logger):
        try:
            self.inbox_path = os.path.abspath(config.workers.ocr.inbox_path)
            os.makedirs(self.inbox_path, exist_ok=True)
        except Exception as error:
            raise Exception('Failed to create inbox: {}'.format(error))

        self.logger = logger

    async def run(self):
        await self.logger.info('Started OCR worker in path: %s', self.inbox_path)

        while True:
            await sleep(1)

            with os.scandir(self.inbox_path) as entries:
                for entry in entries:
                    path = os.path.relpath(entry.path, self.inbox_path)
                    if not entry.is_file(follow_symlinks=False):
                        await self.logger.warning('Found non-file "%s" in inbox, ignoring', path)
                    
                    await self.logger.debug('Processing "%s" from inbox', path)
                    started = perf_counter()
                    await to_thread(self._process_inbox_file, entry.path)
                    finished = perf_counter()
                    await self.logger.info('Processed "%s" from inbox, took %d seconds', path, finished-started)

    def _process_inbox_file(self, path):
        df = image_to_data(Image.open(path), output_type=Output.DATAFRAME)






