"""Command Line Interface for CRCreditum."""

import click
import json
from typing import Dict, Any
from .schemas import CreditAssessment
from .core.config import CreditConfig
from . import __version__


@click.group()
@click.version_option(version=__version__)
def main():
    """CRCreditum - Advanced Credit Risk Assessment Platform."""
    pass


@main.command()
def version():
    """Display version information."""
    click.echo(f"CRCreditum version {__version__}")


@main.command()
@click.option('--config', '-c', help='Configuration file path')
def config(config):
    """Display current configuration."""
    try:
        credit_config = CreditConfig(config)
        config_dict = credit_config.to_dict()
        click.echo(json.dumps(config_dict, indent=2))
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)


@main.command()
@click.option('--input', '-i', required=True, help='Input JSON file with assessment data')
@click.option('--type', '-t', type=click.Choice(['individual', 'business']), 
              default='individual', help='Type of assessment')
@click.option('--enhanced', is_flag=True, help='Use enhanced assessment')
@click.option('--output', '-o', help='Output file path')
def assess(input, type, enhanced, output):
    """Perform credit assessment."""
    try:
        # Load input data
        with open(input, 'r') as f:
            data = json.load(f)
        
        # Initialize assessment engine
        assessor = CreditAssessment()
        
        # Perform assessment
        assessment_type = "enhanced" if enhanced else "basic"
        
        if type == 'individual':
            result = assessor.assess_individual(data, assessment_type=assessment_type)
        else:
            result = assessor.assess_business(data, assessment_type=assessment_type)
        
        # Output result
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"Assessment result saved to {output}")
        else:
            click.echo(json.dumps(result, indent=2))
    
    except FileNotFoundError:
        click.echo(f"Error: Input file '{input}' not found", err=True)
    except json.JSONDecodeError:
        click.echo(f"Error: Invalid JSON in input file '{input}'", err=True)
    except Exception as e:
        click.echo(f"Error performing assessment: {e}", err=True)


@main.command()
def info():
    """Display package information."""
    from . import get_package_info
    
    info = get_package_info()
    
    click.echo(f"Package: {info['name']} v{info['version']}")
    click.echo(f"Description: {info['description']}")
    click.echo("\nFeatures:")
    for feature in info['features']:
        click.echo(f"  • {feature}")
    
    click.echo(f"\nSupported Assessment Types: {', '.join(info['supported_types'])}")
    click.echo(f"Compliance Frameworks: {', '.join(info['compliance_frameworks'])}")
    click.echo(f"ML Models: {', '.join(info['ml_models'])}")


@main.command()
@click.option('--data', '-d', required=True, help='JSON data to validate')
@click.option('--type', '-t', type=click.Choice(['individual', 'business']), 
              default='individual', help='Type of data to validate')
def validate(data, type):
    """Validate assessment data format."""
    try:
        # Parse JSON data
        if data.startswith('{'):
            # Direct JSON string
            assessment_data = json.loads(data)
        else:
            # File path
            with open(data, 'r') as f:
                assessment_data = json.load(f)
        
        # Initialize assessment engine
        assessor = CreditAssessment()
        
        # Validate data
        if type == 'individual':
            result = assessor.validate_individual_data(assessment_data)
        else:
            result = assessor.validate_business_data(assessment_data)
        
        if result['valid']:
            click.echo("✅ Data validation successful")
            click.echo(result['message'])
        else:
            click.echo("❌ Data validation failed")
            click.echo(f"Error: {result['error']}", err=True)
    
    except json.JSONDecodeError:
        click.echo("Error: Invalid JSON data", err=True)
    except FileNotFoundError:
        click.echo(f"Error: File '{data}' not found", err=True)
    except Exception as e:
        click.echo(f"Error validating data: {e}", err=True)


@main.command()
@click.option('--scenario', '-s', default='ccar_baseline', 
              help='Stress test scenario name')
@click.option('--portfolio', '-p', required=True, 
              help='Portfolio data JSON file')
@click.option('--output', '-o', help='Output file path')
def stress_test(scenario, portfolio, output):
    """Run stress test analysis."""
    try:
        from .models.stress_testing import StressTestingEngine, StressTestType
        
        # Load portfolio data
        with open(portfolio, 'r') as f:
            portfolio_data = json.load(f)
        
        # Create mock model for demo
        class MockModel:
            def predict(self, X):
                return [0.7]
        
        model = MockModel()
        
        # Initialize stress testing engine
        engine = StressTestingEngine()
        
        # Run stress test
        result = engine.run_stress_test(scenario, portfolio_data, model, StressTestType.CCAR)
        
        # Convert to dict for JSON serialization
        result_dict = result.dict()
        
        # Output result
        if output:
            with open(output, 'w') as f:
                json.dump(result_dict, f, indent=2)
            click.echo(f"Stress test result saved to {output}")
        else:
            click.echo(json.dumps(result_dict, indent=2))
    
    except FileNotFoundError:
        click.echo(f"Error: Portfolio file '{portfolio}' not found", err=True)
    except Exception as e:
        click.echo(f"Error running stress test: {e}", err=True)


if __name__ == '__main__':
    main()