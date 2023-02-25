from django.shortcuts import render
from django.utils.html import format_html
from django.views.generic import TemplateView
from django.templatetags.static import static
from django.contrib.sites.shortcuts import get_current_site


def handler400(request, *args, **kwargs):
    return render(request, '404.html', status=400)


def handler403(request, *args, **kwargs):
    return render(request, '404.html', status=403)


def handler404(request, *args, **kwargs):
    return render(request, '404.html', status=404)


def handler500(request, *args, **kwargs):
    return render(request, '404.html', status=500)


html_code = """
<div class="dark:bg-gray-900 pt-20 pb-8">
    <div class="mx-auto container w-full flex items-center md:flex-row flex-col justify-between px-6 lg:px-0"></div>
    <div class="mx-auto container w-full flex xl:flex-row flex-col justify-between items-start mt-12 px-6 lg:px-0">
        <div class="flex flex-col justify-start items-start dark:text-white font-serif">

            <h1 class="font-bold text-4xl my-5">Privacy Policy</h1>
            <p class="my-4">Last updated: February 23, 2023</p>
            <p class="my-4">This Privacy Policy describes Our
                policies and procedures on the collection, use and disclosure of Your information
                when You use the Service and tells You about Your privacy rights and how the law protects You.</p>
            <p class="my-4">We use Your Personal data to provide
                and improve the Service. By using the Service, You agree to the collection and
                use of information in accordance with this Privacy Policy. This Privacy Policy has been created with the help of
                the
                <a href="https://www.privacypolicies.com/privacy-policy-generator/" class="font-medium text-blue-600 dark:text-blue-400 hover:underline" target="_blank">Privacy Policy
                    Generator</a>.
            </p>
            <h1 class="font-bold text-4xl my-5">Interpretation and Definitions</h1>
            <h2 class="font-bold text-2xl my4">Interpretation</h2>
            <p class="my-4">The words of which the initial letter
                is capitalized have meanings defined under the following conditions. The
                following definitions shall have the same meaning regardless of whether they appear in singular or in plural.
            </p>
            <h2 class="font-bold text-2xl my4">Definitions</h2>
            <p class="my-4">For the purposes of this Privacy Policy:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>
                    <p class="my-4"><strong>Account</strong> means
                        a unique account created for You to access our Service or parts of our
                        Service.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Affiliate</strong>
                        means an entity that controls, is controlled by or is under common control with a
                        party, where &quot;control&quot; means ownership of 50% or more of the shares, equity interest or other
                        securities entitled to vote for election of directors or other managing authority.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Company</strong>
                        (referred to as either &quot;the Company&quot;, &quot;We&quot;, &quot;Us&quot; or
                        &quot;Our&quot; in this Agreement) refers to Hoàng Văn Giỏi.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Cookies</strong> are
                        small files that are placed on Your computer, mobile device or any other device
                        by a website, containing the details of Your browsing history on that website among its many uses.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Country</strong> refers
                        to: Vietnam</p>
                </li>
                <li>
                    <p class="my-4"><strong>Device</strong> means
                        any device that can access the Service such as a computer, a cellphone or a
                        digital tablet.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Personal Data</strong>
                        is any information that relates to an identified or identifiable individual.
                    </p>
                </li>
                <li>
                    <p class="my-4"><strong>Service</strong> refers
                        to the Website.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Service
                            Provider</strong> means any natural or legal person who processes the data on behalf of the
                        Company. It refers to third-party companies or individuals employed by the Company to facilitate the
                        Service, to provide the Service on behalf of the Company, to perform services related to the Service or
                        to
                        assist the Company in analyzing how the Service is used.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Usage Data</strong>
                        refers to data collected automatically, either generated by the use of the
                        Service or from the Service infrastructure itself (for example, the duration of a page visit).</p>
                </li>
                <li>
                    <p class="my-4"><strong>Website</strong> refers
                        to Hoàng Văn Giỏi, accessible from <a href="https://hoangvangioi.live/" class="font-medium text-blue-600 dark:text-blue-400 hover:underline" rel="external nofollow noopener"
                            target="_blank">https://hoangvangioi.live/</a></p>
                </li>
                <li>
                    <p class="my-4"><strong>You</strong> means the
                        individual accessing or using the Service, or the company, or other legal
                        entity on behalf of which such individual is accessing or using the Service, as applicable.</p>
                </li>
            </ul>
            <h1 class="font-bold text-4xl my-5">Collecting and Using Your Personal Data</h1>
            <h2 class="font-bold text-2xl my4">Types of Data Collected</h2>
            <h3 class="font-bold text-lg my-4">Personal Data</h3>
            <p class="my-4">While using Our Service, We may ask You
                to provide Us with certain personally identifiable information that can be
                used to contact or identify You. Personally identifiable information may include, but is not limited to:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>
                    <p class="my-4">Email address</p>
                </li>
                <li>
                    <p class="my-4">First name and last name</p>
                </li>
                <li>
                    <p class="my-4">Usage Data</p>
                </li>
            </ul>
            <h3 class="font-bold text-lg my-4">Usage Data</h3>
            <p class="my-4">Usage Data is collected automatically
                when using the Service.</p>
            <p class="my-4">Usage Data may include information such
                as Your Device's Internet Protocol address (e.g. IP address), browser type,
                browser version, the pages of our Service that You visit, the time and date of Your visit, the time spent on
                those
                pages, unique device identifiers and other diagnostic data.</p>
            <p class="my-4">When You access the Service by or
                through a mobile device, We may collect certain information automatically,
                including, but not limited to, the type of mobile device You use, Your mobile device unique ID, the IP address
                of
                Your mobile device, Your mobile operating system, the type of mobile Internet browser You use, unique device
                identifiers and other diagnostic data.</p>
            <p class="my-4">We may also collect information that
                Your browser sends whenever You visit our Service or when You access the Service
                by or through a mobile device.</p>
            <h3 class="font-bold text-lg my-4">Tracking Technologies and Cookies</h3>
            <p class="my-4">We use Cookies and similar tracking
                technologies to track the activity on Our Service and store certain information.
                Tracking technologies used are beacons, tags, and scripts to collect and track information and to improve and
                analyze Our Service. The technologies We use may include:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li><strong>Cookies or Browser Cookies.</strong> A cookie is a small file placed on Your Device. You can
                    instruct
                    Your browser to refuse all Cookies or to indicate when a Cookie is being sent. However, if You do not accept
                    Cookies, You may not be able to use some parts of our Service. Unless you have adjusted Your browser setting
                    so
                    that it will refuse Cookies, our Service may use Cookies.</li>
                <li><strong>Web Beacons.</strong> Certain sections of our Service and our emails may contain small electronic
                    files
                    known as web beacons (also referred to as clear gifs, pixel tags, and single-pixel gifs) that permit the
                    Company, for example, to count users who have visited those pages or opened an email and for other related
                    website statistics (for example, recording the popularity of a certain section and verifying system and
                    server
                    integrity).</li>
            </ul>
            <p class="my-4">Cookies can be &quot;Persistent&quot;
                or &quot;Session&quot; Cookies. Persistent Cookies remain on Your personal
                computer or mobile device when You go offline, while Session Cookies are deleted as soon as You close Your web
                browser. Learn more about cookies on the <a
                    href="https://www.privacypolicies.com/blog/privacy-policy-template/#Use_Of_Cookies_Log_Files_And_Tracking"
                    class="font-medium text-blue-600 dark:text-blue-400 hover:underline"
                    target="_blank">Privacy Policies website</a> article.</p>
            <p class="my-4">We use both Session and Persistent
                Cookies for the purposes set out below:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>
                    <p class="my-4"><strong>Necessary / Essential
                            Cookies</strong></p>
                    <p class="my-4">Type: Session Cookies</p>
                    <p class="my-4">Administered by: Us</p>
                    <p class="my-4">Purpose: These Cookies are
                        essential to provide You with services available through the Website and to enable
                        You to use some of its features. They help to authenticate users and prevent fraudulent use of user
                        accounts. Without these Cookies, the services that You have asked for cannot be provided, and We only
                        use
                        these Cookies to provide You with those services.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Cookies Policy / Notice
                            Acceptance Cookies</strong></p>
                    <p class="my-4">Type: Persistent Cookies</p>
                    <p class="my-4">Administered by: Us</p>
                    <p class="my-4">Purpose: These Cookies identify
                        if users have accepted the use of cookies on the Website.</p>
                </li>
                <li>
                    <p class="my-4"><strong>Functionality
                            Cookies</strong></p>
                    <p class="my-4">Type: Persistent Cookies</p>
                    <p class="my-4">Administered by: Us</p>
                    <p class="my-4">Purpose: These Cookies allow us
                        to remember choices You make when You use the Website, such as remembering
                        your login details or language preference. The purpose of these Cookies is to provide You with a more
                        personal experience and to avoid You having to re-enter your preferences every time You use the Website.
                    </p>
                </li>
            </ul>
            <p class="my-4">For more information about the cookies
                we use and your choices regarding cookies, please visit our Cookies Policy or
                the Cookies section of our Privacy Policy.</p>
            <h2 class="font-bold text-2xl my4">Use of Your Personal Data</h2>
            <p class="my-4">The Company may use Personal Data for
                the following purposes:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>
                    <p class="my-4"><strong>To provide and maintain
                            our Service</strong>, including to monitor the usage of our Service.</p>
                </li>
                <li>
                    <p class="my-4"><strong>To manage Your
                            Account:</strong> to manage Your registration as a user of the Service. The Personal
                        Data You provide can give You access to different functionalities of the Service that are available to
                        You
                        as a registered user.</p>
                </li>
                <li>
                    <p class="my-4"><strong>For the performance of
                            a contract:</strong> the development, compliance and undertaking of the
                        purchase contract for the products, items or services You have purchased or of any other contract with
                        Us
                        through the Service.</p>
                </li>
                <li>
                    <p class="my-4"><strong>To contact
                            You:</strong> To contact You by email, telephone calls, SMS, or other equivalent forms of
                        electronic communication, such as a mobile application's push notifications regarding updates or
                        informative
                        communications related to the functionalities, products or contracted services, including the security
                        updates, when necessary or reasonable for their implementation.</p>
                </li>
                <li>
                    <p class="my-4"><strong>To provide You</strong>
                        with news, special offers and general information about other goods, services
                        and events which we offer that are similar to those that you have already purchased or enquired about
                        unless
                        You have opted not to receive such information.</p>
                </li>
                <li>
                    <p class="my-4"><strong>To manage Your
                            requests:</strong> To attend and manage Your requests to Us.</p>
                </li>
                <li>
                    <p class="my-4"><strong>For business
                            transfers:</strong> We may use Your information to evaluate or conduct a merger,
                        divestiture, restructuring, reorganization, dissolution, or other sale or transfer of some or all of Our
                        assets, whether as a going concern or as part of bankruptcy, liquidation, or similar proceeding, in
                        which
                        Personal Data held by Us about our Service users is among the assets transferred.</p>
                </li>
                <li>
                    <p class="my-4"><strong>For other
                            purposes</strong>: We may use Your information for other purposes, such as data analysis,
                        identifying usage trends, determining the effectiveness of our promotional campaigns and to evaluate and
                        improve our Service, products, services, marketing and your experience.</p>
                </li>
            </ul>
            <p class="my-4">We may share Your personal information
                in the following situations:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li><strong>With Service Providers:</strong> We may share Your personal information with Service Providers to
                    monitor and analyze the use of our Service, to contact You.</li>
                <li><strong>For business transfers:</strong> We may share or transfer Your personal information in connection
                    with,
                    or during negotiations of, any merger, sale of Company assets, financing, or acquisition of all or a portion
                    of
                    Our business to another company.</li>
                <li><strong>With Affiliates:</strong> We may share Your information with Our affiliates, in which case we will
                    require those affiliates to honor this Privacy Policy. Affiliates include Our parent company and any other
                    subsidiaries, joint venture partners or other companies that We control or that are under common control
                    with
                    Us.</li>
                <li><strong>With business partners:</strong> We may share Your information with Our business partners to offer
                    You
                    certain products, services or promotions.</li>
                <li><strong>With other users:</strong> when You share personal information or otherwise interact in the public
                    areas
                    with other users, such information may be viewed by all users and may be publicly distributed outside.</li>
                <li><strong>With Your consent</strong>: We may disclose Your personal information for any other purpose with
                    Your
                    consent.</li>
            </ul>
            <h2 class="font-bold text-2xl my4">Retention of Your Personal Data</h2>
            <p class="my-4">The Company will retain Your Personal
                Data only for as long as is necessary for the purposes set out in this Privacy
                Policy. We will retain and use Your Personal Data to the extent necessary to comply with our legal obligations
                (for
                example, if we are required to retain your data to comply with applicable laws), resolve disputes, and enforce
                our
                legal agreements and policies.</p>
            <p class="my-4">The Company will also retain Usage Data
                for internal analysis purposes. Usage Data is generally retained for a
                shorter period of time, except when this data is used to strengthen the security or to improve the functionality
                of
                Our Service, or We are legally obligated to retain this data for longer time periods.</p>
            <h2 class="font-bold text-2xl my4">Transfer of Your Personal Data</h2>
            <p class="my-4">Your information, including Personal
                Data, is processed at the Company's operating offices and in any other places
                where the parties involved in the processing are located. It means that this information may be transferred to —
                and
                maintained on — computers located outside of Your state, province, country or other governmental jurisdiction
                where
                the data protection laws may differ than those from Your jurisdiction.</p>
            <p class="my-4">Your consent to this Privacy Policy
                followed by Your submission of such information represents Your agreement to that
                transfer.</p>
            <p class="my-4">The Company will take all steps
                reasonably necessary to ensure that Your data is treated securely and in accordance
                with this Privacy Policy and no transfer of Your Personal Data will take place to an organization or a country
                unless there are adequate controls in place including the security of Your data and other personal information.
            </p>
            <h2 class="font-bold text-2xl my4">Delete Your Personal Data</h2>
            <p class="my-4">You have the right to delete or request
                that We assist in deleting the Personal Data that We have collected about
                You.</p>
            <p class="my-4">Our Service may give You the ability to
                delete certain information about You from within the Service.</p>
            <p class="my-4">You may update, amend, or delete Your
                information at any time by signing in to Your Account, if you have one, and
                visiting the account settings section that allows you to manage Your personal information. You may also contact
                Us
                to request access to, correct, or delete any personal information that You have provided to Us.</p>
            <p class="my-4">Please note, however, that We may need
                to retain certain information when we have a legal obligation or lawful basis
                to do so.</p>
            <h2 class="font-bold text-2xl my4">Disclosure of Your Personal Data</h2>
            <h3 class="font-bold text-lg my-4">Business Transactions</h3>
            <p class="my-4">If the Company is involved in a merger,
                acquisition or asset sale, Your Personal Data may be transferred. We will
                provide notice before Your Personal Data is transferred and becomes subject to a different Privacy Policy.</p>
            <h3 class="font-bold text-lg my-4">Law enforcement</h3>
            <p class="my-4">Under certain circumstances, the
                Company may be required to disclose Your Personal Data if required to do so by law
                or in response to valid requests by public authorities (e.g. a court or a government agency).</p>
            <h3 class="font-bold text-lg my-4">Other legal requirements</h3>
            <p class="my-4">The Company may disclose Your Personal
                Data in the good faith belief that such action is necessary to:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>Comply with a legal obligation</li>
                <li>Protect and defend the rights or property of the Company</li>
                <li>Prevent or investigate possible wrongdoing in connection with the Service</li>
                <li>Protect the personal safety of Users of the Service or the public</li>
                <li>Protect against legal liability</li>
            </ul>
            <h2 class="font-bold text-2xl my4">Security of Your Personal Data</h2>
            <p class="my-4">The security of Your Personal Data is
                important to Us, but remember that no method of transmission over the Internet,
                or method of electronic storage is 100% secure. While We strive to use commercially acceptable means to protect
                Your
                Personal Data, We cannot guarantee its absolute security.</p>
            <h1 class="font-bold text-4xl my-5">Children's Privacy</h1>
            <p class="my-4">Our Service does not address anyone
                under the age of 13. We do not knowingly collect personally identifiable
                information from anyone under the age of 13. If You are a parent or guardian and You are aware that Your child
                has
                provided Us with Personal Data, please contact Us. If We become aware that We have collected Personal Data from
                anyone under the age of 13 without verification of parental consent, We take steps to remove that information
                from
                Our servers.</p>
            <p class="my-4">If We need to rely on consent as a
                legal basis for processing Your information and Your country requires consent from
                a parent, We may require Your parent's consent before We collect and use that information.</p>
            <h1 class="font-bold text-4xl my-5">Links to Other Websites</h1>
            <p class="my-4">Our Service may contain links to other
                websites that are not operated by Us. If You click on a third party link, You
                will be directed to that third party's site. We strongly advise You to review the Privacy Policy of every site
                You
                visit.</p>
            <p class="my-4">We have no control over and assume no
                responsibility for the content, privacy policies or practices of any third
                party sites or services.</p>
            <h1 class="font-bold text-4xl my-5">Changes to this Privacy Policy</h1>
            <p class="my-4">We may update Our Privacy Policy from
                time to time. We will notify You of any changes by posting the new Privacy
                Policy on this page.</p>
            <p class="my-4">We will let You know via email and/or a
                prominent notice on Our Service, prior to the change becoming effective and
                update the &quot;Last updated&quot; date at the top of this Privacy Policy.</p>
            <p class="my-4">You are advised to review this Privacy
                Policy periodically for any changes. Changes to this Privacy Policy are
                effective when they are posted on this page.</p>
            <h1 class="font-bold text-4xl my-5">Contact Us</h1>
            <p class="my-4">If you have any questions about this
                Privacy Policy, You can contact us:</p>
            <ul class="list-disc list-outside lg:mx-16 mx-10">
                <li>By email: <a href="mailto:support@hoangvangioi.live" class="font-medium text-blue-600 dark:text-blue-400 hover:underline __cf_email__" data-cfemail="a8dbddd8d8c7dadce8c0c7c9c6cfdec9c6cfc1c7c186c4c1decd">support@hoangvangioi.live</a></li>
            </ul>

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


class AboutPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):

        about_html_code = """
            <div class="bg-white dark:bg-gray-800">
                <div class="w-full container mx-auto pt-12"></div>
                <div class="2xl:container 2xl:mx-auto lg:py-16 lg:px-20 md:py-12 md:px-6 py-9 px-4">
                    <div class="flex flex-col lg:flex-row justify-between gap-8">
                        <div class="w-full lg:w-5/12 flex flex-col justify-center px-4">
                            <h1 class="text-3xl lg:text-4xl font-bold leading-9 text-gray-800 dark:text-white pb-6">Giới thiệu bản thân </h1>
                            <p class="font-normal text-base leading-6 text-gray-600 dark:text-white">
                                Xin chào! 
                                <br><br>
                                Tôi là Hoàng Văn Giỏi người tạo trang web {2} và được tạo ra nhằm mục đích lưu trữ, chia sẻ kiến thức và kinh nghiệm của đã học và đã tích luỹ được. 
                                <br>
                                Nếu bạn muốn liên hệ với tôi, bạn có thể gửi email cho tôi tại địa chỉ admin@{2}. Hoặc bạn cũng có thể liên hệ với tôi qua biểu mẫu <a href="{0}">tại đây</a>.
                                <br><br>
                                Cảm ơn bạn đã đọc về tôi và tôi hy vọng bạn sẽ thấy bài viết của tôi hữu ích!
                                <br><br>
                                Trân trọng,<br>Hoàng Văn Giỏi
                            </p>
                        </div>
                        <div class="mx-auto w-10/12 lg:w-8/12 px-16">
                            <img class="w-full h-full" src="{1}" alt="A group of People" />
                        </div>
                    </div>
                </div>
            </div>
            """.format('/contact/', static('favicon.svg'), get_current_site(self.request))

        context = super().get_context_data(**kwargs)
        context['about'] = format_html(about_html_code)
        return context