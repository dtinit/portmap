from functools import wraps

from .models import TrackArticleView

def track_view(function):
    @wraps(function)
    def _wrap_track_view(request, *args, **kwargs):
        print("Tracking: " + request.path)

        # Get event properties for tracking the view
        article_path = request.path
        allowed_attr = ['HTTP_ACCEPT','HTTP_ACCEPT_ENCODING','HTTP_HOST','HTTP_REFERER','HTTP_USER_AGENT','QUERY_STRING','REQUEST_METHOD']
        user_meta_data = {key: request.META[key] for key in allowed_attr if key in request.META}

        TrackArticleView.objects.create(article=article_path, user_meta_data=user_meta_data)
        return function(request, *args, **kwargs)
    
    return _wrap_track_view
