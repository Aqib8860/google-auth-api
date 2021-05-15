
import uvicorn

from server.settings import app, SERVER

if __name__ == "__main__":
    uvicorn.run("server.settings:app", host=SERVER.HOST, port=SERVER.PORT, log_level="info", debug=SERVER.DEBUG)