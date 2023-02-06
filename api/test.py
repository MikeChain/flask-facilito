import unittest
from app import create_app
from app.models.task import insert_tasks
from config import config
from app import db
import json


class TestApi(unittest.TestCase):
    def setUp(self):
        environment = config['tests']
        self.app = create_app(environment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'

        with self.app.app_context():
            insert_tasks()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_one_equals_one(self):
        self.assertEqual(1, 1)

    def test_get_all_tasks(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)

    def test_get_first_task(self):
        new_path = f'{self.path}/1'
        response = self.client.get(
            path=new_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode('utf-8'))
        task_id = data['data']['id']

        self.assertEqual(task_id, 1)

    def test_get_unexistent_task(self):
        new_path = f'{self.path}/30'
        response = self.client.get(
            path=new_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
