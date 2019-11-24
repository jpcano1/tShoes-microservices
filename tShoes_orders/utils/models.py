from django.db import models

# Create your models here.

class TShoesModel(models.Model):
    """ tShoes Base model
        tShoes Model acts as an abstract base class from which
        every other model will inherit in the project. This class provides
        every table with the following attibutes:
        * created (Datetime): Stores the datetime the object was created
        * modified (Datetime): Stores the last datetime the object was modified
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was last modified'
    )
    modified = models.DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        """ Meta options """

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']