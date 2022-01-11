from starlette.applications import Starlette
from server.urls import urlpatterns
import uvicorn
import click
from server.settings import SERVER
import IPython

# def greeter(**kwargs):
#     output = '{0}, {1}!'.format(kwargs['greeting'],
#                                 kwargs['name'])
#     if kwargs['caps']:
#         output = output.upper()
#     print(output)

@click.group()
def args():
    pass

@args.command()
@click.option("--port", default=8000, show_default=True)
@click.option("--host", default="localhost", show_default=True)
# @click.option("-h", default="localhost", show_default=True)
# @click.option("-p", default=8000, show_default=True)
def runserver(**kwargs):
    uvicorn.run("server.settings:app", host=kwargs.get("host"), port=kwargs.get("port"), log_level="info", debug=SERVER.DEBUG)
    pass

@args.command()
def shell():
    IPython.embed()
    pass

@args.command()
def test():
    # print("tests")
    print("DEBUG: No tests available")
    pass

app = Starlette(routes=urlpatterns)
if __name__=="__main__":
    # args()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
