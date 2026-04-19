from datetime import datetime

from repository.scheduleDB import ScheduleDB


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
        return [ScheduleService._build_schedule_response(schedule) for schedule in schedules]

    @staticmethod
    def get_schedules_by_status(user_id, status):
        if not user_id:
            raise ValueError("Thieu user_id")

        normalized_status = ScheduleService._normalize_status(status)
        schedules = ScheduleService.get_schedules(user_id)
        return [s for s in schedules if s["status"] == normalized_status]

    @staticmethod
    def get_overdue_schedules(user_id):
        if not user_id:
            raise ValueError("Thieu user_id")

        schedules = ScheduleService.get_schedules(user_id)
        return [s for s in schedules if s["status"] == "qua_han"]
     
    @staticmethod
    def update_schedule(schedule_id, user_id, work_date, start_time, end_time, title, note):
        if not schedule_id or not user_id or not work_date or not start_time or not end_time or not title:
            raise ValueError("Thieu du lieu bat buoc")
        try:
            start_dt = datetime.strptime(f"{work_date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{work_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Sai dinh dang ngay gio, dung YYYY-MM-DD va HH:MM")
        if start_dt >= end_dt:
            raise ValueError("Gio bat dau phai nho hon gio ket thuc")
        if ScheduleDB.has_conflict_excluding_id(schedule_id, user_id, work_date, start_time, end_time):
            raise ValueError("Lich bi trung voi ca lam khac")

        if ScheduleDB.update_schedule(schedule_id, user_id, work_date, start_time, end_time, title, note) == 0:
            raise ValueError("Khong tim thay lich hoac khong co quyen sua")
        return True

    @staticmethod
    def delete_schedule(schedule_id, user_id):
        if not schedule_id or not user_id:
            raise ValueError("Thieu du lieu bat buoc")

        if ScheduleDB.delete_schedule(schedule_id, user_id) == 0:
            raise ValueError("Khong tim thay lich hoac khong co quyen xoa")

        return True

# -----------------------------------------------------------------------------------------------------------------#


    @staticmethod
    def _parse_schedule_datetime(work_date, time_value):
        datetime_str = f"{work_date} {time_value}"
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        raise ValueError("Du lieu ngay gio trong DB khong hop le")

    @staticmethod
    def _build_schedule_response(schedule):
        now = datetime.now()
        start_dt = ScheduleService._parse_schedule_datetime(
            schedule.get_work_date(), schedule.get_start_time()
        )
        end_dt = ScheduleService._parse_schedule_datetime(
            schedule.get_work_date(), schedule.get_end_time()
        )

        status = "chua_bat_dau"
        if now > end_dt:
            status = "qua_han"
        elif start_dt <= now <= end_dt:
            status = "dang_dien_ra"

        return {
            "id": schedule.get_id(),
            "user_id": schedule.get_user_id(),
            "work_date": str(schedule.get_work_date()),
            "start_time": str(schedule.get_start_time()),
            "end_time": str(schedule.get_end_time()),
            "title": schedule.get_title(),
            "note": schedule.get_note(),
            "status": status,
        }

    @staticmethod
    def _normalize_status(status):
        if not status:
            raise ValueError("Thieu status")

        normalized = status.strip().lower()
        aliases = {
            "upcoming": "chua_bat_dau",
            "pending": "chua_bat_dau",
            "in_progress": "dang_dien_ra",
            "processing": "dang_dien_ra",
            "overdue": "qua_han",
            "late": "qua_han",
        }
        normalized = aliases.get(normalized, normalized)

        allowed = {"chua_bat_dau", "dang_dien_ra", "qua_han"}
        if normalized not in allowed:
            raise ValueError("Trang thai khong hop le")
        return normalized

    @staticmethod
    def get_schedules_by_status(user_id, status):
        if not user_id:
            raise ValueError("Thieu user_id")

        normalized_status = ScheduleService._normalize_status(status)
        schedules = ScheduleService.get_schedules(user_id)
        return [s for s in schedules if s["status"] == normalized_status]

    @staticmethod
    def get_overdue_schedules(user_id):
        if not user_id:
            raise ValueError("Thieu user_id")

        schedules = ScheduleService.get_schedules(user_id)
        return [s for s in schedules if s["status"] == "qua_han"]

