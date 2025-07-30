# Flask-Quill

Flask アプリで Quill リッチテキストエディタを簡単に使える拡張です。

## インストール

```bash
pip install flask_quill
```

## 使い方

1. Flask アプリに拡張を登録（Bootstrap5 も利用する場合）

```python
from flask import Flask, render_template
from flask_quill import Quill
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
quill = Quill(app)
bootstrap5 = Bootstrap5(app)
```

2. WTForms でフィールドを定義

```python
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired
from flask_quill.fields import QuillField

class PostForm(FlaskForm):
    body = QuillField('本文', validators=[DataRequired()])
    submit = SubmitField('送信')
```

3. テンプレートでエディタを表示（Bootstrap5 の render_form を利用）

```jinja
{{ quill.load() }}
{{ quill.config(name='body') }}
{{ render_form(form, novalidate=True, button_map={"submit": "primary"}) }}
```

- Bootstrap5 の render_form と組み合わせて使えます。
- Quill エディタの内容は自動的に textarea に反映され、サーバーに送信されます。

## ライセンス

MIT
