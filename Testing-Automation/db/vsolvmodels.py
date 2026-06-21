from django.core.management import call_command
from django.db import connection, models

class VSolvQueryset(models.QuerySet):

    def delete(self):
        counter, counter_dict = 0, {}
        for obj in self:
            result = obj.delete()
            if result is not None:
                current_counter, current_counter_dict = result
                counter += current_counter
                counter_dict.update(current_counter_dict)
        if counter:
            return counter, counter_dict

class VsolvModels(models.Model):
    auto_drop_schema = False
    auto_create_schema = True
    entity_id = models.BigIntegerField(null=True)
    objects = VSolvQueryset.as_manager()
    scope = None

    class Meta:
        abstract = True

    def save(self, verbosity=1, *args, **kwargs):
        super(VsolvModels, self).save(*args, **kwargs)

    def delete(self, force_drop=False, *args, **kwargs):
        return super(VsolvModels, self).delete(*args, **kwargs)