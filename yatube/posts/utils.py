from django.core.paginator import Paginator

POSTS_PER_PAGE = 10


def paginate_page(request, object_list, post_per_page=POSTS_PER_PAGE):
    paginator = Paginator(object_list, post_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
