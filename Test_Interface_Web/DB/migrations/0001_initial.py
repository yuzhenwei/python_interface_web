# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-27 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interface_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interfacename', models.CharField(max_length=100, verbose_name='接口名称')),
                ('url', models.CharField(max_length=500, verbose_name='接口地址')),
                ('defaultpar', models.CharField(max_length=10000, verbose_name='默认入参')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('type', models.IntegerField()),
                ('pname', models.CharField(max_length=100, verbose_name='项目名称')),
                ('mname', models.CharField(max_length=100, verbose_name='模块名称')),
                ('isdelete', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'interface_info',
            },
        ),
        migrations.CreateModel(
            name='Interface_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalcount', models.IntegerField(default=0, verbose_name='用例总数')),
                ('okcount', models.IntegerField(default=0, verbose_name='通过数')),
                ('failcount', models.IntegerField(default=0, verbose_name='失败数')),
                ('errorcount', models.IntegerField(default=0, verbose_name='错误数')),
                ('runnertime', models.DateTimeField(auto_now=True, verbose_name='运行时间')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
            ],
            options={
                'db_table': 'interface_result',
            },
        ),
        migrations.CreateModel(
            name='Interface_result_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(verbose_name='结果类型')),
                ('failinfo', models.CharField(max_length=500, verbose_name='失败原因')),
                ('resultinfo', models.TextField(max_length=500, verbose_name='json结果')),
                ('checkinfo', models.TextField(max_length=500, verbose_name='检查点结果')),
                ('versionnum', models.CharField(max_length=100, verbose_name='版本号')),
                ('runnertime', models.DateTimeField(auto_now=True, verbose_name='运行时间')),
                ('resultid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Interface_result')),
            ],
            options={
                'db_table': 'interface_result_detail',
            },
        ),
        migrations.CreateModel(
            name='Job_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobname', models.CharField(max_length=100, verbose_name='任务名称')),
                ('jobid', models.CharField(max_length=100, verbose_name='定时任务ID')),
                ('mailaddress', models.CharField(max_length=100, verbose_name='指向邮件地址')),
                ('day_of_week', models.CharField(max_length=100, verbose_name='运行时间段')),
                ('runnertime', models.CharField(max_length=100, verbose_name='执行时间')),
                ('caselist', models.CharField(max_length=500, verbose_name='用例集')),
                ('jobtype', models.IntegerField(default=0, verbose_name='状态')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
            ],
            options={
                'db_table': 'job_info',
            },
        ),
        migrations.CreateModel(
            name='Project_info',
            fields=[
                ('pname', models.CharField(max_length=100, verbose_name='项目名称')),
                ('pnumber', models.BigAutoField(max_length=100, primary_key=True, serialize=False, verbose_name='项目标识')),
                ('description', models.CharField(max_length=200, verbose_name='项目描述')),
                ('sortnum', models.IntegerField(default=0, verbose_name='项目排序号')),
                ('isdelete', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'project_info',
            },
        ),
        migrations.CreateModel(
            name='Project_model',
            fields=[
                ('modelname', models.CharField(max_length=100, verbose_name='模块名称')),
                ('mnumber', models.BigAutoField(max_length=100, primary_key=True, serialize=False, verbose_name='模块标识号')),
                ('description', models.CharField(max_length=200, verbose_name='模块描述')),
                ('sortnum', models.IntegerField(default=0, verbose_name='模块排序号')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
                ('pnumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Project_info')),
            ],
            options={
                'db_table': 'project_model',
            },
        ),
        migrations.CreateModel(
            name='Template_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isdelete', models.IntegerField(default=0)),
                ('interfaceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Interface_info')),
            ],
            options={
                'db_table': 'template_detail',
            },
        ),
        migrations.CreateModel(
            name='Template_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('templatename', models.CharField(max_length=100, verbose_name='模板名称')),
                ('remark', models.CharField(max_length=100, verbose_name='备注')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
                ('publicpar', models.CharField(default=None, max_length=900, verbose_name='公共参数')),
                ('pnumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Project_info')),
            ],
            options={
                'db_table': 'template_info',
            },
        ),
        migrations.CreateModel(
            name='User_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interfaceurl', models.CharField(max_length=500, verbose_name='接口地址')),
                ('paraminfo', models.CharField(max_length=10000, verbose_name='参数字段内容')),
                ('isequal', models.CharField(max_length=500, verbose_name='是否等于')),
                ('isnotequal', models.CharField(max_length=500, verbose_name='是否不等于')),
                ('iscontain', models.CharField(max_length=500, verbose_name='是否包含')),
                ('isnotcontain', models.CharField(max_length=500, verbose_name='不包含')),
                ('usercasename', models.CharField(max_length=100, verbose_name='用例名称')),
                ('isjoin', models.IntegerField(default=0, verbose_name='是否关联')),
                ('joininfo', models.CharField(max_length=500, verbose_name='关联描述')),
                ('rejoin_key', models.CharField(max_length=500, null=True, verbose_name='对外提供的关联key')),
                ('rejoin_value', models.CharField(max_length=500, null=True, verbose_name='对外提供的关联values')),
                ('isheader', models.IntegerField(default=0, verbose_name='是否有头部')),
                ('headerinfo', models.CharField(max_length=500, verbose_name='Header内容')),
                ('status', models.IntegerField(default=0, verbose_name='执行状态')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
                ('run_order', models.IntegerField(default=-1, verbose_name='执行顺序')),
                ('interfaceid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Interface_info')),
            ],
            options={
                'db_table': 'user_case',
            },
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='名称')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('isdelete', models.IntegerField(default=0, verbose_name='是否删除')),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
        migrations.AddField(
            model_name='template_detail',
            name='templateid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Template_info'),
        ),
        migrations.AddField(
            model_name='template_detail',
            name='usercaseid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.User_case'),
        ),
        migrations.AddField(
            model_name='interface_result_detail',
            name='usercaseid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.User_case'),
        ),
        migrations.AddField(
            model_name='interface_result',
            name='templateid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Template_info'),
        ),
        migrations.AddField(
            model_name='interface_info',
            name='mnumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Project_model'),
        ),
        migrations.AddField(
            model_name='interface_info',
            name='pnumber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Project_info'),
        ),
    ]
