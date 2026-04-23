# Chủ đề làm việc:
- Trong cuộc sống và công việc hiện đại, việc quản lý thời gian và theo dõi các nhiệm vụ là rất quan trọng. Tuy nhiên, nhiều người vẫn gặp khó khăn trong việc ghi nhớ và sắp xếp công việc một cách hiệu quả.

- Hệ thống To-Do App được xây dựng nhằm hỗ trợ người dùng:

    + Quản lý danh sách công việc
    + Theo dõi tiến độ thực hiện
    + Nhắc nhở các công việc quá hạn

Ứng dụng giúp tăng năng suất làm việc, tránh quên deadline và tổ chức công việc một cách khoa học.

# Thành viên nhóm:
- Nguyễn Đức Vĩnh : Trưởng nhóm
    + Thực hiện phần frontend
    + Thiết kế database
    + Hoàn thiện chức năng đăng ký, đăng nhập
    + Xây base code cho backend

- Bùi Duy Mạnh : Thành viên
    + Thực hiện phần backend
    + Hoàn thiện chức năng thêm, sửa, xóa task
    + Hoàn thiện chức đặt Deadline cho task

- Hoàng Tuấn Minh : Thành viên
    + Thực hiện phần backend
    + Hoàn thiện chức năng Nhắc việc quá hạn
    + Hoàn thiện chức năng lọc công việc theo trạng thái

# Tech tack sử dụng:
- Frontend: ReactJS, thư viện Ant Design
- Backend: thư viện MySQL-connector-python
- Database: MySQL

# Mô tả chức năng chính:
1. Đăng ký và đăng nhập: Người dùng có thể tạo tài khoản và đăng nhập vào hệ thống để quản lý công việc của mình.
2. Quản lý công việc: Người dùng có thể tạo, sửa, xóa công việc, đặt deadline và đánh dấu công việc đã hoàn thành.
3. Nhắc việc quá hạn: Hệ thống sẽ tự động nhắc người dùng về công việc đã quá hạn dựa trên deadline đã đặt.
4. Lọc công việc: Người dùng có thể lọc công việc theo trạng thái (đang làm, đã hoàn thành, quá hạn) để dễ dàng quản lý.
5. Quản lý phiên người dùng: Lưu trạng thái đăng nhập để người dùng không phải đăng nhập lại ngay khi tải lại trang, và có chức năng đăng xuất.
6. Tùy chỉnh giao diện: Cho phép người dùng chuyển đổi chế độ tối/sáng.

# Thiết kế hệ thống UML:
https://res.cloudinary.com/djfsn7nty/image/upload/f_auto,q_auto/diagram_eyb0lz?fbclid=IwY2xjawRW4h1leHRuA2FlbQIxMQBzcnRjBmFwcF9pZAEwAAEeTbLyp7jODsQwWCaySX0RW14vjU4S-p5xOw37wFtUW4Ok0iy-KG6wM9qURLg_aem_H8SCYNrZV6Mf22sNTFwJjQ

# Hướng phần phát triển:
- Tăng cường bảo mật với JSON Web Token (JWT)
    + Hệ thống sử dụng JWT để xác thực và phân quyền người dùng theo mô hình stateless. Sau khi đăng nhập thành công, hệ thống cấp một token cho người dùng; token này sẽ được gửi kèm trong các request API để xác thực.

- Thêm công việc bằng giọng nói (Voice Input)
   + Hệ thống hỗ trợ tạo công việc bằng giọng nói thông qua công nghệ Speech-to-Text, giúp chuyển đổi lời nói thành văn bản tự động. Người dùng có thể tạo task nhanh chóng mà không cần nhập tay, đặc biệt tiện lợi trên thiết bị di động.

- Chatbot hỗ trợ quản lý công việc
   + Hệ thống tích hợp chatbot thông minh có khả năng hiểu ngôn ngữ tự nhiên để tạo công việc, truy vấn trạng thái và hỗ trợ sắp xếp, ưu tiên task. Chatbot giúp người dùng tương tác nhanh chóng và thuận tiện hơn trong quá trình quản lý công việc.

- Gửi thông báo khi công việc sắp hết hạn
    + Hệ thống hỗ trợ gửi thông báo nhắc việc qua nhiều kênh như Telegram, Discord, Email, SMS và Zalo khi công việc sắp đến hạn hoặc quá hạn. Điều này giúp người dùng không bỏ lỡ deadline và quản lý công việc hiệu quả hơn.

# Video demo sản phẩm: 
https://drive.google.com/file/d/1f_x8dPNRO849cLZIfOaB-85BB9T1C5nG/view?fbclid=IwY2xjawRW641leHRuA2FlbQIxMQBzcnRjBmFwcF9pZAEwAAEebSgM8D_U2d7vOMy86MdVUcgmnaN4WIbfTkcIaWDtWQbVPxFaUToQCi_bc5I_aem_s0qq5bbasTSFbBpcI8NwLA
