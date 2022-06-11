```python
from django.conf.urls import include
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include(debug_toolbar.urls)),  # Django Debug Tool
    path("", index, name="index"),
    path("get_user/<int:user_id>", get_user),
]
```

- debug toolar에 대한 url path를 추가해줘야됨
