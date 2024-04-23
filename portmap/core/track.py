from .models import TrackArticleView

def track_view(request, article):
  article_visited = article
  article_path = request.path
  referrer = request.META.get('HTTP_REFERER')
  visited_directly = not bool(referrer) # If there's no referrer, it's visited directly
  TrackArticleView.objects.create(article=article_visited, article_path=article_path, visited_directly=visited_directly, external_referrer=referrer)