# 🧩 nyz-dynamic-design-builder

**nyz-dynamic-design-builder** is a lightweight Django-compatible Python utility for exporting model data — including `ForeignKey` and `ManyToMany` fields — into a structured `pandas.DataFrame` format. You can write it to Excel if needed.

No serializers or admin customization required. Just your model and your queryset.

---

## 📦 Installation

```bash
pip install nyz-dynamic-design-builder
```

---

## 📝 Sample Model: Blog

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(max_length=100)

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## ⚙️ Usage

```python
from nyz_dynamic_design_builder.exporter import export_data

queryset = Blog.objects.all()

df = export_data(
    query=queryset,
    field_list=["title", "content", "author", "tags", "created_at"],
    search_fk_list=["text", "name", "username", "first_name", "last_name"],
    special_fk_values={
        "author": ["username", "first_name", "last_name", "is_active"]
    },
    special_m2m_fields={
        "tags": ["name"]
    },
    ignore_m2m_fields=["id", "created_at", "updated_at"]
)

df.to_excel("blog_export.xlsx", index=False)
```

---

## 🔍 Parameters Explained

| Parameter            | Description |
|----------------------|-------------|
| `query`              | Django queryset (e.g. `Blog.objects.all()`) |
| `field_list`         | Fields to export from the model (including FK/M2M) |
| `search_fk_list`     | List of attributes to try in FK fields (fallback order) |
| `special_fk_values`  | Dict: FK field -> list of subfields to extract |
| `special_m2m_fields` | Dict: M2M field -> list of subfields to extract |
| `ignore_m2m_fields`  | M2M fields or subfields to ignore |

---

## 🧠 How It Works

- For `ForeignKey` fields:
  - If listed in `special_fk_values`, it exports the specified subfields.
  - Else, it searches through `search_fk_list` and uses the first match.
  
- For `ManyToMany` fields:
  - If listed in `special_m2m_fields`, only those subfields are exported.
  - Otherwise, all subfields are exported except those in `ignore_m2m_fields`.

---

## 📤 Output Example

Columns in the Excel might look like:

- `Title`
- `Content`
- `Author - Username`
- `Author - First Name`
- `Author - Last Name`
- `Author - Is Active`
- `Tags 1 - Name`
- `Tags 2 - Name`
- `Created At`

---

## ✅ Perfect For

- Admin-level or reporting exports
- Human-readable outputs for nested fields
- Avoiding verbose serializers or views for temporary data output
- Excel generation from any model dynamically

---

## 🔒 Notes

- You control exactly which fields and subfields are included.
- `pandas` and `openpyxl` are required.
- You can use `.to_excel()`, `.to_csv()` or any other `pandas` method after export.

---

## 📜 License

MIT