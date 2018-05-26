# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('asset_type', models.CharField(max_length=64, choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('software', '软件资产')], verbose_name='资产类型', default='server')),
                ('name', models.CharField(unique=True, verbose_name='资产名称', max_length=64)),
                ('sn', models.CharField(unique=True, verbose_name='资产序列号', max_length=128)),
                ('status', models.SmallIntegerField(choices=[(0, '在线'), (1, '下线'), (2, '未知'), (3, '故障'), (4, '备用')], verbose_name='设备状态', default=0)),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('purchase_day', models.DateField(blank=True, null=True, verbose_name='购买日期')),
                ('expire_day', models.DateField(blank=True, null=True, verbose_name='过保日期')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='价格')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('c_time', models.DateTimeField(verbose_name='批准日期', auto_now_add=True)),
                ('m_time', models.DateTimeField(verbose_name='更新日期', auto_now=True)),
                ('admin', models.ForeignKey(related_name='admin', blank=True, verbose_name='资产管理员', null=True, to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(related_name='approved_by', blank=True, verbose_name='批准人', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-c_time'],
                'verbose_name_plural': '资产总表',
                'verbose_name': '资产总表',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='业务线', max_length=64)),
                ('memo', models.CharField(blank=True, null=True, verbose_name='备注', max_length=64)),
                ('parent_unit', models.ForeignKey(related_name='parent_level', blank=True, null=True, to='assets.BusinessUnit')),
            ],
            options={
                'verbose_name_plural': '业务线',
                'verbose_name': '业务线',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sn', models.CharField(unique=True, verbose_name='合同号', max_length=128)),
                ('name', models.CharField(verbose_name='合同名称', max_length=64)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('price', models.IntegerField(verbose_name='合同金额')),
                ('detail', models.TextField(blank=True, null=True, verbose_name='合同详细')),
                ('start_day', models.DateField(blank=True, null=True, verbose_name='开始日期')),
                ('end_day', models.DateField(blank=True, null=True, verbose_name='失效日期')),
                ('license_num', models.IntegerField(blank=True, null=True, verbose_name='license数量')),
                ('c_day', models.DateField(verbose_name='创建日期', auto_now_add=True)),
                ('m_day', models.DateField(verbose_name='修改日期', auto_now=True)),
            ],
            options={
                'verbose_name_plural': '合同',
                'verbose_name': '合同',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('cpu_model', models.CharField(blank=True, null=True, verbose_name='CPU型号', max_length=128)),
                ('cpu_count', models.PositiveSmallIntegerField(verbose_name='物理CPU个数', default=1)),
                ('cpu_core_count', models.PositiveSmallIntegerField(verbose_name='CPU核数', default=1)),
                ('asset', models.OneToOneField(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': 'CPU',
                'verbose_name': 'CPU',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sn', models.CharField(verbose_name='硬盘SN号', max_length=128)),
                ('slot', models.CharField(blank=True, null=True, verbose_name='所在插槽位', max_length=64)),
                ('model', models.CharField(blank=True, null=True, verbose_name='磁盘型号', max_length=128)),
                ('manufacturer', models.CharField(blank=True, null=True, verbose_name='磁盘制造商', max_length=128)),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='磁盘容量(GB)')),
                ('interface_type', models.CharField(max_length=16, choices=[('SATA', 'SATA'), ('SAS', 'SAS'), ('SCSI', 'SCSI'), ('SSD', 'SSD'), ('unknown', 'unknown')], verbose_name='接口类型', default='unknown')),
                ('asset', models.ForeignKey(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '硬盘',
                'verbose_name': '硬盘',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='事件名称', max_length=128)),
                ('event_type', models.SmallIntegerField(choices=[(0, '其它'), (1, '硬件变更'), (2, '新增配件'), (3, '设备下线'), (4, '设备上线'), (5, '定期维护'), (6, '业务上线\\更新\\变更')], verbose_name='事件类型', default=4)),
                ('component', models.CharField(blank=True, null=True, verbose_name='事件子项', max_length=256)),
                ('detail', models.TextField(verbose_name='事件详情')),
                ('date', models.DateTimeField(verbose_name='事件时间', auto_now_add=True)),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '事件纪录',
                'verbose_name': '事件纪录',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='机房名称', max_length=64)),
                ('memo', models.CharField(blank=True, null=True, verbose_name='备注', max_length=128)),
            ],
            options={
                'verbose_name_plural': '机房',
                'verbose_name': '机房',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='厂商名称', max_length=64)),
                ('telephone', models.CharField(blank=True, null=True, verbose_name='支持电话', max_length=30)),
                ('memo', models.CharField(blank=True, null=True, verbose_name='备注', max_length=128)),
            ],
            options={
                'verbose_name_plural': '厂商',
                'verbose_name': '厂商',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '路由器'), (1, '交换机'), (2, '负载均衡'), (4, 'VPN设备')], verbose_name='网络设备类型', default=0)),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VLanIP')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网IP')),
                ('model', models.CharField(blank=True, null=True, verbose_name='网络设备型号', max_length=128)),
                ('firmware', models.CharField(blank=True, null=True, verbose_name='设备固件版本', max_length=128)),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='详细配置')),
                ('asset', models.OneToOneField(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网络设备',
                'verbose_name': '网络设备',
            },
        ),
        migrations.CreateModel(
            name='NewAssetApprovalZone',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sn', models.CharField(unique=True, verbose_name='资产SN号', max_length=128)),
                ('asset_type', models.CharField(verbose_name='资产类型', default='server', choices=[('server', '服务器'), ('networkdevice', '网络设备'), ('storagedevice', '存储设备'), ('securitydevice', '安全设备'), ('IDC', '机房'), ('software', '软件资产')], blank=True, null=True, max_length=64)),
                ('manufacturer', models.CharField(blank=True, null=True, verbose_name='生产厂商', max_length=64)),
                ('model', models.CharField(blank=True, null=True, verbose_name='型号', max_length=128)),
                ('ram_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='内存大小')),
                ('cpu_model', models.CharField(blank=True, null=True, verbose_name='CPU型号', max_length=128)),
                ('cpu_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cpu_core_count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('os_distribution', models.CharField(blank=True, null=True, max_length=64)),
                ('os_type', models.CharField(blank=True, null=True, max_length=64)),
                ('os_release', models.CharField(blank=True, null=True, max_length=64)),
                ('data', models.TextField(verbose_name='资产数据')),
                ('c_time', models.DateTimeField(verbose_name='汇报日期', auto_now_add=True)),
                ('m_time', models.DateTimeField(verbose_name='数据更新日期', auto_now=True)),
                ('approved', models.BooleanField(verbose_name='是否批准', default=False)),
            ],
            options={
                'ordering': ['-c_time'],
                'verbose_name_plural': '新上线待批准资产',
                'verbose_name': '新上线待批准资产',
            },
        ),
        migrations.CreateModel(
            name='NIC',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(blank=True, null=True, verbose_name='网卡名称', max_length=64)),
                ('model', models.CharField(verbose_name='网卡型号', max_length=128)),
                ('mac', models.CharField(verbose_name='MAC地址', max_length=64)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('net_mask', models.CharField(blank=True, null=True, verbose_name='掩码', max_length=64)),
                ('bonding', models.CharField(blank=True, null=True, verbose_name='绑定地址', max_length=64)),
                ('asset', models.ForeignKey(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '网卡',
                'verbose_name': '网卡',
            },
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sn', models.CharField(blank=True, null=True, verbose_name='SN号', max_length=128)),
                ('model', models.CharField(blank=True, null=True, verbose_name='内存型号', max_length=128)),
                ('manufacturer', models.CharField(blank=True, null=True, verbose_name='内存制造商', max_length=128)),
                ('slot', models.CharField(verbose_name='插槽', max_length=64)),
                ('capacity', models.IntegerField(blank=True, null=True, verbose_name='内存大小(GB)')),
                ('asset', models.ForeignKey(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '内存',
                'verbose_name': '内存',
            },
        ),
        migrations.CreateModel(
            name='SecurityDevice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '防火墙'), (1, '入侵检测设备'), (2, '互联网网关'), (4, '运维审计系统')], verbose_name='安全设备类型', default=0)),
                ('asset', models.OneToOneField(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '安全设备',
                'verbose_name': '安全设备',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, 'PC服务器'), (1, '刀片机'), (2, '小型机')], verbose_name='服务器类型', default=0)),
                ('created_by', models.CharField(max_length=32, choices=[('auto', '自动添加'), ('manual', '手工录入')], verbose_name='添加方式', default='auto')),
                ('model', models.CharField(blank=True, null=True, verbose_name='服务器型号', max_length=128)),
                ('raid_type', models.CharField(blank=True, null=True, verbose_name='Raid类型', max_length=512)),
                ('os_type', models.CharField(blank=True, null=True, verbose_name='操作系统类型', max_length=64)),
                ('os_distribution', models.CharField(blank=True, null=True, verbose_name='发行版本', max_length=64)),
                ('os_release', models.CharField(blank=True, null=True, verbose_name='操作系统版本', max_length=64)),
                ('asset', models.OneToOneField(to='assets.Asset')),
                ('hosted_on', models.ForeignKey(related_name='hosted_on_server', blank=True, verbose_name='宿主机', null=True, to='assets.Server')),
            ],
            options={
                'verbose_name_plural': '服务器',
                'verbose_name': '服务器',
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '操作系统'), (1, '办公\\开发软件'), (2, '业务软件')], verbose_name='软件类型', default=0)),
                ('license_num', models.IntegerField(verbose_name='授权数量', default=1)),
                ('version', models.CharField(unique=True, verbose_name='软件/系统版本', help_text='例如: CentOS release 6.7 (Final)', max_length=64)),
            ],
            options={
                'verbose_name_plural': '软件/系统',
                'verbose_name': '软件/系统',
            },
        ),
        migrations.CreateModel(
            name='StorageDevice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('sub_asset_type', models.SmallIntegerField(choices=[(0, '磁盘阵列'), (1, '网络存储器'), (2, '磁带库'), (4, '磁带机')], verbose_name='存储设备类型', default=0)),
                ('asset', models.OneToOneField(to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': '存储设备',
                'verbose_name': '存储设备',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(unique=True, verbose_name='标签名', max_length=32)),
                ('c_day', models.DateField(verbose_name='创建日期', auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '标签',
                'verbose_name': '标签',
            },
        ),
        migrations.AddField(
            model_name='eventlog',
            name='new_asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, null=True, to='assets.NewAssetApprovalZone'),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, verbose_name='事件执行人', null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, verbose_name='所属业务线', null=True, to='assets.BusinessUnit'),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ForeignKey(blank=True, verbose_name='合同', null=True, to='assets.Contract'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, verbose_name='所在机房', null=True, to='assets.IDC'),
        ),
        migrations.AddField(
            model_name='asset',
            name='manufacturer',
            field=models.ForeignKey(blank=True, verbose_name='制造商', null=True, to='assets.Manufacturer'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tags',
            field=models.ManyToManyField(blank=True, verbose_name='标签', to='assets.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([('asset', 'slot')]),
        ),
        migrations.AlterUniqueTogether(
            name='nic',
            unique_together=set([('asset', 'model', 'mac')]),
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([('asset', 'sn')]),
        ),
    ]
