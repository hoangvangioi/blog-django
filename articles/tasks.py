import datetime
import mimetypes
from io import StringIO

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import call_command

logger = get_task_logger(__name__)


def send_email_with_attachment(subject, message, from_email, recipient_list, attachment_path):

    email = EmailMessage(subject, message, from_email, recipient_list)

    with open(attachment_path, 'rb') as fp:
        email.attach(
            filename=fp.name, 
            content=fp.read(), 
            mimetype=mimetypes.guess_type(attachment_path)[0] or 'application/octet-stream'
            )

    email.send()


@shared_task
def backup_send_email():
    logger.info(" Backup Database ")

    filebackup = 'dumpdata.json'
    buf = StringIO()
    call_command('dumpdata', 
                '--exclude=django_celery_beat',
                '--exclude=sessions',
                '--exclude=admin', 
                '--exclude=contenttypes',
                '--exclude=auth.Permission', 
                natural_foreign=True, 
                natural_primary=True, 
                indent=4,
                stdout=buf)

    buf.seek(0)
    with open(filebackup, 'w', encoding='utf-8') as f:
        f.write(buf.read())

    subject = f' Email with Attached Backup File - {datetime.date.today()} '
    message = f"""
    Hello ,

    We have sent you the backup file of our system as requested.

    Details of the backup:
    - Backup File Name: {filebackup}
    - Backup Time: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    Please check the attached file to ensure its integrity.

    Best regards
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = settings.EMAIL_RECIPIENT_LIST

    return send_email_with_attachment(subject, message, from_email, recipient_list, filebackup)