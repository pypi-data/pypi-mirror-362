from irlpdf import cli,__app_name__

def start():
    cli.app(prog_name=__app_name__)
    
if __name__=="__main__":
    start()