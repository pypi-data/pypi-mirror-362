from .commands import app

if __name__ == "__main__":
    import sys
    if len(sys.argv)==1:
        app(["about"])
    else:
        app()
