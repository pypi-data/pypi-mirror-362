from markupsafe import Markup

__version__ = "0.1.0"

class Quill:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.jinja_env.globals['quill'] = self

    def load(self):
        return Markup('''
<link href="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.js"></script>
''')

    def create_editor(self, field_id):
        return Markup(f'''
<div id="editor"></div>
<input type="hidden" name="{field_id}" id="{field_id}">
<script>
  let quill;
  document.addEventListener('DOMContentLoaded', function () {{
    quill = new Quill('#editor', {{ theme: 'snow' }});
    document.querySelector('form').onsubmit = function() {{
      document.querySelector('#{field_id}').value = quill.root.innerHTML;
    }};
  }});
</script>
''')

    def config(self, name):
        """
        指定したname属性のtextareaをQuillエディタ化するJSを出力します。
        Bootstrap5のrender_formと併用可能。
        """
        return Markup(f'''
<script>
  document.addEventListener('DOMContentLoaded', function () {{
    var textarea = document.querySelector("textarea[name='{name}']");
    if (textarea) {{
      textarea.style.display = "none";
      textarea.removeAttribute("required");
      var quillDiv = document.createElement("div");
      quillDiv.id = "quill-container-{name}";
      quillDiv.style.height = "150px";
      textarea.parentNode.insertBefore(quillDiv, textarea);
      var quill = new Quill(quillDiv, {{ theme: "snow" }});
      quill.root.innerHTML = textarea.value;
      textarea.form.onsubmit = function () {{
        textarea.value = quill.root.innerHTML;
      }};
    }}
  }});
</script>
''')