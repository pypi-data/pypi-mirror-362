#!/usr/bin/env python3
"""
QuantumLangChain License Management CLI

Command-line interface for managing QuantumLangChain licenses,
checking status, and troubleshooting licensing issues.

Usage:
    quantum-license status
    quantum-license info
    quantum-license activate <license_file>
    quantum-license machine-id
    quantum-license support
    quantum-license test [component]
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    from quantumlangchain.licensing import (
        LicenseManager,
        get_license_status,
        get_machine_id,
        display_license_info,
        validate_license,
        QuantumLicenseError,
        LicenseExpiredError,
        FeatureNotLicensedError,
        GracePeriodExpiredError,
        LicenseNotFoundError,
        UsageLimitExceededError,
        LICENSE_CONFIG,
        FEATURE_TIERS
    )
except ImportError:
    print("❌ Error: QuantumLangChain not installed or not in PATH")
    print("Install with: pip install quantumlangchain")
    sys.exit(1)


class QuantumLicenseCLI:
    """Command-line interface for QuantumLangChain license management."""
    
    def __init__(self):
        self.license_manager = LicenseManager()
    
    def status(self):
        """Display detailed license status."""
        print("\n" + "="*70)
        print("🧬 QuantumLangChain License Status")
        print("="*70)
        
        status = get_license_status()
        
        # Basic information
        print(f"🔧 Machine ID: {status['machine_id']}")
        print(f"📧 Contact: {status['contact_email']}")
        
        # License status
        if status["license_valid"]:
            print(f"✅ License Status: Valid")
            print(f"📊 License Tier: {status['tier'].title()}")
            if status.get("expiry_date"):
                expiry = datetime.fromisoformat(status["expiry_date"])
                days_until_expiry = (expiry - datetime.now()).days
                print(f"📅 Expires: {status['expiry_date']} ({days_until_expiry} days)")
            
            # Feature access
            features = status.get("features_available", [])
            print(f"🔧 Available Features ({len(features)}):")
            for feature in features[:10]:  # Show first 10
                print(f"   • {feature}")
            if len(features) > 10:
                print(f"   ... and {len(features) - 10} more")
        
        elif status["grace_active"]:
            hours_remaining = status["grace_remaining_hours"]
            print(f"⏰ Grace Period: {hours_remaining:.1f} hours remaining")
            
            if hours_remaining < 4:
                print("⚠️  WARNING: Grace period ending soon!")
            
            features = status.get("features_available", [])
            print(f"🔧 Evaluation Features ({len(features)}):")
            for feature in features:
                print(f"   • {feature}")
        
        else:
            print("❌ License Status: No valid license")
            print("🔒 Access: Denied (Grace period expired)")
        
        # Usage statistics
        print(f"📊 Usage Today: {status['usage_today']} operations")
        
        # Tier information
        current_tier = status.get("tier", "none")
        if current_tier in FEATURE_TIERS:
            tier_info = FEATURE_TIERS[current_tier]
            max_ops = tier_info.get("max_operations", 0)
            if max_ops == -1:
                print("📈 Operation Limit: Unlimited")
            else:
                usage_pct = (status['usage_today'] / max_ops) * 100 if max_ops > 0 else 0
                print(f"📈 Operation Limit: {status['usage_today']}/{max_ops} ({usage_pct:.1f}%)")
        
        print("="*70 + "\n")
    
    def info(self):
        """Display comprehensive licensing information."""
        display_license_info()
        
        print("\n" + "="*70)
        print("💼 Available License Tiers")
        print("="*70)
        
        for tier_name, tier_info in FEATURE_TIERS.items():
            if tier_name == "evaluation":
                continue
            
            price = tier_info.get("price", "Contact for pricing")
            max_ops = tier_info.get("max_operations", 0)
            features = tier_info.get("features", [])
            
            ops_str = "Unlimited" if max_ops == -1 else f"{max_ops:,}"
            
            print(f"\n📦 {tier_name.title()} Tier - {price}")
            print(f"   📊 Operations/Day: {ops_str}")
            print(f"   🔧 Features: {len(features)}")
            
            # Show key features
            key_features = features[:5]
            for feature in key_features:
                print(f"      • {feature}")
            if len(features) > 5:
                print(f"      • ... and {len(features) - 5} more")
        
        print(f"\n📧 Contact: {LICENSE_CONFIG['contact_email']}")
        print(f"🌐 Support: {LICENSE_CONFIG['support_url']}")
        print("="*70 + "\n")
    
    def machine_id(self):
        """Display machine ID for licensing."""
        machine_id = get_machine_id()
        print("\n" + "="*50)
        print("🔧 Machine Identification")
        print("="*50)
        print(f"Machine ID: {machine_id}")
        print("\n📋 To obtain a license:")
        print(f"1. Email: {LICENSE_CONFIG['contact_email']}")
        print(f"2. Include this Machine ID: {machine_id}")
        print("3. Specify desired license tier")
        print("4. Receive license file via email")
        print("5. Activate using: quantum-license activate <license_file>")
        print("="*50 + "\n")
    
    def activate(self, license_file):
        """Activate license from file."""
        try:
            license_path = Path(license_file)
            if not license_path.exists():
                print(f"❌ Error: License file not found: {license_file}")
                return False
            
            print(f"🔄 Activating license from: {license_file}")
            
            # TODO: Implement license activation
            print("⚠️  License activation will be implemented in future version")
            print(f"📧 Please contact {LICENSE_CONFIG['contact_email']} for manual activation")
            print(f"🔧 Machine ID: {get_machine_id()}")
            
            return False
            
        except Exception as e:
            print(f"❌ Error activating license: {e}")
            return False
    
    def support(self):
        """Display support information."""
        print("\n" + "="*60)
        print("🆘 QuantumLangChain Support")
        print("="*60)
        
        machine_id = get_machine_id()
        status = get_license_status()
        
        print("📋 When contacting support, please include:")
        print(f"   🔧 Machine ID: {machine_id}")
        print(f"   📊 Current Status: {status.get('tier', 'No license')}")
        print(f"   📈 Usage Today: {status['usage_today']}")
        print(f"   🐍 Python Version: {sys.version.split()[0]}")
        
        try:
            import quantumlangchain
            version = getattr(quantumlangchain, '__version__', 'Unknown')
            print(f"   🧬 QuantumLangChain Version: {version}")
        except:
            print("   🧬 QuantumLangChain Version: Unable to determine")
        
        print(f"\n📧 Email: {LICENSE_CONFIG['contact_email']}")
        print(f"🌐 Support: {LICENSE_CONFIG['support_url']}")
        
        print("\n💬 Common Issues:")
        print("   • License expired: Include expiry date and machine ID")
        print("   • Feature not licensed: Specify which feature and current tier")
        print("   • Usage limit exceeded: Current usage and desired limit")
        print("   • Grace period expired: Machine ID and purchase interest")
        
        print("\n⚡ Response Time: Within 24 hours")
        print("="*60 + "\n")
    
    def test(self, component=None):
        """Test license validation for components."""
        print("\n" + "="*60)
        print("🧪 QuantumLangChain License Testing")
        print("="*60)
        
        # Test cases: (component_name, features, tier)
        test_cases = [
            ("Core Package", ["core"], "basic"),
            ("QLChain", ["core", "basic_chains"], "basic"),
            ("Quantum Memory", ["core", "quantum_memory"], "basic"),
            ("Multi-Agent Systems", ["multi_agent"], "professional"),
            ("Advanced Backends", ["advanced_backends"], "professional"),
            ("Enterprise Features", ["enterprise"], "enterprise"),
            ("Research Tools", ["experimental_apis"], "research")
        ]
        
        if component:
            # Test specific component
            test_cases = [tc for tc in test_cases if component.lower() in tc[0].lower()]
            if not test_cases:
                print(f"❌ Unknown component: {component}")
                return
        
        print(f"🔧 Machine ID: {get_machine_id()}")
        print(f"📊 Testing {len(test_cases)} components...\n")
        
        results = []
        for comp_name, features, tier in test_cases:
            try:
                validate_license("quantumlangchain", features, tier)
                status = "✅ LICENSED"
                results.append((comp_name, status, ""))
                
            except LicenseExpiredError:
                status = "❌ EXPIRED"
                message = "License expired"
                results.append((comp_name, status, message))
                
            except FeatureNotLicensedError:
                status = "🔒 NOT LICENSED"
                message = f"Requires {tier} tier"
                results.append((comp_name, status, message))
                
            except GracePeriodExpiredError:
                status = "⏰ GRACE EXPIRED"
                message = "Grace period ended"
                results.append((comp_name, status, message))
                
            except LicenseNotFoundError:
                status = "⏰ GRACE PERIOD"
                message = "Evaluation mode"
                results.append((comp_name, status, message))
                
            except UsageLimitExceededError:
                status = "📊 LIMIT EXCEEDED"
                message = "Daily limit reached"
                results.append((comp_name, status, message))
                
            except Exception as e:
                status = "❌ ERROR"
                message = str(e)[:50]
                results.append((comp_name, status, message))
        
        # Display results
        for comp_name, status, message in results:
            print(f"{comp_name:<25} {status:<20} {message}")
        
        # Summary
        licensed_count = sum(1 for _, status, _ in results if "✅" in status)
        total_count = len(results)
        
        print(f"\n📊 Summary: {licensed_count}/{total_count} components licensed")
        
        if licensed_count < total_count:
            print(f"📧 For full access, contact: {LICENSE_CONFIG['contact_email']}")
        
        print("="*60 + "\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="QuantumLangChain License Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  quantum-license status              # Show license status
  quantum-license info                # Show licensing information  
  quantum-license machine-id          # Get machine ID for licensing
  quantum-license support             # Get support information
  quantum-license test                # Test all components
  quantum-license test qlchain        # Test specific component
  quantum-license activate license.qkey  # Activate license file

Contact: bajpaikrishna715@gmail.com for licensing
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show detailed license status')
    
    # Info command
    subparsers.add_parser('info', help='Show licensing information and tiers')
    
    # Machine ID command
    subparsers.add_parser('machine-id', help='Display machine ID for licensing')
    
    # Support command
    subparsers.add_parser('support', help='Display support information')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test license validation')
    test_parser.add_argument('component', nargs='?', help='Specific component to test')
    
    # Activate command
    activate_parser = subparsers.add_parser('activate', help='Activate license from file')
    activate_parser.add_argument('license_file', help='Path to license file')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create CLI instance
    cli = QuantumLicenseCLI()
    
    # Execute command
    try:
        if args.command == 'status':
            cli.status()
        elif args.command == 'info':
            cli.info()
        elif args.command == 'machine-id':
            cli.machine_id()
        elif args.command == 'support':
            cli.support()
        elif args.command == 'test':
            cli.test(getattr(args, 'component', None))
        elif args.command == 'activate':
            cli.activate(args.license_file)
        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"📧 Contact support: {LICENSE_CONFIG['contact_email']}")


if __name__ == "__main__":
    main()
