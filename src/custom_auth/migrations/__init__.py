from django.db.models.signals import post_migrate
from django.contrib.auth.management import (
    DEFAULT_DB_ALIAS, global_apps, router, _get_all_permissions
)
from django.conf import settings


# Custom function to crate permission fields
def custom_create_permissions(app_config,
                              verbosity=2,
                              interactive=True,
                              using=DEFAULT_DB_ALIAS,
                              apps=global_apps,
                              **kwargs):

    # Getting models to exclude from permissions
    try:
        exclude = settings.UNRECOGNIZED_PERMISSION.get(app_config.label)
    except AttributeError:
        exclude = None

    if exclude is not None and exclude.count("all") != 0:
        return

    if not app_config.models_module:
        return

    app_label = app_config.label
    try:
        app_config = apps.get_app_config(app_label)
        ContentType = apps.get_model('contenttypes', 'ContentType')
        Permission = apps.get_model('auth', 'Permission')
    except LookupError:
        return

    if not router.allow_migrate_model(using, Permission):
        return

    # This will hold the permissions we're looking for as
    # (content_type, (codename, name))
    searched_perms = []
    # The codenames and ctypes that should exist.
    ctypes = set()
    for klass in app_config.get_models():
        # Force looking up the content types in the current database
        # before creating foreign keys to them.
        ctype = ContentType.objects.db_manager(using).get_for_model(klass)

        # Excluding unrecognized models
        if exclude is None or ctype.model not in exclude:
            ctypes.add(ctype)
            for perm in _get_all_permissions(klass._meta):
                searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're
    # looking for.  We don't need to check for codenames since we already have
    # a list of the ones we're going to create.
    all_perms = set(Permission.objects.using(using).filter(
        content_type__in=ctypes,
    ).values_list(
        "content_type", "codename"
    ))

    perms = [
        Permission(codename=codename, name=name, content_type=ct)
        for ct, (codename, name) in searched_perms
        if (ct.pk, codename) not in all_perms
    ]
    Permission.objects.using(using).bulk_create(perms)
    if verbosity >= 2:
        for perm in perms:
            print("Adding permission '%s'" % perm)


# Disconnecting old function
post_migrate.disconnect(
    dispatch_uid="django.contrib.auth.management.create_permissions"
)
# Setting custom function
post_migrate.connect(
    custom_create_permissions,
    dispatch_uid="custom_create_permissions"
)
