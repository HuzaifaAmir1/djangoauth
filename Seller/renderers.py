from rest_framework import renderers

class CustomStatusRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            'status_code': renderer_context['response'].status_code,
            'data': data
        }
        return super().render(response, accepted_media_type, renderer_context)
