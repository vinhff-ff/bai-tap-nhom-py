import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  Table,
  Modal,
  Form,
  Input,
  Select,
  DatePicker,
  Button,
  Popconfirm,
  message,
  Tooltip,
  Switch,
  Badge,
  Tag,
  Empty,
} from "antd";
import type { ColumnsType } from "antd/es/table";
import {
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  BellOutlined,
  ReloadOutlined,
  SearchOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  SyncOutlined,
  ExclamationCircleOutlined,
  CalendarOutlined,
  ThunderboltOutlined,
  CloseOutlined,
  LogoutOutlined,
  UserOutlined,
  PlusCircleOutlined,
} from "@ant-design/icons";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import {
  Task,
  listTasks,
  createTask,
  updateTask,
  deleteTask,
  getOverdueTasks,
  listTasksByStatus,
} from "./api/auth";
import AuthPage from "./page/Authpage";
import "./style/index.scss";

dayjs.extend(relativeTime);


interface AuthState {
  userId: number | null;
  username: string;
}

const getStoredAuth = (): AuthState => {
  const raw = localStorage.getItem("tf_user_id");
  const userId = raw ? Number(raw) : null;
  const username = localStorage.getItem("tf_user") ?? "";
  return { userId, username };
};

const clearAuth = () => {
  localStorage.removeItem("tf_user_id");
  localStorage.removeItem("tf_user");
};

interface NotifItem {
  id: number;
  title: string;
  desc: string;
  time: string;
}
type Status = Task["status"];
type StatusFilter = Status | "all";

const App: React.FC = () => {
  const [auth, setAuth] = useState<AuthState>(getStoredAuth);

  const isLoggedIn = auth.userId !== null && auth.userId > 0;

  const handleLoginSuccess = (userId: number, username: string) => {
    setAuth({ userId, username });
  };

  const handleLogout = () => {
    clearAuth();
    setAuth({ userId: null, username: "" });
    setTasks([]);
    setNotifications([]);
    message.success("Đã đăng xuất!");
  };

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [searchText, setSearchText] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");
  const [bellOpen, setBellOpen] = useState(false);
  const [notifications, setNotifications] = useState<NotifItem[]>([]);
  const [logoutConfirm, setLogoutConfirm] = useState(false);
  const [form] = Form.useForm();
  const bellRef = useRef<HTMLDivElement>(null);
  const [allTasks, setAllTasks] = useState<Task[]>([]);

  const USER_ID = auth.userId ?? 1;

  const fetchTasks = useCallback(async () => {
    if (!isLoggedIn) return;
    setLoading(true);
    try {
      const data = await listTasks({ user_id: USER_ID });
      const tasks = data.data || [];
      setAllTasks(tasks);
      setTasks(tasks);
    } catch {
      message.error("Không thể tải danh sách task!");
    } finally {
      setLoading(false);
    }
  }, [isLoggedIn, USER_ID]);

  const fetchOverdue = useCallback(async () => {
    if (!isLoggedIn) return;
    try {
      const data = await getOverdueTasks({ user_id: USER_ID });
      const tasks = data.data || [];
      if (Array.isArray(tasks) && tasks.length > 0) {
        setNotifications(
          tasks.map((t) => ({
            id: t.task_id,
            title: `Quá hạn: ${t.title}`,
            desc: `Deadline: ${dayjs(t.deadline).format("DD/MM/YYYY HH:mm")}`,
            time: dayjs(t.deadline).from(dayjs()),
          }))
        );
      } else {
        setNotifications([]);
      }
    } catch {

    }
  }, [isLoggedIn, USER_ID]);

  useEffect(() => {
    if (isLoggedIn) {
      fetchTasks();
      fetchOverdue();
    }
  }, [isLoggedIn, fetchTasks, fetchOverdue]);


  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (bellRef.current && !bellRef.current.contains(e.target as Node)) {
        setBellOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      const created_at = values.created_at
        ? dayjs(values.created_at).format("YYYY-MM-DD HH:mm")
        : "Chưa chọn";

      const deadline = values.deadline
        ? dayjs(values.deadline).format("YYYY-MM-DD HH:mm")
        : "Chưa chọn";

      if (editingTask) {
        await updateTask({
          task_id: editingTask.task_id,
          user_id: USER_ID,
          title: values.title,
          description: values.description,
          status: values.status,
          deadline,
          created_at,
          is_overdue: false,
        });
        message.success("Cập nhật task thành công!");
      } else {
        await createTask({
          user_id: USER_ID,
          title: values.title,
          description: values.description,
          status: values.status,
          deadline,
          created_at,
          is_overdue: false,
        });
        message.success("Tạo task mới thành công!");
      }

      setModalOpen(false);
      form.resetFields();
      setEditingTask(null);
      fetchTasks();
      fetchOverdue();
    } catch (err: unknown) {
      if (err instanceof Error) message.error(err.message);
    }
  };

  const handleDelete = async (task: Task) => {
    try {
      await deleteTask({ task_id: task.task_id, user_id: USER_ID });
      message.success("Đã xóa task!");
      fetchTasks();
      fetchOverdue();
    } catch {
      message.error("Xóa task thất bại!");
    }
  };

  const openEdit = (task: Task) => {
    setEditingTask(task);
    form.setFieldsValue({
      title: task.title,
      description: task.description,
      status: task.status,
      deadline: task.deadline ? dayjs(task.deadline) : null,
      is_overdue: task.is_overdue,
      created_at: task.created_at ? dayjs(task.created_at) : null,
    });
    setModalOpen(true);
  };

  const openCreate = () => {
    setEditingTask(null);
    form.resetFields();
    setModalOpen(true);
  };

  type Status = "pending" | "in_progress" | "completed";

  const statusConfig: Record<Status, { label: string; icon: React.ReactNode; cls: string }> = {
    pending: { label: "Chờ xử lý", icon: <ClockCircleOutlined />, cls: "status--pending" },
    in_progress: { label: "Đang xử lý", icon: <SyncOutlined spin />, cls: "status--progress" },
    completed: { label: "Hoàn thành", icon: <CheckCircleOutlined />, cls: "status--done" },
  };

  const StatusChip: React.FC<{ status: Status }> = ({ status }) => {
    const cfg = statusConfig[status];
    return (
      <span className={`status-chip ${cfg.cls}`}>
        {cfg.icon}
        <span>{cfg.label}</span>
      </span>
    );
  };

  const fetchTasksByStatus = useCallback(async (status: string) => {
    if (!isLoggedIn) return;

    setLoading(true);
    try {
      let res;

      if (status === "all") {
        res = await listTasks({ user_id: USER_ID });
        const data = res.data || [];

        setTasks(data);
        setAllTasks(data);
      } else {
        res = await listTasksByStatus({
          user_id: USER_ID,
          status: status as Task["status"],
        });

        const data = res.data || [];
        setTasks(data);
      }
    } catch {
      message.error("Không thể lọc task!");
    } finally {
      setLoading(false);
    }
  }, [isLoggedIn, USER_ID]);

  useEffect(() => {
    if (isLoggedIn) {
      fetchTasksByStatus(statusFilter);
    }
  }, [statusFilter, isLoggedIn, fetchTasksByStatus]);

  const total = allTasks.length;
  const pending = allTasks.filter((t) => t.status === "pending").length;
  const inProgress = allTasks.filter((t) => t.status === "in_progress").length;
  const overdue = allTasks.filter((t) => t.is_overdue).length;

  const columns: ColumnsType<Task> = [
    {
      title: "STT",
      key: "index",
      width: 53,
      render: (_: unknown, __: Task, index: number) => (
        <span className="col-index">{String(index + 1).padStart(2, "0")}</span>
      ),
    },
    {
      title: "Tiêu đề",
      dataIndex: "title",
      key: "title",
      render: (val: string, record: Task) => (
        <div className="col-title">
          <span>{val}</span>
          {record.is_overdue && (
            <Tag icon={<ExclamationCircleOutlined />} className="overdue-tag">
              Quá hạn
            </Tag>
          )}
        </div>
      ),
    },
    {
      title: "Mô tả",
      dataIndex: "description",
      key: "description",
      ellipsis: true,
      render: (val: string) => <span className="col-muted">{val}</span>,
    },
    {
      title: "Trạng thái",
      dataIndex: "status",
      key: "status",
      width: 148,
      render: (val: Task["status"]) => <StatusChip status={val as Status} />,
      filters: [
        { text: "Chờ xử lý", value: "pending" },
        { text: "Đang xử lý", value: "in_progress" },
        { text: "Hoàn thành", value: "completed" },
      ],
      onFilter: (value: unknown, record: Task) => record.status === value,
    },
    {
      title: "Ngày bắt đầu",
      dataIndex: "created_at",
      key: "created_at",
      width: 148,
      render: (val: string) => (
        <span className="col-muted col-sm">
          {val ? dayjs(val).format("DD/MM/YYYY HH:mm") : "—"}
        </span>
      ),
    },
    {
      title: "Deadline",
      dataIndex: "deadline",
      key: "deadline",
      width: 160,
      render: (val: string) => (
        <span className="col-deadline">
          <CalendarOutlined />
          {val ? dayjs(val).format("DD/MM/YYYY HH:mm") : "—"}
        </span>
      ),
      sorter: (a: Task, b: Task) => dayjs(a.deadline).unix() - dayjs(b.deadline).unix(),
    },
    {
      title: "hành động",
      key: "actions",
      width: 102,
      fixed: "right" as const,
      render: (_: unknown, record: Task) => (
        <div className="row-actions">
          <Tooltip title="Chỉnh sửa" placement="top">
            <button className="act-btn act-edit" onClick={() => openEdit(record)}>
              <EditOutlined style={{ color: 'blue' }} />
            </button>
          </Tooltip>
          <Popconfirm
            title="Xóa công việc này?"
            description="Hành động này không thể hoàn tác."
            onConfirm={() => handleDelete(record)}
            okText="Xóa"
            cancelText="Hủy"
            okButtonProps={{ danger: true, size: "small" }}
            cancelButtonProps={{ size: "small" }}
          >
            <Tooltip title="Xóa" placement="top">
              <button className="act-btn act-delete">
                <DeleteOutlined style={{ color: 'red' }} />
              </button>
            </Tooltip>
          </Popconfirm>
        </div>
      ),
    },
  ];


  if (!isLoggedIn) {
    return <AuthPage onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="shell">

      <header className="topbar">
        <div className="topbar__brand">
          <span className="topbar__brand-name">
            Sản phẩm nhóm 7 - Lập trình Python nâng cao
          </span>
        </div>

        <nav className="topbar__right">
          <span className="topbar__user">
            <UserOutlined />
            {auth.username}
          </span>

          <div className="bell-wrap" ref={bellRef}>
            <Badge count={notifications.length} size="small" offset={[-2, 2]}>
              <button
                className={`bell-btn ${bellOpen ? "bell-btn--on" : ""}`}
                onClick={() => setBellOpen((v) => !v)}
                aria-label="Thông báo"
              >
                <BellOutlined />
              </button>
            </Badge>

            {bellOpen && (
              <div className="notif-panel">
                <div className="notif-panel__head">
                  <span>Thông báo</span>
                  {notifications.length > 0 && (
                    <span className="notif-count">{notifications.length} quá hạn</span>
                  )}
                </div>
                {notifications.length === 0 ? (
                  <div className="notif-empty">
                    <CheckCircleOutlined />
                    <span>Không có thông báo</span>
                  </div>
                ) : (
                  <ul className="notif-list">
                    {notifications.map((n) => (
                      <li className="notif-item" key={n.id}>
                        <ExclamationCircleOutlined className="notif-item__icon" />
                        <div className="notif-item__body">
                          <p className="notif-item__title">{n.title}</p>
                          <p className="notif-item__desc">{n.desc}</p>
                        </div>
                        <span className="notif-item__time">{n.time}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>


          <Popconfirm
            title="Đăng xuất?"
            description="Bạn sẽ cần đăng nhập lại để tiếp tục."
            open={logoutConfirm}
            onConfirm={() => { setLogoutConfirm(false); handleLogout(); }}
            onCancel={() => setLogoutConfirm(false)}
            okText="Đăng xuất"
            cancelText="Hủy"
            okButtonProps={{ danger: true, size: "small" }}
            cancelButtonProps={{ size: "small" }}
            placement="bottomRight"
          >
            <Tooltip title="Đăng xuất" placement="bottom">
              <button
                className="bell-btn logout-btn"
                onClick={() => setLogoutConfirm(true)}
                aria-label="Đăng xuất"
              >
                <LogoutOutlined />
              </button>
            </Tooltip>
          </Popconfirm>
        </nav>
      </header>

      <main className="body">
        <div className="title-row">
          <div className="title-row__text">
            <h1>Quản lý công việc</h1>
            <p>Theo dõi và kiểm soát toàn bộ nhiệm vụ của bạn</p>
          </div>
          <div className="title-row__actions">
            <Tooltip title="Làm mới">
              <Button
                className="btn-ghost"
                icon={<ReloadOutlined />}
                onClick={fetchTasks}
                loading={loading}
              />
            </Tooltip>
            <button className="btn-primary" onClick={openCreate}>
              <PlusOutlined />
              Thêm công việc
            </button>
          </div>
        </div>

        <div className="metrics">
          <div className="metric">
            <CalendarOutlined className="metric__icon metric__icon--blue" />
            <div>
              <div className="metric__val">{total}</div>
              <div className="metric__label">Tổng số công việc</div>
            </div>
          </div>
          <div className="metric">
            <ClockCircleOutlined className="metric__icon metric__icon--amber" />
            <div>
              <div className="metric__val">{pending}</div>
              <div className="metric__label">Chờ xử lý</div>
            </div>
          </div>
          <div className="metric">
            <SyncOutlined className="metric__icon metric__icon--teal" />
            <div>
              <div className="metric__val">{inProgress}</div>
              <div className="metric__label">Đang xử lý</div>
            </div>
          </div>
          <div className="metric">
            <ExclamationCircleOutlined className="metric__icon metric__icon--red" />
            <div>
              <div className="metric__val">{overdue}</div>
              <div className="metric__label">Quá hạn</div>
            </div>
          </div>
        </div>

        <div className="data-panel">
          <div className="data-panel__toolbar">
            <Input
              className="search-input"
              placeholder="Tìm theo tiêu đề, mô tả..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              allowClear
            />
            <Select
              className="filter-select"
              value={statusFilter}
              onChange={setStatusFilter}
              options={[
                { value: "all", label: "Tất cả" },
                { value: "pending", label: "Chờ xử lý" },
                { value: "in_progress", label: "Đang xử lý" },
                { value: "completed", label: "Hoàn thành" },
              ]}
            />
          </div>

          <Table<Task>
            columns={columns}
            dataSource={tasks}
            rowKey="task_id"
            loading={loading}
            pagination={{
              pageSize: 8,
              showSizeChanger: false,
              showTotal: (t) => `${t} công việc`,
            }}
            scroll={{ x: 860 }}
            locale={{
              emptyText: (
                <Empty
                  image={Empty.PRESENTED_IMAGE_SIMPLE}
                  description="Chưa có công việc nào"
                />
              ),
            }}
          />
        </div>
      </main>

      <Modal
        className="task-modal"
        title={
          <span className="modal-title">
            {editingTask ? <EditOutlined /> : <PlusCircleOutlined />}
            {editingTask ? " Chỉnh sửa công việc" : " Thêm công việc mới"}
          </span>
        }
        open={modalOpen}
        onCancel={() => {
          setModalOpen(false);
          form.resetFields();
          setEditingTask(null);
        }}
        closeIcon={<CloseOutlined />}
        footer={
          <div className="modal-footer">
            <Button
              className="btn-ghost"
              onClick={() => {
                setModalOpen(false);
                form.resetFields();
                setEditingTask(null);
              }}
            >
              Hủy
            </Button>
            <button className="btn-primary" onClick={handleSubmit}>
              {editingTask ? "Cập nhật" : "Tạo mới"}
            </button>
          </div>
        }
        width={520}
        destroyOnClose
      >
        <Form form={form} layout="vertical" className="task-form">
          <Form.Item
            name="title"
            label="Tiêu đề"
            rules={[{ required: true, message: "Vui lòng nhập tiêu đề!" }]}
          >
            <Input placeholder="Nhập tiêu đề task..." />
          </Form.Item>

          <Form.Item name="description" label="Mô tả">
            <Input.TextArea rows={3} placeholder="Nhập mô tả..." />
          </Form.Item>

          <div className="form-row">

            <Form.Item
              name="created_at"
              label="Ngày bắt đầu làm"
              rules={[{ required: true, message: "Chọn ngày tạo!" }]}
              style={{ flex: 1 }}
            >
              <DatePicker
                showTime
                format="DD/MM/YYYY HH:mm"
                style={{ width: "100%" }}
                placeholder="Chọn ngày tạo..."
              />
            </Form.Item>
            <Form.Item
              name="deadline"
              label="Deadline"
              rules={[{ required: true, message: "Chọn deadline!" }]}
              style={{ flex: 1 }}
            >
              <DatePicker
                showTime
                format="DD/MM/YYYY HH:mm"
                style={{ width: "100%" }}
                placeholder="Chọn deadline..."
              />
            </Form.Item>
          </div>

          <Form.Item
            name="status"
            label="Trạng thái"
            rules={[{ required: true, message: "Chọn trạng thái!" }]}
            initialValue="pending"
            style={{ flex: 1 }}
          >
            <Select
              options={[
                { value: "pending", label: "Chờ xử lý" },
                { value: "in_progress", label: "Đang xử lý" },
                { value: "completed", label: "Hoàn thành" },
              ]}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default App;