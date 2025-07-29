
try:
    import click
except ImportError:
    from . import click_placeholder as click
    
from .BrowserProfileCreator import BrowserProfileCreator


@click.command()
@click.option("--browser",help="Which browser type do you want? Choose firefox or chrome")
@click.option("--purpose", help="What is this browser for?")
@click.option("--dry-run", default=False, help="Which browser do you want?", is_flag=True)
def create(browser=None, purpose=None, dry_run=False):
    manager = BrowserProfileCreator()
    manager.create_profile(browser, purpose, dry_run)
    
    
if __name__ == '__main__':
    create()
