# Generated by Django 4.1.1 on 2022-11-06 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_friendlist_delete_friend'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='shoppingcart',
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ManyToManyField(related_name='courses', to='main.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.myuser')),
            ],
        ),
    ]