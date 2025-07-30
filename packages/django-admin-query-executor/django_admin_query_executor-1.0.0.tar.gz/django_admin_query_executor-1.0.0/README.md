# Django Admin Query Executor

A powerful Django admin extension that allows you to execute Django ORM queries directly from the admin interface. It supports complex queries including `Q()` objects, annotations, aggregations, and all standard Django ORM methods.

![Django Admin Query Executor](https://img.shields.io/badge/django-%3E%3D3.2-green.svg)
![Python Support](https://img.shields.io/badge/python-%3E%3D3.8-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

## Features

- **Direct Query Execution**: Execute Django ORM queries directly from the admin changelist view
- **Seamless Integration**: Query results replace the standard admin list view
- **Full Django ORM Support**: Use `Q()`, `F()`, `Count()`, `Sum()`, `Avg()`, and other Django model functions
- **Query History**: Automatically saves your recent queries for quick re-execution
- **Favorite Queries**: Save frequently used queries with custom names
- **Collapsible Interface**: Clean, collapsible UI that doesn't clutter your admin
- **Comprehensive Dark Mode Support**:
  - Automatically adapts to system preferences
  - Compatible with Django admin's built-in dark mode
  - Works with popular admin themes (Grappelli, Jazzmin, etc.)
  - Smooth transitions between light and dark themes
  - Accessible color contrasts in both modes
- **Security**: Queries execute in a restricted environment with whitelisted functions
- **Smart Result Detection**: Automatically handles both queryset and scalar results

## Installation

```bash
pip install django-admin-query-executor
```

## Quick Start

1. Add `django_admin_query_executor` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_admin_query_executor',
    ...
]
```

2. Add the `QueryExecutorMixin` to your `ModelAdmin` classes:

```python
from django.contrib import admin
from django_admin_query_executor import QueryExecutorMixin
from .models import MyModel

@admin.register(MyModel)
class MyModelAdmin(QueryExecutorMixin, admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']

    # Optional: Define custom example queries for this model
    query_examples = [
        ("Active items", "MyModel.objects.filter(is_active=True)"),
        ("Recent items", "MyModel.objects.filter(created_at__gte=timezone.now() - timedelta(days=7))"),
        ("Count by status", "MyModel.objects.values('status').annotate(count=Count('id'))"),
    ]
```

## Usage

1. Navigate to any model's admin changelist that uses `QueryExecutorMixin`
2. Click "Execute Django Query" to expand the query interface
3. Enter your Django ORM query (e.g., `MyModel.objects.filter(status='active')`)
4. Click "Execute Query"
5. The admin list updates to show your query results

### Query Examples

```python
# Filter queries
Book.objects.filter(author__name__icontains='Smith')
Book.objects.filter(Q(title__icontains='Django') | Q(title__icontains='Python'))

# Annotations and aggregations
Book.objects.annotate(review_count=Count('reviews')).filter(review_count__gt=10)
Book.objects.aggregate(avg_price=Avg('price'), total_books=Count('id'))

# Complex queries with joins
Author.objects.filter(books__published_date__year=2023).distinct()
Book.objects.select_related('author', 'publisher').filter(price__lt=50)

# Counting and existence checks
Book.objects.filter(category='Fiction').count()
Book.objects.filter(reviews__rating__gte=4).exists()
```

## Configuration

### Custom Change List Templates

The mixin automatically overrides the ModelAdmin's `change_list_template` if the default template is in use. If your ModelAdmin uses a custom template, the template will need to extend `admin/query_executor_change_list.html`:

```
{% extends "admin/query_executor_change_list.html" %}
```

### Custom Example Queries

Define model-specific example queries by adding a `query_examples` attribute to your ModelAdmin:

```python
class BookAdmin(QueryExecutorMixin, admin.ModelAdmin):
    query_examples = [
        ("Bestsellers", "Book.objects.filter(is_bestseller=True)"),
        ("By price range", "Book.objects.filter(price__gte=20, price__lte=50)"),
        ("Review stats", "Book.objects.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=4.0)"),
    ]
```

### Customizing Query History

Control the number of queries saved in history:

```python
class BookAdmin(QueryExecutorMixin, admin.ModelAdmin):
    query_history_limit = 10  # Default is 5
```

## Supported Django ORM Features

### Query Methods
- `filter()`, `exclude()`, `get()`
- `order_by()`, `reverse()`, `distinct()`
- `values()`, `values_list()`
- `select_related()`, `prefetch_related()`
- `annotate()`, `aggregate()`
- `first()`, `last()`, `exists()`, `count()`

### Query Expressions
- `Q()` for complex queries
- `F()` for field references
- `Count()`, `Sum()`, `Avg()`, `Max()`, `Min()`
- `Case()`, `When()` for conditional expressions
- `Exists()`, `OuterRef()`, `Subquery()`

### Database Functions
- String functions: `Lower()`, `Upper()`, `Length()`, `Concat()`
- Date functions: `TruncDate()`, `Extract()`, `Now()`
- Type casting: `Cast()`, `Coalesce()`

## Dark Mode Support

The package includes comprehensive dark mode support that:

- **Auto-detects** your system's color scheme preference
- **Integrates seamlessly** with Django admin's native dark mode
- **Supports popular admin themes** including:
  - Django's built-in dark mode
  - Grappelli dark theme
  - Django Jazzmin dark mode
  - Django Admin Interface dark themes
- **Provides smooth transitions** when switching between themes
- **Ensures accessibility** with proper color contrasts
- **Includes custom CSS variables** for easy customization

### Customizing Dark Mode Colors

You can override the default colors by adding CSS variables to your admin CSS:

```css
.query-executor-container {
    --qe-bg-primary: #1a1a1a;
    --qe-text-primary: #ffffff;
    --qe-button-primary-bg: #007bff;
    /* See query_executor_dark_mode.css for all available variables */
}
```

## Security

The query executor runs in a restricted environment with:
- Whitelisted functions and classes only
- No access to private attributes or methods
- No direct database access beyond Django ORM
- No file system or network access

## Requirements

- Django >= 3.2
- Python >= 3.8

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### 1.0.0 (2025-07-17)
- Initial release
- Full Django ORM query support
- Query history and favorites
- Dark mode support
- Collapsible interface
