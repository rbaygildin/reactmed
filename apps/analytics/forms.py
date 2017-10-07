from django.forms import Form, CharField


class VisualizationParamsForm(Form):
    test = CharField(max_length=50)
    class_col = CharField(max_length=50)
