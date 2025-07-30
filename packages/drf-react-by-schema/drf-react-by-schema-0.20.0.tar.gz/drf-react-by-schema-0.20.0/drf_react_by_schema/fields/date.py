from django.db import models


class DateField(models.DateField):
    description = "Extended DateField"

    def __init__(self, *args, views=None, **kwargs):
        super().__init__(*args, **kwargs)
        if views:
            self.views = views
