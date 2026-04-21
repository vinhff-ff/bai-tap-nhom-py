from services.Task.task_service import TaskService


def create_task_route(request_body):
	user_id = request_body.get("user_id")
	title = request_body.get("title")
	description = request_body.get("description", "")
	status = request_body.get("status", "pending")
	deadline = request_body.get("deadline")
	created_at = request_body.get("created_at")
	is_overdue = request_body.get("is_overdue", False)

	try:
		task_id = TaskService.create_task(
			user_id, title, description, status, deadline, created_at, is_overdue
		)
		return {
			"status": 201,
			"message": "Them task thanh cong",
			"task_id": task_id,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}


def update_task_route(request_body):
	task_id = request_body.get("task_id")
	user_id = request_body.get("user_id")
	title = request_body.get("title")
	description = request_body.get("description", "")
	status = request_body.get("status", "pending")
	deadline = request_body.get("deadline")
	is_overdue = request_body.get("is_overdue", False)

	try:
		TaskService.update_task(
			task_id, user_id, title, description, status, deadline, is_overdue
		)
		return {
			"status": 200,
			"message": "Cap nhat task thanh cong",
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}


def delete_task_route(request_body):
	task_id = request_body.get("task_id")
	user_id = request_body.get("user_id")

	try:
		TaskService.delete_task(task_id, user_id)
		return {
			"status": 200,
			"message": "Xoa task thanh cong",
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}


'''============================================================================================================='''

def list_tasks_route(request_body):
	user_id = request_body.get("user_id")

	try:
		tasks = TaskService.get_tasks(user_id)
		return {
			"status": 200,
			"message": "Lay danh sach task thanh cong",
			"data": tasks,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}


def list_tasks_by_status_route(request_body):
	user_id = request_body.get("user_id")
	status = request_body.get("status")

	try:
		tasks = TaskService.get_tasks_by_status(user_id, status)
		return {
			"status": 200,
			"message": "Loc task theo trang thai thanh cong",
			"data": tasks,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}


def overdue_tasks_route(request_body):
	user_id = request_body.get("user_id")

	try:
		tasks = TaskService.get_overdue_tasks(user_id)
		return {
			"status": 200,
			"message": "Lay danh sach task qua han thanh cong",
			"data": tasks,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
