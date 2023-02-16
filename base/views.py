from django.shortcuts import render
from django.utils.html import format_html
from django.views.generic import TemplateView


def handler400(request, *args, **kwargs):
    return render(request, '404.html', status=400)


def handler403(request, *args, **kwargs):
    return render(request, '404.html', status=403)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '404.html', status=500)



html_code = """
<div class="dark:bg-gray-900 pt-28">
    <div class="mx-auto container w-full flex items-center md:flex-row flex-col justify-between px-6 lg:px-0">
        <div class="flex flex-col justify-start items-start lg:w-2/5 px-2 lg:px-0">
            <div class="md:mt-3">
                <p class="text-gray-800 dark:text-white lg:text-4xl text-3xl font-extrabold leading-9">Chính sách
                    bảo
                    mật</p>
            </div>
            <div class="md:mt-3">
                <p class="lg:text-base text-sm leading-normal text-gray-600 dark:text-gray-300">Learn how Trello has
                    leveraged Webber to consolidate it’s diverse range of services software</p>
            </div>
        </div>
    </div>
    <div class="mx-auto container w-full flex xl:flex-row flex-col justify-between items-start mt-12 px-6 lg:px-0">
        <div class="flex flex-col justify-start items-start">
            <div>
                <h2 class="text-gray-800 dark:text-white lg:text-2xl text-xl font-bold leading-7">Cookies</h2>
            </div>
            <div class="mt-3 mb-8">
                <p class="text-gray-800 dark:text-white lg:text-base text-sm leading-normal">
                    Nếu bạn viết bình luận trong website, bạn có thể cung cấp cần nhập tên, email địa chỉ website
                    trong
                    cookie. Các thông tin này nhằm giúp bạn không cần nhập thông tin nhiều lần khi viết bình luận
                    khác.
                    Cookie này sẽ được lưu giữ trong một thời điểm nhất định.
                    Nếu bạn vào trang đăng nhập, chúng tôi sẽ thiết lập một cookie tạm thời để xác định nếu trình
                    duyệt
                    cho phép sử dụng cookie. Cookie này không bao gồm thông tin cá nhân và sẽ được gỡ bỏ khi bạn
                    đóng
                    trình duyệt.
                    Khi bạn đăng nhập, chúng tôi sẽ thiết lập một vài cookie để lưu thông tin đăng nhập và lựa chọn
                    hiển
                    thị. Nếu bạn thoát tài khoản, thông tin cookie đăng nhập sẽ bị xoá.
                </p>
            </div>
            <div>
                <h2 class="text-gray-800 dark:text-white lg:text-2xl text-xl font-bold leading-7">Bình luận</h2>
            </div>
            <div class="mt-3 mb-8">
                <p class="text-gray-800 dark:text-white lg:text-base text-sm leading-normal">
                    Khi khách truy cập để lại bình luận trên trang web, chúng tôi thu thập dữ liệu được hiển thị
                    trong
                    biểu mẫu bình luận và cũng là địa chỉ IP của người truy cập và chuỗi user agent của người dùng
                    trình
                    duyệt để giúp phát hiện spam.
                </p>
            </div>
            <div>
                <h2 class="text-gray-800 dark:text-white lg:text-2xl text-xl font-bold leading-7">Media</h2>
            </div>
            <div class="mt-3 mb-8">
                <p class="text-gray-800 dark:text-white lg:text-base text-sm leading-normal">
                    Nếu bạn tải hình ảnh lên trang web, bạn nên tránh tải lên hình ảnh có dữ liệu vị trí được nhúng
                    (EXIF GPS) đi kèm. Khách truy cập vào trang web có thể tải xuống và giải nén bất kỳ dữ liệu vị
                    trí
                    nào từ hình ảnh trên trang web.
                </p>
            </div>
            <div>
                <h2 class="text-gray-800 dark:text-white lg:text-2xl text-xl font-bold leading-7">Nội dung nhúng từ
                    website khác</h2>
            </div>
            <div class="mt-3 mb-8">
                <p class="text-gray-800 dark:text-white lg:text-base text-sm leading-normal">
                    Các bài viết trên trang web này có thể bao gồm nội dung được nhúng (ví dụ: video, hình ảnh, bài
                    viết, v.v.). Nội dung được nhúng từ các trang web khác hoạt động theo cùng một cách chính xác
                    như
                    khi khách truy cập đã truy cập trang web khác.

                    Những website này có thể thu thập dữ liệu về bạn, sử dụng cookie, nhúng các trình theo dõi của
                    bên
                    thứ ba và giám sát tương tác của bạn với nội dung được nhúng đó, bao gồm theo dõi tương tác của
                    bạn
                    với nội dung được nhúng nếu bạn có tài khoản và đã đăng nhập vào trang web đó.
                </p>
            </div>
        </div>
    </div>
</div>
"""


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['privacy_policy'] = format_html(html_code)
        return context