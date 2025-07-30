from django.db import models


class ForeignKey(models.ForeignKey):
    description = "Extended ForeignKey"

    def __init__(
        self, *args, related_editable=True, label="", verbose_name="", **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label  # deprecated! Remove in jan2024
        self.verbose_name = verbose_name


class ManyToManyField(models.ManyToManyField):
    description = "Extended Many to Many Field"

    def __init__(self, *args, related_editable=True, label="", **kwargs):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label  # deprecated! Remove in jan2024


class OneToOneField(models.OneToOneField):
    description = "Extended One to One Field"

    def __init__(self, *args, related_editable=True, label="", **kwargs):
        super().__init__(*args, **kwargs)
        self.related_editable = related_editable
        self.label = label  # deprecated! Remove in jan2024
