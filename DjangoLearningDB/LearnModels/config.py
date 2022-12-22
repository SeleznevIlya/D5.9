news = 'NS'
article = 'AR'
TYPE = [
        (news, 'Новости'),
        (article, 'Статья'),
    ]

# class SimpleMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         response = self.get_response(request)
#         if request.mobile:
#             prefix = 'mobile/'
#         else:
#             prefix = 'posts/'
#
#         response.template_name = prefix + response.template_name
#         return response
