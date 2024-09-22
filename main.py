import argparse
from datetime import datetime
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
  if not os.path.exists(TASKS_FILE):
      return []
  with open(TASKS_FILE, 'r') as file:
    return json.load(file)
  
def save_tasks(tasks):
  with open(TASKS_FILE, "w") as file:
    json.dump(tasks, file, indent=2)

def add_task(description):
  tasks = load_tasks()
  now = datetime.now().isoformat()
  task_id = len(tasks) + 1
  task = {
    "id": task_id,
    "description": description,
    "status": "todo",
    "createdAt": now,
    "updatedAt": now
  }
  tasks.append(task)
  save_tasks(tasks)
  print(f"Task added successfully (ID: {task_id})")


def task_exist(id):
    tasks = load_tasks()
    current_state = False
    exist = any(task['id'] == id for task in tasks)
    if exist:
      current_state = True
    return current_state

def delete_task(id):
  tasks = load_tasks()  
  exist = task_exist(id)

  if not exist:
    print("This task does not exist")
    return
  
  filtered_tasks = [task for task in tasks if task['id'] != id]
  save_tasks(filtered_tasks)
  print("Task successfully deleted")


def update_task(id, new_description):
  tasks = load_tasks()  
  exist = task_exist(id)
  now = datetime.now().isoformat()

  if not exist:
    print("This task does not exist")
    return
  
  for i in tasks:
    if i['id'] == id:
      i['description'] = new_description
      i['updatedAt'] = now
  save_tasks(tasks)
  print(f"Task with id:{id} successfully updated")


def mark_task(id, new_status):
  tasks = load_tasks()
  exist = task_exist(id)
  now = datetime.now().isoformat()

  if not exist:
    print("This task does not exist")
    return
  
  for i in tasks:
    if i['id'] == id:
      i['status'] = new_status
      i['updatedAt'] = now
      save_tasks(tasks)
      print(f"Task with id: {id} successfully marked as {new_status}")
      return

def list_tasks(status=None):
  tasks = load_tasks()
  filtered_tasks = tasks if not status else [task for task in tasks if task["status"] == status]
  for task in filtered_tasks:
    print(f"{task["id"]}: {task["description"]} - {task["status"]}")
  
def main():
  parser = argparse.ArgumentParser(description='Task tracker CLI')
  subparsers = parser.add_subparsers(dest='command')

  # Add task command
  parser_add = subparsers.add_parser('add', help='Add a new task')
  parser_add.add_argument('description', type=str, help='Description of the task')

  # Delete task
  parser_delete = subparsers.add_parser("delete", help="Delete an existing task")
  parser_delete.add_argument('id', type = int, help = 'task id')

  # update task
  parser_update = subparsers.add_parser("update", help="Update an existing task")
  parser_update.add_argument('id', type = int, help = 'task id')
  parser_update.add_argument('description', type=str, help='New description of the task')

  # mark task as in progress
  parser_mark_in_progress = subparsers.add_parser("mark-in-progress", help="Mark a task as in progress")
  parser_mark_in_progress.add_argument('id', type = int, help = 'task id')

  # mark task as done
  parser_mark_done = subparsers.add_parser("mark-done", help="Marked a task as done")
  parser_mark_done.add_argument('id', type = int, help = 'task id')

  # list tasks
  parser_list = subparsers.add_parser("list", help="List tasks")
  parser_list.add_argument("status", nargs="?", type=str, help="Filter task by status (todo, in-progress, done)")

  args = parser.parse_args()

  commands = {
    "add": lambda: add_task(args.description),
    "update": lambda: update_task(args.id, args.description),
    "delete": lambda: delete_task(args.id),
    "list": lambda: list_tasks(args.status),
    "mark-done": lambda: mark_task(args.id, "done"),
    "mark-in-progress": lambda: mark_task(args.id, "in-progress")
  }

  command_function = commands.get(args.command, lambda: parser.print_help())
  command_function()

if __name__ == '__main__':
  main()