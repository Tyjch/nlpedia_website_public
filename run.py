# coding=utf-8
from nlpedia import create_app
import os

app = create_app()

# For Heroku
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
