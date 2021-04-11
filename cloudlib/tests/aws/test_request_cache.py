
import unittest
from cloudtools.aws.cache import request_cache, use_request_cache, _get_global_request_cache


class RequestCacheTests(unittest.TestCase):

    @use_request_cache
    def test_request_cache_should_return_cached_value_for_parameter_keys(self):
        expected_data = {'data': 'entry'}
        count = 0

        @request_cache
        def get_data(query: str, limit: int, ascending: bool):
            nonlocal count
            count += 1
            return expected_data

        def handler(event, context):
            data = get_data('test', 2, True)
            self.assertEqual(data, expected_data)

            data = get_data('test', 2, True)
            self.assertEqual(data, expected_data)

        handler(None, None)

        cache = _get_global_request_cache()
        rq_cache = cache.get()

        self.assertIsNotNone(rq_cache)

        data = rq_cache.get(('get_data', 'test', 2, True))

        self.assertEqual(expected_data, data)

    def test_should_remove_request_cache_upon_exiting_context(self):

        @use_request_cache
        def handler(event, context):
            cache = _get_global_request_cache()
            self.assertIsNotNone(cache.get())

        handler(None, None)

        cache = _get_global_request_cache()

        self.assertIsNone(cache.get())
        self.assertFalse(cache._cache)

    def test_should_handle_multiple_request_caches(self):

        @request_cache
        def get_data(id: str):
            return {'data': id}

        @use_request_cache
        def handler1(event, context):
            data = get_data('1')
            self.assertEqual(data, {'data': '1'})
            self.assertEqual(data, {'data': '1'})
            data = get_data('2')
            self.assertEqual(data, {'data': '2'})
            data = get_data('2')
            self.assertEqual(data, {'data': '2'})

            cache = _get_global_request_cache()
            rq_cache = cache.get()
            self.assertCountEqual(rq_cache.cache, {
                ('get_data', '1'): {'data': '1'},
                ('get_data', '2'): {'data': '2'}
            })

        @use_request_cache
        def handler2(event, context):
            handler1(event, context)
            data = get_data('1')
            self.assertEqual(data, {'data': '1'})
            self.assertEqual(data, {'data': '1'})
            data = get_data('2')
            self.assertEqual(data, {'data': '2'})
            data = get_data('2')
            self.assertEqual(data, {'data': '2'})

            cache = _get_global_request_cache()
            rq_cache = cache.get()
            self.assertCountEqual(rq_cache.cache, {
                ('get_data', '1'): {'data': '1'},
                ('get_data', '2'): {'data': '2'}
            })

        handler2(None, None)

        cache = _get_global_request_cache()

        self.assertIsNone(cache.get())
        self.assertFalse(cache._cache)
