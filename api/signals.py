from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.cache import cache
import hashlib, time

User = get_user_model()

def invalidate_user_list_caches():
    try:
        from django.core.cache import caches
        c = caches['default']
    
        c.clear()
    except Exception:
        pass

@receiver(post_save, sender=User)
def on_user_saved(sender, instance, **kwargs):
    invalidate_user_list_caches()

@receiver(post_delete, sender=User)
def on_user_deleted(sender, instance, **kwargs):
    invalidate_user_list_caches()
