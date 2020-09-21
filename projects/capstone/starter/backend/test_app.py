import unittest
from datetime import date
from dotenv import load_dotenv

load_dotenv('.env_test')
from flask import jsonify
from app import app
from shared.models import Artist, Movie, Role
import json


class BasicTests(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    def tearDown(self) -> None:
        pass

    def test_00_index_success(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))

    # region testing artists
    def test_01_get_artists_list_success(self):
        response = self.app.get('/artists/')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_02_get_artists_names_success(self):
        response = self.app.get('/artists/names')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_03_get_artist_not_found(self):
        response = self.app.get('/artists/9999999999')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 404)
        self.assertFalse(data.get('success'))

    def test_04_get_artist_success(self):
        response = self.app.get('/artists/1')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_05_delete_artist_for_assistant_role_not_permitted(self):
        response = self.app.delete('/artists/1?role=assistant')
        self.assertEqual(response.status_code, 403)

    def test_06_delete_artist_for_director_role_not_found(self):
        response = self.app.delete('/artists/9999999999?role=director')
        self.assertEqual(response.status_code, 404)

    def test_07_delete_artist_for_director_role_success(self):
        response = self.app.delete('/artists/1?role=director')
        self.assertEqual(response.status_code, 200)
        artist = Artist.query.get(1)
        self.assertIsNone(artist)
        artist = Artist(1,'Liu Yifei',33,'Female','Liu Yifei ( born An Feng; August 25, 1987) is a popular Chinese-American actress, model and singer. She was born in China and moved to the United States when she was 11.','https://walter.trakt.tv/images/people/000/016/108/headshots/thumb/5d54607292.jpg.webp')
        artist.insert()
        role = Role(1, 1, 1, 'temp')
        role.insert()

    def test_08_delete_artist_for_producer_role_not_found(self):
        response = self.app.delete('/artists/9999999999?role=producer')
        self.assertEqual(response.status_code, 404)

    def test_09_delete_artist_for_producer_role_success(self):
        response = self.app.delete('/artists/1?role=producer')
        self.assertEqual(response.status_code, 200)
        artist = Artist.query.get(1)
        self.assertIsNone(artist)
        artist = Artist(1,'Liu Yifei',33,'Female','Liu Yifei ( born An Feng; August 25, 1987) is a popular Chinese-American actress, model and singer. She was born in China and moved to the United States when she was 11.','https://walter.trakt.tv/images/people/000/016/108/headshots/thumb/5d54607292.jpg.webp')
        artist.insert()
        role = Role(1, 1, 1, 'temp')
        role.insert()

    def test_10_new_artist_form_submission_for_assistant_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/artists/new?role=assistant')
            self.assertEqual(response.status_code, 403)

    def test_11_new_artist_form_submission_for_director_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/artists/new?role=director', data={})
            self.assertEqual(response.status_code, 400)

    def test_12_new_artist_form_submission_for_director_role_success(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_insert'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_insert.com'
            data = artist.format()
            response = self.app.post('/artists/new?role=director', data=jsonify(data).data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            artist = Artist.query.filter_by(name='test_insert').first()
            self.assertIsNotNone(artist)
            self.assertGreater(artist.id, 14)  # last record after seeded data

    def test_13_new_artist_form_submission_for_producer_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/artists/new?role=producer')
            self.assertEqual(response.status_code, 400)

    def test_14_new_artist_form_submission_for_producer_role_success(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_insert'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_insert.com'
            data = artist.format()
            response = self.app.post('/artists/new?role=producer', data=jsonify(data).data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            artist = Artist.query.filter_by(name='test_insert').first()
            self.assertIsNotNone(artist)
            self.assertGreater(artist.id, 14)  # last record after seeded data

    def test_15_edit_artist_form_submission_for_assistant_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/artists/edit/1?role=assistant')
            self.assertEqual(response.status_code, 403)

    def test_16_edit_artist_form_submission_for_director_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/artists/edit/1?role=director')
            self.assertEqual(response.status_code, 400)

    def test_17_edit_artist_form_submission_for_director_role_not_found(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_edit'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_edit.com'
            response = self.app.post('/artists/edit/9999999999?role=director', data=jsonify(artist.format()).data)
            self.assertEqual(response.status_code, 404)

    def test_18_edit_artist_form_submission_for_director_role_success(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_edit'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_edit.com'
            response = self.app.post('/artists/edit/1?role=director', data=jsonify(artist.format()).data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            modified_artist = Artist.query.get(1)
            self.assertIsNotNone(artist)
            self.assertEqual(modified_artist.id, 1)  # last record after seeded data
            self.assertEqual(modified_artist.name, artist.name)
            self.assertEqual(modified_artist.age, artist.age)
            self.assertEqual(modified_artist.gender, artist.gender)
            self.assertEqual(modified_artist.image, artist.image)

    def test_19_edit_artist_form_submission_for_producer_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/artists/edit/1?role=producer')
            self.assertEqual(response.status_code, 400)

    def test_20_edit_artist_form_submission_for_producer_role_not_found(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_edit'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_edit.com'
            response = self.app.post('/artists/edit/9999999999?role=producer', data=jsonify(artist.format()).data, follow_redirects=True)
            self.assertEqual(response.status_code, 404)

    def test_21_edit_artist_form_submission_for_producer_role_success(self):
        with app.test_request_context():
            artist = Artist()
            artist.name = 'test_edit'
            artist.age = 33
            artist.gender = 'Male'
            artist.image = 'http://test_edit.com'
            response = self.app.post('/artists/edit/1?role=producer', data=jsonify(artist.format()).data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            modicfied_artist = Artist.query.get(1)
            self.assertIsNotNone(modicfied_artist)
            self.assertEqual(modicfied_artist.id, 1)  # last record after seeded data
            self.assertEqual(modicfied_artist.name, artist.name)
            self.assertEqual(modicfied_artist.age, artist.age)
            self.assertEqual(modicfied_artist.gender, artist.gender)
            self.assertEqual(modicfied_artist.image, artist.image)
    # endregion

    # region testing movies
    def test_22_get_movies_list_success(self):
        response = self.app.get('/movies', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_23_get_movies_names_success(self):
        response = self.app.get('/movies/names')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data is not None)

    def test_24_get_movies_not_found(self):
        response = json.loads(self.app.get('/movies/9999999999').data)
        self.assertEqual(response.get('status_code'), 404)
        self.assertFalse(response.get('success'))
        self.assertTrue(response.get('message') is not None)

    def test_25_get_movies_success(self):
        response = self.app.get('/movies/1')
        self.assertEqual(response.status_code, 200)

    def test_26_delete_movies_for_assistant_role_not_permitted(self):
        response = self.app.delete('/movies/9999999999?role=assistant')
        self.assertEqual(response.status_code, 403)

    def test_27_delete_movies_for_director_role_not_permitted(self):
        response = self.app.delete('/movies/9999999999?role=director')
        self.assertEqual(response.status_code, 403)

    def test_28_delete_movies_for_producer_role_not_found(self):
        response = self.app.delete('/movies/9999999999?role=producer')
        self.assertEqual(response.status_code, 404)

    def test_29_delete_movies_for_producer_role_success(self):
        response = self.app.delete('/movies/1?role=producer')
        self.assertEqual(response.status_code, 200)
        movie = Movie.query.get(1)
        self.assertIsNone(movie)
        movie = Movie(1,'Mulan',date(2020, 8, 4),'When the Emperor of China issues a decree that one man per family must serve in the Imperial Chinese Army to defend the country from Huns, Hua Mulan, the eldest daughter of an honored warrior, steps in to take the place of her ailing father. She is spirited, determined and quick on her feet. Disguised as a man by the name of Hua Jun, she is tested every step of the way and must harness her innermost strength and embrace her true potential.','https://walter.trakt.tv/images/movies/000/218/005/posters/thumb/95f91d6351.jpg.webp')
        movie.insert()
        role = Role(1, 1, 1, 'temp')
        role.insert()

    def test_30_new_movie_form_submission_for_assistant_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/movies/new?role=assistant')
            self.assertEqual(response.status_code, 403)

    def test_31_new_movie_form_submission_for_director_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/movies/new?role=director')
            self.assertEqual(response.status_code, 403)

    def test_32_new_movie_form_submission_for_producer_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/movies/new?role=producer')
            self.assertEqual(response.status_code, 400)

    def test_33_new_movies_form_submission_for_producer_role_success(self):
        with app.test_request_context():
            movie = Movie()
            movie.name = 'test_insert'
            movie.release_date = date.today()
            movie.image = 'http://test_insert.com'
            response = self.app.post('/movies/new?role=producer', data=jsonify(movie.format()).data)
            self.assertEqual(response.status_code, 200)
            movie = Movie.query.filter_by(name='test_insert').first()
            self.assertIsNotNone(movie)
            self.assertGreater(movie.id, 10)  # last record after seeded data

    def test_34_edit_movie_form_submission_for_assistant_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/movies/edit/1?role=assistant')
            self.assertEqual(response.status_code, 403)

    def test_35_edit_movie_form_submission_for_director_role_not_permitted(self):
        with app.test_request_context():
            response = self.app.post('/movies/edit/1?role=director')
            self.assertEqual(response.status_code, 403)

    def test_36_edit_movie_form_submission_for_producer_role_not_valid(self):
        with app.test_request_context():
            response = self.app.post('/movies/edit/1?role=producer')
            self.assertEqual(response.status_code, 400)

    def test_37_edit_movie_form_submission_for_producer_role_not_found(self):
        with app.test_request_context():
            movie = Movie()
            movie.name = 'test_edit'
            movie.release_date = date.today()
            movie.image = 'http://test_edit.com'
            response = self.app.post('/movies/edit/9999999999?role=producer', data=jsonify(movie.format()).data)
            self.assertEqual(response.status_code, 404)

    def test_38_edit_movie_form_submission_for_producer_role_success(self):
        with app.test_request_context():
            movie = Movie()
            movie.name = 'test'
            movie.release_date = date.today()
            movie.image = 'http://test.com'
            response = self.app.post('/movies/edit/1?role=producer', data=jsonify(movie.format()).data)
            self.assertEqual(response.status_code, 200)
            modified_movie = Movie.query.get(1)
            self.assertIsNotNone(modified_movie)
            self.assertEqual(modified_movie.id, 1)  # last record after seeded data
            self.assertEqual(modified_movie.name, movie.name)
            self.assertEqual(modified_movie.release_date, movie.release_date)
            self.assertEqual(modified_movie.image, movie.image)
    # endregion

    # region testing roles
    def test_39_get_roles_list(self):
        response = self.app.get('/roles/')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_40_get_role_not_found(self):
        response = self.app.get('/roles/9999999999')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 404)
        self.assertFalse(data.get('success'))

    def test_41_get_role_success(self):
        response = self.app.get('/roles/1')
        data = json.loads(response.data)
        self.assertEqual(data.get('status_code'), 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('data'))

    def test_42_delete_roles_for_assistant_role_not_permitted(self):
        response = self.app.delete('/roles/9999999999?role=assistant')
        self.assertEqual(response.status_code, 403)

    def test_43_delete_roles_for_director_role_not_found(self):
        response = self.app.delete('/roles/9999999999?role=director')
        self.assertEqual(response.status_code, 404)

    def test_44_delete_roles_for_director_role_success(self):
        response = self.app.delete('/roles/1?role=director')
        self.assertEqual(response.status_code, 200)
        role = Role.query.get(1)
        self.assertIsNone(role)
        role = Role(role_id=1, artist_id=1, movie_id=1, character='temp')
        role.insert()

    def test_45_delete_roles_for_producer_role_not_found(self):
        response = self.app.delete('/movies/9999999999?role=producer')
        self.assertEqual(response.status_code, 404)

    def test_46_delete_roles_for_producer_role_success(self):
        response = self.app.delete('/roles/1?role=producer')
        self.assertEqual(response.status_code, 200)
        role = Role.query.get(1)
        self.assertIsNone(role)
        role = Role(role_id=1, artist_id=1, movie_id=1, character='temp')
        role.insert()

    # endregion



if __name__ == '__main__':
    unittest.main()
