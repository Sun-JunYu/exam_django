from django.db import models

# Create your models here.

class User(models.Model):

    # 用户名
    username = models.CharField(max_length=200)

    # 密码
    password = models.CharField(max_length=200)

     # 声明表名
    class Meta:
        db_table = "user"
