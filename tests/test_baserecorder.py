import unittest
from unittest import mock

from flumine.resources.recorder import BaseRecorder, RacingRecorder


class BaseRecorderTest(unittest.TestCase):

    def setUp(self):
        self.base_recorder = BaseRecorder()
        self.base_recorder._market_filter = mock.Mock()
        self.base_recorder._market_data_filter = mock.Mock()

    def test_init(self):
        assert self.base_recorder.name == 'BASE_RECORDER'

    @mock.patch('flumine.resources.recorder.BaseRecorder.process_market_book')
    @mock.patch('flumine.resources.recorder.BaseRecorder.market_book_parameters')
    def test_call(self, mock_market_book_parameters, mock_process_market_book):
        mock_market_book = mock.Mock()
        self.base_recorder(mock_market_book)

        mock_market_book_parameters.assert_called_with(mock_market_book)
        mock_process_market_book.assert_called_with(mock_market_book)

    def test_market_book_parameters(self):
        mock_market_book = mock.Mock()
        assert self.base_recorder.market_book_parameters(mock_market_book) is True

    def test_process_market_book(self):
        with self.assertRaises(NotImplementedError):
            mock_market_book = mock.Mock()
            self.base_recorder.process_market_book(mock_market_book)

    def test_market_filter(self):
        assert self.base_recorder.market_filter == self.base_recorder._market_filter.serialise

    def test_market_data_filter(self):
        assert self.base_recorder.market_data_filter == self.base_recorder._market_data_filter.serialise

    def test_str(self):
        assert str(self.base_recorder) == '<BASE_RECORDER>'


class RacingRecorderTest(unittest.TestCase):

    def setUp(self):
        self.in_play = True
        self.directory = ''
        self.base_recorder = RacingRecorder(self.in_play, self.directory)
        self.base_recorder._market_filter = mock.Mock()
        self.base_recorder._market_data_filter = mock.Mock()

    def test_init(self):
        assert self.base_recorder.name == 'RACING_RECORDER'
        assert self.base_recorder.in_play == self.in_play
        assert self.base_recorder.directory == self.directory

    def test_market_parameters(self):
        market_book = mock.Mock()
        market_book.status = 'OPEN'
        market_book.inplay = True

        assert self.base_recorder.market_book_parameters(market_book) is True