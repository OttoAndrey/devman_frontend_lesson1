import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

excel_data_wines = pandas.read_excel('files/wine.xlsx', sheet_name='Wines', keep_default_na=False)

grouped_by_category_wines = collections.defaultdict(list)
for wine in excel_data_wines.to_dict(orient='records'):
    grouped_by_category_wines[wine['category']].append(wine)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

delta = datetime.date.today() - datetime.date(year=1920, month=1, day=1)
age_place = int(delta.total_seconds() / 60 / 60 / 24 / 365.25)

template = env.get_template('template.html')

rendered_page = template.render(
    age_place=age_place,
    wine_bottles=dict(grouped_by_category_wines).items(),
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
