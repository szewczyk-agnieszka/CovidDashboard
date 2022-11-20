from dash import dcc, html
import dash
from app import app
from app import server
from layouts import world, who, others
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/world':
        return world
    elif pathname == '/apps/who':
        return who
    elif pathname == '/apps/others':
        return others
    else:
        return world


if __name__ == '__main__':
    app.run_server(debug=False)
