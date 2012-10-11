from django.contrib import admin
from celerytest.models import SimpleEntry, ContentProducer, \
                                SimpleUser, Condition


admin.site.register(ContentProducer)
admin.site.register(SimpleUser)
admin.site.register(Condition)
