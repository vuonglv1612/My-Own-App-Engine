from fastapi import FastAPI

app = FastAPI()


@app.post("/build-from-zip")
def build_from_zip():
    pass


@app.post("/build-from-git")
def build_from_git():
    pass
