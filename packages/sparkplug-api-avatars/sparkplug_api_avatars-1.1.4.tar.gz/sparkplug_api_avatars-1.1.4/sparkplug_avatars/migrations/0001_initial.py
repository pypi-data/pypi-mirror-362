from django.db import migrations, models
import django_extensions.db.fields
import sorl.thumbnail.fields
from sparkplug_avatars.utils.get_upload_location import get_upload_location


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', django_extensions.db.fields.ShortUUIDField(blank=True, editable=False)),
                ('file', sorl.thumbnail.fields.ImageField(upload_to=get_upload_location)),
            ],
        ),
    ]
