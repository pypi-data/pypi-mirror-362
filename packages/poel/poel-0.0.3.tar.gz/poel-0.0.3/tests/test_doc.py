import unittest

from poel.api.easydoc import parse_files


class TestTencent(unittest.TestCase):

    def setUp(self):
        self.api_key = "amaRp77baPsGnUB0nW07vi7a3eQqTX89"  # 免费领取：https://platform.easylink-ai.com/api-keys

    def test_doc(self):
        r = parse_files(api_key=self.api_key, file_path=r"test_files")
        print(r)
