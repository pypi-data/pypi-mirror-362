from app import create_app
from app.api.deps import get_settings
app = create_app(get_settings())
