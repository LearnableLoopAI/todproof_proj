from django.contrib import admin
from .models import Message
from .models import Translation
from .models import Assignment
# from .models import User
from .models import Sentence
from .models import Lookup
from .models import Edit
from .models import Contribution

admin.site.register(Message)
admin.site.register(Translation)
admin.site.register(Assignment)
# admin.site.register(User)
admin.site.register(Sentence)
admin.site.register(Lookup)
admin.site.register(Edit)
admin.site.register(Contribution)