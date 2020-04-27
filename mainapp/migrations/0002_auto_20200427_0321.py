# Generated by Django 3.0.5 on 2020-04-27 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maaplesson',
            name='a1',
            field=models.PositiveIntegerField(default=0, verbose_name='a1'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='addi',
            field=models.PositiveIntegerField(default=1, verbose_name='addi'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='ax',
            field=models.PositiveIntegerField(default=50, verbose_name='ax'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='b1',
            field=models.PositiveIntegerField(default=0, verbose_name='b1'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='c1',
            field=models.PositiveIntegerField(default=0, verbose_name='c1'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='favor_ans',
            field=models.CharField(blank=True, max_length=128, verbose_name='hist'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='favor_thresold_time',
            field=models.PositiveIntegerField(default=15, verbose_name='hist_depth'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='hist',
            field=models.CharField(blank=True, max_length=128, verbose_name='hist'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='hist_depth',
            field=models.PositiveIntegerField(default=5, verbose_name='hist_depth'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='mult',
            field=models.PositiveIntegerField(default=1, verbose_name='mult'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='no_dec_mul',
            field=models.PositiveIntegerField(default=1, verbose_name='no_dec_mul'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='no_minus',
            field=models.PositiveIntegerField(default=1, verbose_name='no_minus'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='nx',
            field=models.PositiveIntegerField(default=12, verbose_name='nx'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='ny',
            field=models.PositiveIntegerField(default=10, verbose_name='ny'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='qst_time',
            field=models.CharField(blank=True, max_length=12, verbose_name='mode'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='subt',
            field=models.PositiveIntegerField(default=1, verbose_name='subt'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='sx',
            field=models.PositiveIntegerField(default=50, verbose_name='sx'),
        ),
        migrations.AddField(
            model_name='maaplesson',
            name='two_digit',
            field=models.PositiveIntegerField(default=1, verbose_name='two_digit'),
        ),
        migrations.AlterField(
            model_name='maaplesson',
            name='ans_amount',
            field=models.PositiveIntegerField(default=1, verbose_name='ans_amount'),
        ),
        migrations.AlterField(
            model_name='maaplesson',
            name='ans_correct',
            field=models.PositiveIntegerField(default=0, verbose_name='ans_correct'),
        ),
    ]
