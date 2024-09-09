import argparse
from datetime import datetime
import json
import os

TASKS_FILE = "tasks.json"

concept_aquiles = """
  1 - VALIDATE IF THE FILE EXIST (IF NOT, CREATE AN EMPTY LIST AND RETURN IT) ✅
  2 - READ THE FILE TO KNOW OUR CURRENT TASKS ✅
  3 - SAVE THOSE TASKS IN A VARIABLE ✅
  4 - ADD OUR NEW TASK TO THE VARIABLE ✅
  5 - SAVE THE VARIABLE WITH LIST INTO THE FILE ✅
"""

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


delete_algorithm = """
1. llamarlos
2. iterar por todos y ver si existe
3. Si existe, borrarlo. Si no exite, dar feedback
4. mostrar la lista actualizada
"""

new_algo = """
 - load all tasks
 - iterate over all tasks to check if searched id exist or not
 - if id doesnt exist print an error
 - if id exists iterate again to filter
"""

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

def main():
  parser = argparse.ArgumentParser(description='Task tracker CLI')
  subparsers = parser.add_subparsers(dest='command')

  # Add task command
  parser_add = subparsers.add_parser('add', help='Add a new task')
  parser_add.add_argument('description', type=str, help='Description of the task')

  # Delete task
  parser_delete = subparsers.add_parser("delete", help="Delete an existing task")
  parser_delete.add_argument('id', type = int, help = 'task id')


  args = parser.parse_args()

  #print(args)

  if args.command == 'add':
    add_task(args.description)
  elif args.command == 'delete':
    delete_task(args.id)



if __name__ == '__main__':
  main()