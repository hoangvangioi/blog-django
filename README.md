## Bản demo dự án: [Demo] (https://www.hoangvangioi.xyz)


## Chạy dự án tại máy chủ cục bộ


1. Sao chép dự án về máy tính

    Mở cửa sổ dòng lệnh, đi tới thư mục lưu dự án và nhập lệnh sau: 

   ```
   git clone https://github.com/hoangvangioi/blog-django.git
   ```

2. Tạo và kích hoạt môi trường ảo

    Di chuyển đến thư mục dự án

    ```
    cd blog-django
    ```

    Tạo môi trường ảo

    ```
    python -m venv env
    ```

    Kích hoạt môi trường ảo

    ```
    # windows
    env\Scripts\activate

    # linux and macOS
   source env/bin/activate
    ```

3. Cài đặt các gói thư viện cho dự án

    ```
    pip install -r requirements.txt
    ```


4. Tạo file .env và cập nhật

    ```
    DEBUG = True
    ALLOWED_HOSTS = 127.0.0.1

    SECRET_KEY = 'secret-key'

    EMAIL_HOST_USER = "email"
    EMAIL_HOST_PASSWORD = "password"

    CSRF_TRUSTED_ORIGINS = 'http://127.0.0.1'
    CSRF_COOKIE_DOMAIN = '127.0.0.1'
    CORS_ORIGIN_WHITELIST = 'http://127.0.0.1'
    
    NAME_ADMIN = 'name-admin'
    EMAIL_ADMIN = 'email-admin'

    SITE_ID = 1

    CLOUDINARY_URL = 'cloudinary_url'
    ```

5. Di chuyển cơ sở dữ liệu

    Chạy lệnh sau để di chuyển cơ sở dữ liệu:

    ```
    python manage.py migrate
    ```

6. Tạo tài khoản quản trị viên

    ```
    python manage.py createsuperuser
    ```

7. Chạy máy chủ phát triển

    ```
    python manage.py runserver
    ```

    Nhập vào trình duyệt của bạn: 127.0.0.1:8000

8. Truy cập trang quản trị website

    Nhập vào trình duyệt: 127.0.0.1:8000/hvg

    Đăng nhập bằng tài khoản quản trị viên đã tạo ở bước 6