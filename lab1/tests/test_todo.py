import unittest
from src.todo import TodoList

class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.todo_list = TodoList()

    def test_add_task(self):
        self.todo_list.add_task("Task 1")
        self.assertIn("Task 1", self.todo_list.get_active_tasks())

    def test_complete_task(self):
        self.todo_list.add_task("Task 1")
        self.todo_list.complete_task("Task 1")

        self.assertNotIn("Task 1", self.todo_list.get_active_tasks())
        self.assertIn("Task 1", self.todo_list.get_completed_tasks())

    def test_get_active_tasks(self):
        self.todo_list.add_task("Task 1")
        self.todo_list.add_task("Task 2")

        active_tasks = self.todo_list.get_active_tasks()
        self.assertEqual(active_tasks, ["Task 1", "Task 2"])

    def test_get_completed_tasks(self):
        self.todo_list.add_task("Task 1")
        self.todo_list.complete_task("Task 1")

        completed_tasks = self.todo_list.get_completed_tasks()
        self.assertEqual(completed_tasks, ["Task 1"])

    def test_complete_task_not_in_active_list(self):
        self.todo_list.add_task("Task 1")
        self.todo_list.complete_task("Task 1")
        self.todo_list.complete_task("Non-existent task")

        self.assertNotIn("Non-existent task", self.todo_list.get_completed_tasks())
        self.assertNotIn("Non-existent task", self.todo_list.get_active_tasks())

if __name__ == "__main__":
    unittest.main()