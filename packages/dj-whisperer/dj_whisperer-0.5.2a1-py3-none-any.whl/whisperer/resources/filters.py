import sys

from whisperer.models import EventQueue, Webhook, WebhookEvent

if sys.version_info.major == 3:
    from django_filters import FilterSet, filters

    class WebhookFilterPY3(FilterSet):
        target_url = filters.CharFilter(field_name="target_url", lookup_expr="iexact")
        event_type = filters.CharFilter(field_name="event_type", lookup_expr="iexact")
        is_active = filters.BooleanFilter(field_name="is_active")

        class Meta:
            model = Webhook
            fields = ('target_url', 'is_active', 'event_type')

    class WebhookEventFilterPY3(FilterSet):
        event_type = filters.CharFilter(
            field_name='webhook__event_type', lookup_expr='iexact'
        )

        class Meta:
            model = WebhookEvent
            fields = {
                'uuid': ['exact'],
                'response_http_status': ['exact'],
                'delivered': ['exact'],
                'created_date': ['exact', 'gt', 'gte', 'lt', 'lte'],
                'object_id': ['exact'],
                'content_type': ['exact'],
                'webhook': ['exact'],
            }

    class EventQueueFilterPY3(FilterSet):
        event_type = filters.CharFilter(field_name="event_type", lookup_expr="iexact")

        class Meta:
            model = EventQueue
            fields = ('event_type',)

    WebhookFilter = WebhookFilterPY3
    WebhookEventFilter = WebhookEventFilterPY3
    EventQueueFilter = EventQueueFilterPY3
else:
    import rest_framework_filters as PY2Filters

    class WebhookFilterPY2(PY2Filters.FilterSet):
        target_url = PY2Filters.CharFilter(name="target_url", lookup_expr="iexact")
        event_type = PY2Filters.CharFilter(name="event_type", lookup_expr="iexact")
        is_active = PY2Filters.BooleanFilter(name='is_active')

        class Meta:
            model = Webhook
            fields = ('target_url', 'is_active', 'event_type')

    class WebhookEventFilterPY2(PY2Filters.FilterSet):
        event_type = PY2Filters.CharFilter(
            name='webhook__event_type', lookup_expr='iexact'
        )
        created_date = PY2Filters.DateTimeFilter(name='created_date')
        created_date__gt = PY2Filters.DateTimeFilter(
            name='created_date', lookup_expr='gt'
        )
        created_date__gte = PY2Filters.DateTimeFilter(
            name='created_date', lookup_expr='gte'
        )
        created_date__lt = PY2Filters.DateTimeFilter(
            name='created_date', lookup_expr='lt'
        )
        created_date__lte = PY2Filters.DateTimeFilter(
            name='created_date', lookup_expr='lte'
        )
        delivered = PY2Filters.BooleanFilter(name='delivered')
        object_id = PY2Filters.CharFilter(name='object_id', lookup_expr='exact')

        class Meta:
            model = WebhookEvent
            fields = (
                'uuid',
                'event_type',
                'response_http_status',
                'delivered',
                'created_date',
                'created_date__gt',
                'created_date__gte',
                'created_date__lt',
                'created_date__lte',
                'object_id',
                'content_type',
                'webhook',
            )

    class EventQueueFilterPY2(PY2Filters.FilterSet):
        event_type = PY2Filters.CharFilter(name="event_type", lookup_expr="iexact")

        class Meta:
            model = EventQueue
            fields = ('event_type',)

    WebhookFilter = WebhookFilterPY2
    WebhookEventFilter = WebhookEventFilterPY2
    EventQueueFilter = EventQueueFilterPY2
