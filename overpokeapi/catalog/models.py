from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db.models import Model, CharField, IntegerField, JSONField, ManyToManyField, OneToOneField, CASCADE
from django.contrib.auth.models import User


class Type(Model):
    name = CharField(max_length=255, db_index=True, unique=True)


class Pokemon(Model):
    poke_id = IntegerField(db_index=True)   # Id de l'API publique
    name = CharField(max_length=255, db_index=True)
    url = CharField(max_length=2048)
    types = ManyToManyField("catalog.Type", related_name="pokemons")
    description = JSONField()


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Feeder(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    types = ManyToManyField("catalog.Type", related_name="feeders")


@receiver(post_save, sender=User)
def create_feeder(sender, instance, created, **kwargs):
    if created:
        Feeder.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_feeder(sender, instance, **kwargs):
    instance.feeder.save()