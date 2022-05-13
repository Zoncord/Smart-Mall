from django import forms


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = 'widgets/image.html'
