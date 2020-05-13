from app import create_app


app = create_app()

@app.cli.command()
def prueba():
    "adsfasdfa da fdasd"
    pass



if __name__ == "__main__":
    app.run()
