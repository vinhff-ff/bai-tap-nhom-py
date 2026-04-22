import React, { useState } from "react";
import { Form, Input, message } from "antd";
import {
  UserOutlined,
  LockOutlined,
  ThunderboltOutlined,
  ArrowRightOutlined,
  LoadingOutlined,
} from "@ant-design/icons";
import { register, login } from "../api/auth";

// ─── Props ────────────────────────────────────────────────────────────────────
interface AuthPageProps {
  onLoginSuccess: (userId: number, username: string) => void;
}

type Mode = "login" | "register";

// ─── Component ────────────────────────────────────────────────────────────────
const AuthPage: React.FC<AuthPageProps> = ({ onLoginSuccess }) => {
  const [mode, setMode] = useState<Mode>("login");
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      if (mode === "register") {
        await register({ username: values.username, password: values.password });
        message.success("Đăng ký thành công! Vui lòng đăng nhập.");
        form.resetFields();
        setMode("login");
      } else {
        // res = { status: 200, message: "...", username: "...", id: 4 }
        const res = await login({ username: values.username, password: values.password });
        const userId: number  = (res as any).id;
        const uname: string   = (res as any).username ?? values.username;

        // Lưu session vào localStorage dùng id làm key
        localStorage.setItem("tf_user_id", String(userId));
        localStorage.setItem("tf_user",    uname);

        message.success("Đăng nhập thành công!");
        // Gọi callback → App sẽ cập nhật state và chuyển trang
        onLoginSuccess(userId, uname);
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        message.error(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const switchMode = (m: Mode) => {
    setMode(m);
    form.resetFields();
  };

  return (
    <div className="auth-shell">
      <div className="auth-bg" aria-hidden="true">
        <div className="auth-bg__grid" />
        <div className="auth-bg__glow" />
      </div>

      <div className="auth-card">
        {/* Brand */}
        <div className="auth-brand">
          <span className="auth-brand__name">
            Sản phẩm nhóm 7 - Lập trình Python nâng cao
          </span>
        </div>

        {/* Heading */}
        <div className="auth-heading">
          <h1 className="auth-heading__title">
            {mode === "login" ? "Chào mừng trở lại" : "Tạo tài khoản"}
          </h1>
          <p className="auth-heading__sub">
            {mode === "login"
              ? "Đăng nhập để quản lý công việc của bạn"
              : "Đăng ký để bắt đầu sử dụng TaskFlow"}
          </p>
        </div>

        {/* Tabs */}
        <div className="auth-tabs">
          <button
            className={`auth-tab ${mode === "login" ? "auth-tab--active" : ""}`}
            onClick={() => switchMode("login")}
            type="button"
          >
            Đăng nhập
          </button>
          <button
            className={`auth-tab ${mode === "register" ? "auth-tab--active" : ""}`}
            onClick={() => switchMode("register")}
            type="button"
          >
            Đăng ký
          </button>
          <div
            className="auth-tabs__indicator"
            style={{ transform: mode === "register" ? "translateX(100%)" : "translateX(0)" }}
          />
        </div>

        {/* Form */}
        <Form
          form={form}
          layout="vertical"
          className="auth-form"
          onFinish={handleSubmit}
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[
              { required: true, message: "Vui lòng nhập tên đăng nhập!" },
              { min: 3, message: "Tối thiểu 3 ký tự!" },
            ]}
          >
            <Input
              className="auth-input"
              prefix={<UserOutlined className="auth-input__icon" />}
              placeholder="Tên đăng nhập"
              size="large"
              autoComplete="username"
            />
          </Form.Item>

          <Form.Item
            name="password"
            rules={[
              { required: true, message: "Vui lòng nhập mật khẩu!" },
              { min: 6, message: "Tối thiểu 6 ký tự!" },
            ]}
          >
            <Input.Password
              className="auth-input"
              prefix={<LockOutlined className="auth-input__icon" />}
              placeholder="Mật khẩu"
              size="large"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
          </Form.Item>

          {mode === "register" && (
            <Form.Item
              name="confirmPassword"
              dependencies={["password"]}
              rules={[
                { required: true, message: "Vui lòng xác nhận mật khẩu!" },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error("Mật khẩu không khớp!"));
                  },
                }),
              ]}
            >
              <Input.Password
                className="auth-input"
                prefix={<LockOutlined className="auth-input__icon" />}
                placeholder="Xác nhận mật khẩu"
                size="large"
                autoComplete="new-password"
              />
            </Form.Item>
          )}

          <button className="auth-submit" type="submit" disabled={loading}>
            {loading ? (
              <LoadingOutlined />
            ) : (
              <>
                <span>{mode === "login" ? "Đăng nhập" : "Tạo tài khoản"}</span>
                <ArrowRightOutlined className="auth-submit__arrow" />
              </>
            )}
          </button>
        </Form>

        <p className="auth-hint">
          {mode === "login" ? "Chưa có tài khoản? " : "Đã có tài khoản? "}
          <button
            className="auth-hint__link"
            onClick={() => switchMode(mode === "login" ? "register" : "login")}
            type="button"
          >
            {mode === "login" ? "Đăng ký ngay" : "Đăng nhập"}
          </button>
        </p>
      </div>
    </div>
  );
};

export default AuthPage;