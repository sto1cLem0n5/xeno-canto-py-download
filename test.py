import asyncio
import os
import shutil
import unittest
from urllib import request
from xenocanto import metadata, download, gen_meta, purge, delete


# TODO:
#   [ ] Test resuming a download after interrupt
class TestCases(unittest.TestCase):

    # Check if connection to the API can be established
    def test_conn(self):
        url = 'https://www.xeno-canto.org/api/2/recordings?query=cnt:any'
        status = request.urlopen(url).getcode()
        self.assertEqual(status, 200)

    # Checks if metadata is successfully downloaded into the expected
    # folder structure
    def test_metadata(self):
        metadata(['Bearded Bellbird', 'q:A'])
        self.assertTrue(os.path.exists
                        ('dataset/metadata/BeardedBellbirdq_A/page1.json'))

    # Checks if audio files are downloaded into the correct directory
    def test_download(self):
        asyncio.run(download(['gen:Otis']))
        self.assertTrue(os.path.exists('dataset/metadata/gen_Otis/page1.json'))
        self.assertTrue(os.path.exists('dataset/audio/GreatBustard/'
                                       '459281.mp3'))

    # Check if purge is deleting folders based on file count
    def test_purge(self):
        asyncio.run(download(['gen:Otis']))
        asyncio.run(download(['Bearded Bellbird', 'q:A', 'cnt:Brazil']))
        purge(7)
        b = self.assertFalse(os.path.exists('dataset/audio/GreatBustard/'))
        self.assertTrue(os.path.exists('dataset/audio/BeardedBellbird/'))
        asyncio.sleep(.25)
        return b

    # Check if metadata is being correctly generated for one
    # recording with metadata already saved
    def test_gen_meta_with_extra_metadata(self):
        metadata(['gen:Otis'])
        asyncio.run(download(['Bearded Bellbird', 'q:A', 'cnt:Brazil']))
        gen_meta()
        self.assertTrue(os.path.exists('dataset/metadata/library.json'))

    # Check if deleting files using multiple filters
    def test_delete(self):
        asyncio.run(download(['Bearded Bellbird', 'q:A', 'cnt:Brazil']))
        self.assertTrue(os.path.exists('dataset/audio/BeardedBellbird/'
                                       '493159.mp3'))
        self.assertTrue(os.path.exists('dataset/audio/BeardedBellbird/'
                                       '427845.mp3'))
        delete(['id:493159', 'id:427845'])
        self.assertFalse(os.path.exists('dataset/audio/BeardedBellbird/'
                                        '493159.mp3'))
        self.assertFalse(os.path.exists('dataset/audio/BeardedBellbird/'
                                        '427845.mp3'))

    # Check if deleting files from multiple folders
    def test_delete_multiple_species(self):
        asyncio.run(download(['Bearded Bellbird', 'q:A', 'cnt:Brazil']))
        self.assertTrue(os.path.exists('dataset/audio/BeardedBellbird/'
                                       '493159.mp3'))
        asyncio.run(download(['gen:Otis']))
        self.assertTrue(os.path.exists('dataset/audio/GreatBustard/'))
        # delete(['gen:Otis'])
        delete(['id:493159', 'gen:Otis'])
        self.assertFalse(os.path.exists('dataset/audio/BeardedBellbird/'
                                        '493159.mp3'))
        self.assertFalse(os.path.exists('dataset/audio/GreatBustard/'))

    # Check if metadata is being correctly generated when some metadata
    #  is saved and some must be retrieved from an API call
    def test_gen_meta_with_extra_tracks(self):
        path = metadata(['gen:Otis'])
        asyncio.run(download(['gen:Otis']))
        asyncio.run(download(['Bearded Bellbird', 'q:A', 'cnt:Brazil']))
        shutil.rmtree(path)
        gen_meta()
        self.assertTrue(os.path.exists('dataset/metadata/library.json'))

    # Removes files used in testing
    def tearDown(self):
        print(("TEAR_DOWN"))
        try:
            shutil.rmtree('dataset/')
        except OSError:
            pass

"""fix yelling at me error"""
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
"""fix yelling at me error end"""

def main():
    # test
    test = TestCases()
    # test.test_conn()
    # test.test_metadata()
    # test.test_download()
    # test.test_purge()
    # test.test_gen_meta_with_extra_metadata()
    # test.test_delete()
    # test.tearDown()
    # test.test_delete_multiple_species()
    # test.test_gen_meta_with_extra_tracks()
    test.tearDown()


if __name__ == "__main__":
   main()


