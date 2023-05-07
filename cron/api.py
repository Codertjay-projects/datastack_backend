from account.models import User


def resetDownloads():
    users = User.objects.filter().update(todayDownloads=0)
    print("Cron has been executed!")
