from datetime import datetime
from django import forms
from django.contrib import messages
from django.db.models import Q, F, Count, Sum, Avg, Max, Min, Value, Case, When
from django.db.models.functions import Coalesce, Concat, Length, Lower, Upper, Substr
from django.apps import apps
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import path
from django.core.cache import cache


class QueryExecutorForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 80,
            'placeholder': 'e.g., Model.objects.filter(field=value)',
            'style': 'font-family: monospace; width: 100%;'
        }),
        label='Django Query',
        help_text='Enter a Django ORM query. Supports Q(), Count(), and other Django model functions.',
        required=True
    )

    save_to_favorites = forms.BooleanField(
        label='Save to favorites',
        help_text='Save this query to your favorites for quick access',
        required=False,
        initial=False
    )

    query_name = forms.CharField(
        label='Query name (for favorites)',
        help_text='Give this query a memorable name',
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'e.g., Active items with matches'})
    )


class QueryExecutorMixin:
    """
    Mixin that adds Django query execution capability to ModelAdmin classes.
    Allows pasting and executing Django ORM queries directly in the admin interface.
    """

    # Override this in your ModelAdmin to provide custom example queries
    query_examples = []

    # Override to set custom history limit (default 5)
    query_history_limit = 5

    class Media:
        css = {
            'all': ('admin/css/query_executor_dark_mode.css',)
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('execute-query/', self.admin_site.admin_view(self.execute_query_ajax), name='%s_%s_execute_query' % (self.model._meta.app_label, self.model._meta.model_name)),
            path('delete-query-favorite/', self.admin_site.admin_view(self.delete_query_favorite), name='%s_%s_delete_query_favorite' % (self.model._meta.app_label, self.model._meta.model_name)),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Add query executor data to the changelist
        extra_context['has_execute_query'] = True
        extra_context['model_name'] = self.model.__name__
        extra_context['query_history'] = self._get_query_history(request)[:self.query_history_limit]
        extra_context['query_favorites'] = self._get_query_favorites(request)
        extra_context['query_examples'] = self.get_query_examples()
        extra_context['opts'] = self.model._meta

        # Ensure we use the template that includes the query executor interface
        # Only set if no custom template is already configured
        if not hasattr(self, 'change_list_template') or self.change_list_template is None:
            self.change_list_template = 'admin/query_executor_change_list.html'

        # Check if we have a query filter applied
        if 'query_ids' in request.session and request.session.get('query_model') == self.model.__name__:
            query_ids = request.session['query_ids']
            extra_context['active_query'] = request.session.get('active_query', '')
            extra_context['query_result_count'] = len(query_ids)

            # Clear query filter button
            if 'clear_query' in request.GET:
                del request.session['query_ids']
                del request.session['query_model']
                del request.session['active_query']
                return HttpResponseRedirect(request.path)

        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Apply query filter if exists
        if 'query_ids' in request.session and request.session.get('query_model') == self.model.__name__:
            query_ids = request.session['query_ids']
            qs = qs.filter(pk__in=query_ids)

        return qs

    def get_query_examples(self):
        """
        Get example queries for this model.
        Returns a list of tuples (description, query)
        """
        if self.query_examples:
            return self.query_examples

        # Default examples
        model_name = self.model.__name__
        return [
            ("All objects", f"{model_name}.objects.all()"),
            ("Filter by ID", f"{model_name}.objects.filter(id=1)"),
            ("Count objects", f"{model_name}.objects.count()"),
        ]

    def execute_query_ajax(self, request):
        """Handle AJAX query execution"""
        if request.method == 'POST':
            query_string = request.POST.get('query', '').strip()
            save_to_favorites = request.POST.get('save_to_favorites', 'false') == 'true'
            query_name = request.POST.get('query_name', '').strip()

            if not query_string:
                return JsonResponse({'success': False, 'error': 'Query is required'})

            # Save to history
            self._save_query_to_history(request, query_string)

            # Save to favorites if requested
            if save_to_favorites and query_name:
                self._save_query_to_favorites(request, query_string, query_name)

            try:
                # Parse and execute the query
                result = self._execute_django_query(query_string)

                # Check if result is a queryset
                if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
                    # Store query results in session for filtering
                    ids = list(result.values_list('pk', flat=True))
                    request.session['query_ids'] = ids
                    request.session['query_model'] = self.model.__name__
                    request.session['active_query'] = query_string

                    return JsonResponse({
                        'success': True,
                        'applied_filter': True,
                        'count': len(ids),
                        'redirect': True,  # Signal to reload the page
                        'message': f'Query executed successfully. Found {len(ids)} objects.'
                    })
                else:
                    # For non-queryset results (like count(), aggregate(), etc.)
                    return JsonResponse({
                        'success': True,
                        'query_string': query_string,
                        'is_scalar': True,
                        'raw_result': str(result),
                        'message': f'Query result: {result}'
                    })

            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    def _execute_django_query(self, query_string):
        """
        Safely execute a Django ORM query string.
        Supports common Django ORM methods and functions.
        """
        # Import additional Django ORM features
        from django.db.models import (
            Exists, OuterRef, Subquery, ExpressionWrapper,
            IntegerField, FloatField, CharField, DateField, DateTimeField,
            BooleanField, DecimalField, DurationField, EmailField, TextField,
            StdDev, Variance
        )
        from django.db.models.functions import (
            Cast, Extract, Now, TruncDate, TruncMonth, TruncYear,
            Trim, LTrim, RTrim, Replace, StrIndex
        )

        # Define allowed names for eval
        allowed_names = {
            # Models
            self.model.__name__: self.model,
            'objects': self.model.objects,

            # Query methods
            'filter': 'filter',
            'exclude': 'exclude',
            'all': 'all',
            'get': 'get',
            'first': 'first',
            'last': 'last',
            'count': 'count',
            'exists': 'exists',
            'values': 'values',
            'values_list': 'values_list',
            'order_by': 'order_by',
            'distinct': 'distinct',
            'select_related': 'select_related',
            'prefetch_related': 'prefetch_related',
            'annotate': 'annotate',
            'aggregate': 'aggregate',
            'only': 'only',
            'defer': 'defer',
            'using': 'using',
            'raw': 'raw',
            'union': 'union',
            'intersection': 'intersection',
            'difference': 'difference',

            # Lookups and expressions
            'Q': Q,
            'F': F,
            'Count': Count,
            'Sum': Sum,
            'Avg': Avg,
            'Max': Max,
            'Min': Min,
            'StdDev': StdDev,
            'Variance': Variance,
            'Value': Value,
            'Case': Case,
            'When': When,
            'Exists': Exists,
            'OuterRef': OuterRef,
            'Subquery': Subquery,
            'ExpressionWrapper': ExpressionWrapper,

            # Field types for casting
            'IntegerField': IntegerField,
            'FloatField': FloatField,
            'CharField': CharField,
            'DateField': DateField,
            'DateTimeField': DateTimeField,
            'BooleanField': BooleanField,
            'DecimalField': DecimalField,
            'DurationField': DurationField,
            'EmailField': EmailField,
            'TextField': TextField,

            # Functions
            'Coalesce': Coalesce,
            'Concat': Concat,
            'Length': Length,
            'Lower': Lower,
            'Upper': Upper,
            'Substr': Substr,
            'Cast': Cast,
            'Extract': Extract,
            'Now': Now,
            'TruncDate': TruncDate,
            'TruncMonth': TruncMonth,
            'TruncYear': TruncYear,
            'Trim': Trim,
            'LTrim': LTrim,
            'RTrim': RTrim,
            'Replace': Replace,
            'StrIndex': StrIndex,

            # Python built-ins
            'True': True,
            'False': False,
            'None': None,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'str': str,
            'int': int,
            'float': float,
            'len': len,
            'range': range,
        }

        # Replace Model.objects with actual model reference
        import re
        query_string = re.sub(
            r'\b(\w+)\.objects\b',
            lambda m: f'objects' if m.group(1) == self.model.__name__ else m.group(0),
            query_string
        )

        # Create a restricted environment
        restricted_globals = {'__builtins__': {}}
        restricted_globals.update(allowed_names)

        # Add any referenced models from the query
        # This regex finds patterns like "Model.objects" or "Model("
        model_references = re.findall(r'\b([A-Z]\w+)(?:\.objects|\()', query_string)
        for model_name in set(model_references):
            if model_name != self.model.__name__:
                try:
                    # Try to import the model from the same app first
                    try:
                        model = apps.get_model(self.model._meta.app_label, model_name)
                        restricted_globals[model_name] = model
                    except:
                        # Try to find the model in any installed app
                        for app_config in apps.get_app_configs():
                            try:
                                model = apps.get_model(app_config.label, model_name)
                                restricted_globals[model_name] = model
                                break
                            except:
                                continue
                except:
                    pass  # Model not found, will error during eval

        try:
            # Execute the query
            result = eval(query_string, restricted_globals)
            return result
        except SyntaxError as e:
            raise ValueError(f"Syntax error in query: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error executing query: {str(e)}")

    def _get_cache_key_prefix(self, request):
        """Get cache key prefix for user-specific data"""
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        return f'query_executor_{self.model._meta.app_label}_{self.model._meta.model_name}_{user_id}'

    def _save_query_to_history(self, request, query_string):
        """Save query to user's history"""
        cache_key = f'{self._get_cache_key_prefix(request)}_history'
        history = cache.get(cache_key, [])

        # Add to history (avoid duplicates)
        query_entry = {
            'query': query_string,
            'timestamp': datetime.now().isoformat(),
            'model': self.model.__name__
        }

        # Remove existing entry if present
        history = [h for h in history if h['query'] != query_string]

        # Add to beginning
        history.insert(0, query_entry)

        # Keep only last 20 queries
        history = history[:20]

        # Save for 30 days
        cache.set(cache_key, history, 60 * 60 * 24 * 30)

    def _get_query_history(self, request):
        """Get user's query history"""
        cache_key = f'{self._get_cache_key_prefix(request)}_history'
        return cache.get(cache_key, [])

    def _save_query_to_favorites(self, request, query_string, query_name):
        """Save query to user's favorites"""
        cache_key = f'{self._get_cache_key_prefix(request)}_favorites'
        favorites = cache.get(cache_key, [])

        # Create favorite entry
        favorite_entry = {
            'id': f'{self.model.__name__}_{len(favorites)}_{datetime.now().timestamp()}',
            'name': query_name,
            'query': query_string,
            'timestamp': datetime.now().isoformat(),
            'model': self.model.__name__
        }

        # Check if name already exists
        favorites = [f for f in favorites if f['name'] != query_name]

        # Add new favorite
        favorites.append(favorite_entry)

        # Keep only last 50 favorites
        favorites = favorites[:50]

        # Save permanently (or until cache is cleared)
        cache.set(cache_key, favorites, None)

        messages.success(request, f'Query saved to favorites as "{query_name}"')

    def _get_query_favorites(self, request):
        """Get user's favorite queries"""
        cache_key = f'{self._get_cache_key_prefix(request)}_favorites'
        return cache.get(cache_key, [])

    def delete_query_favorite(self, request):
        """Delete a favorite query"""
        if request.method == 'POST':
            favorite_id = request.POST.get('favorite_id')
            if favorite_id:
                cache_key = f'{self._get_cache_key_prefix(request)}_favorites'
                favorites = cache.get(cache_key, [])
                favorites = [f for f in favorites if f.get('id') != favorite_id]
                cache.set(cache_key, favorites, None)
                return JsonResponse({'success': True})

        return JsonResponse({'success': False})
