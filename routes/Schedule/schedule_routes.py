from services.Schedule.schedule_service import ScheduleService


def create_schedule_route(request_body):
	user_id = request_body.get("user_id")
	work_date = request_body.get("work_date")
	start_time = request_body.get("start_time")
	end_time = request_body.get("end_time")
	title = request_body.get("title")
	note = request_body.get("note", "")

	try:
		schedule_id = ScheduleService.create_schedule(
			user_id, work_date, start_time, end_time, title, note
		)
		return {
			"status": 201,
			"message": "Them lich thanh cong",
			"schedule_id": schedule_id,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}


def list_schedules_route(request_body):
	user_id = request_body.get("user_id")

	try:
		schedules = ScheduleService.get_schedules(user_id)
		return {
			"status": 200,
			"message": "Lay danh sach lich thanh cong",
			"data": schedules,
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}


def update_schedule_route(request_body):
	schedule_id = request_body.get("schedule_id")
	user_id = request_body.get("user_id")
	work_date = request_body.get("work_date")
	start_time = request_body.get("start_time")
	end_time = request_body.get("end_time")
	title = request_body.get("title")
	note = request_body.get("note", "")

	try:
		ScheduleService.update_schedule(
			schedule_id, user_id, work_date, start_time, end_time, title, note
		)
		return {
			"status": 200,
			"message": "Cap nhat lich thanh cong",
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}


def delete_schedule_route(request_body):
	schedule_id = request_body.get("schedule_id")
	user_id = request_body.get("user_id")

	try:
		ScheduleService.delete_schedule(schedule_id, user_id)
		return {
			"status": 200,
			"message": "Xoa lich thanh cong",
		}
	except ValueError as e:
		return {"status": 400, "message": str(e)}
	except RuntimeError as e:
		return {"status": 500, "message": str(e)}
