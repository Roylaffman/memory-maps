# Generated migration to convert geometry field to PostGIS

from django.contrib.gis.db import models as gis_models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memory_maps', '0003_photo_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mapfeature',
            name='geometry',
            field=gis_models.GeometryField(
                help_text='PostGIS geometry (Point or Polygon)',
                srid=4326,
                spatial_index=True
            ),
        ),
    ]
