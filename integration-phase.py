import asyncio
import os
import shutil
import unittest
from urllib import request
from xenocanto import metadata, download, gen_meta, purge, delete

# stop asynio close messages
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport

def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper

_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)


def main():
    # asyncio.run(download(['gen:Otis']))
    # asyncio.run(download(['Kiwi']))
    asyncio.run(download(['Anthornis melanura']))
    # self.assertTrue(os.path.exists('dataset/metadata/gen_Otis/page1.json'))
    # self.assertTrue(os.path.exists('dataset/audio/GreatBustard/'
    #                                '459281.mp3'))


if __name__ == "__main__":
   main()
