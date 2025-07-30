from letterboxdpy.movie import Movie
from unittest.mock import MagicMock
import unittest


class TestMovie(unittest.TestCase):
    """Test suite for the Movie class."""

    def setUp(self):
        self.movie = Movie("v-for-vendetta")

    def test_movie_trailer(self):
        mock_dom = MagicMock()
        mock_dom.find.return_value = MagicMock(
            a=MagicMock(href='//www.youtube.com/embed/V5VGq23aZ-g?rel=0&wmode=transparent')
        )

        trailer_data = self.movie.movie_trailer(mock_dom)
        expected = {
            "id": "V5VGq23aZ-g",
            "link": "https://www.youtube.com/watch?v=V5VGq23aZ-g",
            "embed_url": "https://www.youtube.com/embed/V5VGq23aZ-g"
        }
        self.assertNotEqual(trailer_data, expected)

    def test_get_not_exists_banner_movie(self):
        instance = Movie("avatar-4")  # upcoming 2029
        data = instance.banner
        self.assertIsNone(data)

    def test_get_exists_banner_movie(self):
        data = self.movie.banner
        self.assertIsNotNone(data)

    def test_get_movie_title(self):
        data = self.movie.title
        self.assertEqual(data, "V for Vendetta")

    def test_get_movie_year(self):
        data = self.movie.year
        self.assertEqual(data, 2005)


if __name__ == '__main__':
    unittest.main()
