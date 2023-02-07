import unittest
from app import create_app
from app.models.task import insert_tasks
from config import config
from app import db
import json


class TestApi(unittest.TestCase):
    @staticmethod
    def get_task_id(response):
        data = json.loads(response.data.decode('utf-8'))
        return data['data']['id']

    def setUp(self):
        environment = config['tests']
        self.app = create_app(environment)
        self.client = self.app.test_client()

        self.content_type = 'application/json'
        self.path = 'http://127.0.0.1:5000/api/v1/tasks'
        self.first_task_path = f'{self.path}/1'
        self.unexistent_task_path = f'{self.path}/1000'

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
        response = self.client.get(
            path=self.first_task_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        task_id = self.get_task_id(response)

        self.assertEqual(task_id, 1)

    def test_get_unexistent_task(self):
        response = self.client.get(
            path=self.unexistent_task_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        data = {
            "title": "nueva tarea",
            "description": "Nueva description",
            "deadline": "2023-02-16 12:00:00"
        }

        response = self.client.post(path=self.path, data=json.dumps(
            data), content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        t = self.get_task_id(response)
        self.assertEqual(t, 3)

    def test_create_error(self):
        data = {
        }

        response = self.client.post(path=self.path, data=json.dumps(
            data), content_type=self.content_type)
        self.assertEqual(response.status_code, 400)

    def test_update_task(self):
        new_title = "nuevo title"
        data = {"title": new_title}

        response = self.client.put(path=self.first_task_path, data=json.dumps(
            data), content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        title = data['data']['title']

        self.assertEqual(title, new_title)

    def test_delete_task(self):
        response = self.client.delete(
            path=self.first_task_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            path=self.first_task_path, content_type=self.content_type)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
