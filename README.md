- [![](https://img.shields.io/badge/python-3.10.3-orange.svg)](https://www.python.org/downloads/release/python-3103/)
- [![](https://img.shields.io/badge/django-4.0.3-green.svg)](https://docs.djangoproject.com/en/4.0/)
- [![](https://img.shields.io/badge/bootstrap-5.1.3-blue.svg)](https://getbootstrap.com/docs/5.1/getting-started/introduction/)

## Bản demo dự án: [Demo] (https://www.hoangvangioi.xyz)


## Chạy dự án tại máy chủ cục bộ


1. Sao chép dự án về máy tính

    Mở cửa sổ dòng lệnh, đi tới thư mục lưu dự án và nhập lệnh sau: 

   ```
   git clone https://github.com/gioitube/blog-django.git
   ```

2. Tạo và kích hoạt môi trường ảo

    Di chuyển đến thư mục dự án

    ```
    cd blog-django
    ```

    Tạo môi trường ảo

    ```
    virtualenv env
    ```

    Kích hoạt môi trường ảo

    ```
    # windows
    env\Scripts\activate

    # linux and macOS
   source env/bin/activate
    ```

    Để biết cách sử dụng môi trường ảo, hãy xem: [Xây dựng môi trường phát triển] (https://virtualenv.pypa.io/en/latest/index.html). 
    Nếu không muốn sử dụng môi trường ảo, bạn có thể bỏ qua bước này.

3. Cài đặt các gói thư viện cho dự án

    ```
    pip install -r requirements.txt
    ```


4. Tạo file .env và cập nhật

    ```
    DEBUG = True
    ALLOWED_HOSTS = 127.0.0.1

    SECRET_KEY = qf&^m(ttxc+updmfl&p49@l+u-b^jx96f57zvi3xf#c*mftuwm

    EMAIL_HOST_USER = "email"
    EMAIL_HOST_PASSWORD = "password"

    CSRF_TRUSTED_ORIGINS = 'http://127.0.0.1'
    CSRF_COOKIE_DOMAIN = '127.0.0.1'
    CORS_ORIGIN_WHITELIST = 'http://127.0.0.1'
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

    Nhập vào trình duyệt: 127.0.0.1:8000/gioihv

    Đăng nhập bằng tài khoản quản trị viên đã tạo ở bước 6


## Donate

1. [Paypal] (https://www.paypal.com/paypalme/gioihoang)

2. [Momo] (https://me.momo.vn/pwI4TzsliRfeIqCdini5Ia)

-  **Qr Momo**
![](/static/img/momo.jpg)




purgecss --css static/css/theme.min2.css --content templates/base.html templates/404.html templates/accounts/register.html  templates/accounts/profile.html templates/accounts/login.html templates/accounts/edit_profile.html templates/accounts/change-password.html templates/accounts/account_verification_email.html templates/accounts/password-reset/password_reset_complete.html templates/accounts/password-reset/password_reset_confirm.html templates/accounts/password-reset/password_reset_done.html templates/accounts/password-reset/password_reset_email.html templates/accounts/password-reset/password_reset.html templates/category/category_list_form.html templates/category/create_category.html templates/category/delete_category.html templates/category/update_category.html templates/includes/alerts.html templates/includes/dashboard_sidebar.html templates/includes/footer.html templates/includes/navbar.html templates/includes/sidebar.html templates/post/create_post.html templates/post/delete_post.html templates/post/update_post.html templates/post/post_detail.html templates/post/post_list_form.html templates/post/post_list.html static/js/bootstrap.bundle.min.js static/js/lightgallery.min.js static/js/theme.min.js --output build/