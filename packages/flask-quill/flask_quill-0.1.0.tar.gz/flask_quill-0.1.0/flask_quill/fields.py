from wtforms import TextAreaField

class QuillField(TextAreaField):
    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)