from unittest import TestCase

from services.deduplication.deduplication_result import DeduplicationResult
from services.deduplication.deduplicator import DeduplicationException, Deduplicator


class DeduplicationTest(TestCase):
    def setUp(self):
        self.dedup = Deduplicator()

    def test_create_list_string(self):
        self.assertEqual(
            "1. article1\n2. article2",
            self.dedup._create_article_list_string(["article1", "article2"]),
        )
        self.assertEqual("", self.dedup._create_article_list_string([]))

    def test_create_result_from_response(self):
        self.assertEqual(
            DeduplicationResult([1, 2, 3], [[4, 7, 8], [5, 6]]),
            self.dedup._construct_result_from_response(
                '{"unique":[1,2,3], "duplicates_0":[4,7,8], "duplicates_1":[5,6]}',
            ),
        )
