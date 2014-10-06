# django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# standard library


def paginate(request, objects, page_size=25):
    paginator = Paginator(objects, page_size)
    page = request.GET.get('p')

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects
