# Generated migration to increase amount field precision

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payme", "0004_alter_paymetransactions_account_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymetransactions",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]

