import { apiRequest } from "./api";

export interface Task {
  task_id: number;
  user_id: number;
  title: string;
  description: string;
  status: "pending" | "in_progress" | "completed";
  deadline: string;
  created_at: string;
  is_overdue: boolean;
}

export interface RegisterPayload {
  username: string;
  password: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface LoginResponse {
  token?: string;
  user_id?: number;
  message?: string;
}

export interface CreateTaskPayload {
  user_id: number;
  title: string;
  description: string;
  status: Task["status"];
  deadline: string;
  created_at: string;
  is_overdue: boolean;
}

export interface UpdateTaskPayload {
  task_id: number;
  user_id: number;
  title: string;
  description: string;
  status: Task["status"];
  deadline: string;
  created_at: string;
  is_overdue: boolean;
}

export interface DeleteTaskPayload {
  task_id: number;
  user_id: number;
}

export interface ListTasksPayload {
  user_id: number;
}

export interface ListByStatusPayload {
  user_id: number;
  status: Task["status"];
}

// auth

export const register = (payload: RegisterPayload) =>
  apiRequest<{ message: string }>("/api/auth/register", payload);

export const login = (payload: LoginPayload) =>
  apiRequest<LoginResponse>("/api/auth/login", payload);

// schedule
export const listTasks = (payload: ListTasksPayload) =>
  apiRequest<any>("/schedule/list", payload);

export const createTask = (payload: CreateTaskPayload) =>
  apiRequest<{ message: string; task?: Task }>("/schedule/create", payload);

export const updateTask = (payload: UpdateTaskPayload) =>
  apiRequest<{ message: string }>("/schedule/update", payload);

export const deleteTask = (payload: DeleteTaskPayload) =>
  apiRequest<{ message: string }>("/schedule/delete", payload);

export const listTasksByStatus = (payload: ListByStatusPayload) =>
  apiRequest<any>("/schedule/list-by-status", payload);

export const getOverdueTasks = (payload: ListTasksPayload) =>
  apiRequest<any>("/schedule/overdue", payload);