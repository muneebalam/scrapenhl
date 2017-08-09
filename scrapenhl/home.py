import dash_core_components as dcc
import dash_html_components as html
import dash

app = dash.Dash()

markdown_text = '''
### scrapenhl

This is a python package to help you scrape, manipulate, and visualize hockey data. 
Date last updated: _____
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text)
])

### TODO add links to other pages
### TODO add button to autoupdate()

if __name__ == '__main__':
    app.run_server()