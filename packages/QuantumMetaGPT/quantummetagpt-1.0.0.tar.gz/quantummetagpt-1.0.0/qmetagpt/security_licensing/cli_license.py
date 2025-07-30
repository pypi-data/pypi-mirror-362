import click
from .license_manager import LicenseManager
import os
from qmetagpt.utils.logger import get_logger

logger = get_logger(__name__)

@click.group()
def cli():
    """QuantumMetaGPT License Management CLI"""

@cli.command()
@click.option('--customer', default="Quantum Research Lab", help='Customer name')
@click.option('--duration', default=365, help='License duration in days')
def generate(customer, duration):
    """Generate a new license file"""
    manager = LicenseManager()
    license_key = manager.generate_license(customer, duration)
    
    with open("license.key", "wb") as f:
        f.write(license_key)
    logger.info(f"License generated and saved to license.key")

@cli.command()
def validate():
    """Validate the current license"""
    manager = LicenseManager()
    if not os.path.exists("license.key"):
        logger.error("License file not found")
        return
    
    with open("license.key", "rb") as f:
        license_key = f.read()
    
    if manager.validate_license(license_key):
        logger.info("✅ License is valid")
    else:
        logger.error("❌ License is invalid")

@cli.command()
def info():
    """Show hardware ID and license info"""
    manager = LicenseManager()
    hw_id = manager.get_hardware_id()
    
    click.echo(f"Hardware ID: {hw_id}")
    
    if os.path.exists("license.key"):
        with open("license.key", "rb") as f:
            license_key = f.read()
        valid = manager.validate_license(license_key)
        click.echo(f"License status: {'Valid' if valid else 'Invalid'}")
    else:
        click.echo("License file: Not found")

if __name__ == '__main__':
    cli()