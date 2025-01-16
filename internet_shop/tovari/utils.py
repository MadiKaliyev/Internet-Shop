from tovari.models import Products
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Products.objects.filter(id=int(query))
    
    vector = SearchVector('name', 'discription')
    search_query = SearchQuery(query)
    
    result = Products.objects.annotate(
        rank=SearchRank(vector, search_query)
    ).filter(rank__gt=0).order_by('-rank')
    
    result = result.annotate(
        headline=SearchHeadline('name', search_query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>'),
        bodyline=SearchHeadline('discription', search_query, start_sel='<span style="background-color: yellow;">', stop_sel='</span>')
    )

    return result
