from datetime import datetime

from repository.scheduleDB_test import ScheduleDB


class ScheduleService:
    @staticmethod
    def create_schedule(user_id, work_date, start_time, end_time, title, note):
        if not user_id or not work_date or not start_time or not end_time or not title:
            raise ValueError("Thieu du lieu bat buoc")

        try:
            start_dt = datetime.strptime(f"{work_date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{work_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Sai dinh dang ngay gio, dung YYYY-MM-DD va HH:MM")

        if start_dt >= end_dt:
            raise ValueError("Gio bat dau phai nho hon gio ket thuc")

        if ScheduleDB.has_conflict(user_id, work_date, start_time, end_time):
            raise ValueError("Lich bi trung voi ca lam khac")

        schedule_id = ScheduleDB.create_schedule(
            user_id, work_date, start_time, end_time, title, note
        )
        return schedule_id

    @staticmethod
    def get_schedules(user_id):
        if not user_id:
            raise ValueError("Thieu user_id")

        schedules = ScheduleDB.get_schedules_by_user(user_id)
        return [
            {
                "id": schedule.get_id(),
                "user_id": schedule.get_user_id(),
                "work_date": str(schedule.get_work_date()),
                "start_time": str(schedule.get_start_time()),
                "end_time": str(schedule.get_end_time()),
                "title": schedule.get_title(),
                "note": schedule.get_note(),
            }
            for schedule in schedules
        ]
