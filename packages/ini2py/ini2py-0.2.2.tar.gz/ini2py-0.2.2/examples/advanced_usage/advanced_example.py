#!/usr/bin/env python3
"""
Advanced usage example for ini2py.

This demonstrates complex configuration management patterns including:
- Multiple database configurations
- External API management
- Security-sensitive data handling
- Performance monitoring
- Configuration validation

To run this example:
1. Navigate to this directory
2. Run: ini2py --config config.ini --output ./generated
3. Run: python advanced_example.py
"""

import sys
import time
import json
from typing import Dict, Any

# Add the generated config to Python path
sys.path.insert(0, './generated')

try:
    from generated.manager import ConfigManager
    print("✅ Successfully imported ConfigManager")
except ImportError as e:
    print(f"❌ Failed to import ConfigManager: {e}")
    print("\n🔧 To fix this, run:")
    print("   ini2py --config config.ini --output ./generated")
    sys.exit(1)


class ConfigValidator:
    """Utility class for validating configuration values."""
    
    @staticmethod
    def validate_database_config(db_config) -> bool:
        """Validate database configuration."""
        required_fields = ['host', 'port', 'database', 'username']
        for field in required_fields:
            if not hasattr(db_config, field):
                print(f"❌ Missing required database field: {field}")
                return False
        
        if db_config.port < 1 or db_config.port > 65535:
            print(f"❌ Invalid database port: {db_config.port}")
            return False
        
        if db_config.connection_pool_size < 1:
            print(f"❌ Invalid connection pool size: {db_config.connection_pool_size}")
            return False
        
        return True
    
    @staticmethod
    def validate_security_config(security_config) -> bool:
        """Validate security configuration."""
        if security_config.password_min_length < 8:
            print(f"❌ Password minimum length too short: {security_config.password_min_length}")
            return False
        
        if security_config.session_timeout < 300:  # 5 minutes
            print(f"⚠️  Warning: Session timeout very short: {security_config.session_timeout}s")
        
        return True


class ConfigurationManager:
    """Advanced configuration management wrapper."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config = ConfigManager()
        self.validator = ConfigValidator()
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Validate all configuration sections."""
        print("🔍 Validating configuration...")
        
        # Validate databases
        if not self.validator.validate_database_config(self.config.database_primary):
            raise ValueError("Invalid primary database configuration")
        
        if not self.validator.validate_database_config(self.config.database_replica):
            raise ValueError("Invalid replica database configuration")
        
        # Validate security
        if not self.validator.validate_security_config(self.config.security):
            raise ValueError("Invalid security configuration")
        
        print("✅ Configuration validation passed")
    
    def get_database_config(self, db_type: str = 'primary') -> Dict[str, Any]:
        """Get database configuration as dictionary."""
        if db_type == 'primary':
            db_config = self.config.database_primary
        elif db_type == 'replica':
            db_config = self.config.database_replica
        else:
            raise ValueError(f"Unknown database type: {db_type}")
        
        return db_config.return_properties(return_type='dict', mask_sensitive=False)
    
    def get_masked_security_info(self) -> Dict[str, Any]:
        """Get security configuration with sensitive data masked."""
        return self.config.security.return_properties(return_type='dict', mask_sensitive=True)
    
    def get_api_endpoints(self) -> Dict[str, str]:
        """Get all external API endpoints."""
        api_config = self.config.external_apis
        return {
            'payment_gateway': api_config.payment_gateway_url,
            'analytics': api_config.analytics_api_url,
            'email_service': api_config.email_service_url,
            'sms_service': api_config.sms_service_url,
        }
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature flag is enabled."""
        feature_config = self.config.feature_flags
        feature_attr = f"enable_{feature_name}"
        return getattr(feature_config, feature_attr, False)
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related settings."""
        return self.config.performance.return_properties(return_type='dict', mask_sensitive=False)


def demonstrate_basic_usage(config_mgr: ConfigurationManager):
    """Demonstrate basic configuration access."""
    print("\n🚀 Basic Configuration Access")
    print("=" * 50)
    
    config = config_mgr.config
    
    # Application server info
    print(f"App: {config.app_server.name} v{config.app_server.version}")
    print(f"Environment: {config.app_server.environment}")
    print(f"Listening on: {config.app_server.bind_host}:{config.app_server.bind_port}")
    print(f"Workers: {config.app_server.worker_processes}")
    print(f"Compression: {'Enabled' if config.app_server.enable_compression else 'Disabled'}")


def demonstrate_database_management(config_mgr: ConfigurationManager):
    """Demonstrate database configuration management."""
    print("\n🗄️  Database Configuration Management")
    print("=" * 50)
    
    # Primary database
    print("Primary Database:")
    primary_config = config_mgr.get_database_config('primary')
    print(f"  Engine: {primary_config['engine']}")
    print(f"  Host: {primary_config['host']}:{primary_config['port']}")
    print(f"  Database: {primary_config['database']}")
    print(f"  Pool Size: {primary_config['connection_pool_size']}")
    print(f"  SSL: {'Enabled' if primary_config['enable_ssl'] else 'Disabled'}")
    
    # Replica database
    print("\nReplica Database:")
    replica_config = config_mgr.get_database_config('replica')
    print(f"  Host: {replica_config['host']}:{replica_config['port']}")
    print(f"  Pool Size: {replica_config['connection_pool_size']}")
    print(f"  SSL: {'Enabled' if replica_config['enable_ssl'] else 'Disabled'}")


def demonstrate_security_features(config_mgr: ConfigurationManager):
    """Demonstrate security configuration handling."""
    print("\n🔒 Security Configuration")
    print("=" * 50)
    
    security_info = config_mgr.get_masked_security_info()
    
    print("Security Settings (sensitive data masked):")
    for key, value in security_info.items():
        print(f"  {key}: {value}")
    
    config = config_mgr.config
    print(f"\nSecurity Policies:")
    print(f"  Password Min Length: {config.security.password_min_length}")
    print(f"  Require Special Chars: {config.security.password_require_special}")
    print(f"  Session Timeout: {config.security.session_timeout}s")
    print(f"  JWT Expiry: {config.security.jwt_expiry_hours}h")
    print(f"  Rate Limiting: {'Enabled' if config.security.enable_rate_limiting else 'Disabled'}")


def demonstrate_external_apis(config_mgr: ConfigurationManager):
    """Demonstrate external API configuration."""
    print("\n🌐 External API Configuration")
    print("=" * 50)
    
    api_endpoints = config_mgr.get_api_endpoints()
    
    print("API Endpoints:")
    for service, url in api_endpoints.items():
        print(f"  {service.replace('_', ' ').title()}: {url}")
    
    config = config_mgr.config
    print(f"\nAPI Settings:")
    print(f"  Default Timeout: {config.external_apis.default_timeout}s")
    print(f"  Max Retries: {config.external_apis.max_retries}")
    print(f"  Circuit Breaker: {'Enabled' if config.external_apis.enable_circuit_breaker else 'Disabled'}")


def demonstrate_feature_flags(config_mgr: ConfigurationManager):
    """Demonstrate feature flag management."""
    print("\n🚩 Feature Flags")
    print("=" * 50)
    
    features = [
        'new_ui', 'advanced_search', 'beta_features', 
        'experimental_caching', 'async_processing'
    ]
    
    print("Feature Status:")
    for feature in features:
        status = "🟢 Enabled" if config_mgr.is_feature_enabled(feature) else "🔴 Disabled"
        print(f"  {feature.replace('_', ' ').title()}: {status}")
    
    config = config_mgr.config
    print(f"\nRollout Settings:")
    print(f"  New Algorithm Rollout: {config.feature_flags.new_algorithm_rollout_percentage}%")
    print(f"  Cache TTL: {config.feature_flags.cache_ttl_seconds}s")
    print(f"  Max Async Workers: {config.feature_flags.max_async_workers}")


def demonstrate_monitoring_config(config_mgr: ConfigurationManager):
    """Demonstrate monitoring and observability configuration."""
    print("\n📊 Monitoring & Observability")
    print("=" * 50)
    
    config = config_mgr.config
    
    print("Monitoring Settings:")
    print(f"  Metrics: {'Enabled' if config.monitoring.enable_metrics else 'Disabled'}")
    if config.monitoring.enable_metrics:
        print(f"    Port: {config.monitoring.metrics_port}")
        print(f"    Path: {config.monitoring.metrics_path}")
    
    print(f"  Health Checks: {'Enabled' if config.monitoring.enable_health_check else 'Disabled'}")
    if config.monitoring.enable_health_check:
        print(f"    Path: {config.monitoring.health_check_path}")
    
    print(f"  Tracing: {'Enabled' if config.monitoring.enable_tracing else 'Disabled'}")
    if config.monitoring.enable_tracing:
        print(f"    Endpoint: {config.monitoring.tracing_endpoint}")
        print(f"    Sample Rate: {config.monitoring.tracing_sample_rate}")
    
    print(f"  Logging:")
    print(f"    Level: {config.monitoring.log_level}")
    print(f"    Format: {config.monitoring.log_format}")
    print(f"    Structured: {'Enabled' if config.monitoring.enable_structured_logging else 'Disabled'}")


def demonstrate_performance_tuning(config_mgr: ConfigurationManager):
    """Demonstrate performance configuration."""
    print("\n⚡ Performance Configuration")
    print("=" * 50)
    
    perf_settings = config_mgr.get_performance_settings()
    
    print("Performance Settings:")
    for key, value in perf_settings.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")


def demonstrate_storage_config(config_mgr: ConfigurationManager):
    """Demonstrate backup and storage configuration."""
    print("\n💾 Backup & Storage Configuration")
    print("=" * 50)
    
    config = config_mgr.config
    
    print("Storage Settings:")
    print(f"  Type: {config.backup_storage.storage_type.upper()}")
    print(f"  Bucket: {config.backup_storage.s3_bucket}")
    print(f"  Region: {config.backup_storage.s3_region}")
    print(f"  Retention: {config.backup_storage.backup_retention_days} days")
    print(f"  Encryption: {'Enabled' if config.backup_storage.enable_encryption else 'Disabled'}")
    print(f"  Compression: {'Enabled' if config.backup_storage.compression_enabled else 'Disabled'}")
    if config.backup_storage.compression_enabled:
        print(f"    Level: {config.backup_storage.compression_level}")


def demonstrate_type_safety(config_mgr: ConfigurationManager):
    """Demonstrate type safety and inference."""
    print("\n🔢 Type Safety Demonstration")
    print("=" * 50)
    
    config = config_mgr.config
    
    # Demonstrate different types
    samples = [
        ("app_server.bind_port", config.app_server.bind_port),
        ("app_server.enable_compression", config.app_server.enable_compression),
        ("app_server.keepalive_timeout", config.app_server.keepalive_timeout),
        ("app_server.name", config.app_server.name),
        ("security.password_min_length", config.security.password_min_length),
        ("feature_flags.new_algorithm_rollout_percentage", config.feature_flags.new_algorithm_rollout_percentage),
    ]
    
    print("Type Inference Results:")
    for path, value in samples:
        print(f"  {path}: {value} ({type(value).__name__})")


def demonstrate_hot_reloading(config_mgr: ConfigurationManager):
    """Demonstrate hot reloading capabilities."""
    print("\n🔄 Hot Reloading Demonstration")
    print("=" * 50)
    
    config = config_mgr.config
    
    print("Current configuration values:")
    print(f"  App Server Port: {config.app_server.bind_port}")
    print(f"  Worker Processes: {config.app_server.worker_processes}")
    print(f"  Debug Mode: {'Enabled' if config.feature_flags.enable_beta_features else 'Disabled'}")
    
    print("\n🔧 Configuration is being monitored for changes...")
    print("Try editing config.ini and saving it to see automatic reloading!")
    print("Press Ctrl+C to exit the monitoring loop.")
    
    try:
        # Monitor some key configuration values
        last_port = config.app_server.bind_port
        last_workers = config.app_server.worker_processes
        last_debug = config.feature_flags.enable_beta_features
        
        while True:
            time.sleep(2)
            
            current_port = config.app_server.bind_port
            current_workers = config.app_server.worker_processes
            current_debug = config.feature_flags.enable_beta_features
            
            changes = []
            if current_port != last_port:
                changes.append(f"Port: {last_port} → {current_port}")
                last_port = current_port
            
            if current_workers != last_workers:
                changes.append(f"Workers: {last_workers} → {current_workers}")
                last_workers = current_workers
            
            if current_debug != last_debug:
                changes.append(f"Beta Features: {last_debug} → {current_debug}")
                last_debug = current_debug
            
            if changes:
                print(f"\n🔄 Configuration changed: {', '.join(changes)}")
            else:
                print(".", end="", flush=True)
    
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped.")


def main():
    """Main demonstration function."""
    print("🚀 ini2py Advanced Usage Example")
    print("=" * 60)
    
    try:
        # Initialize configuration manager
        config_mgr = ConfigurationManager()
        print("✅ Configuration manager initialized and validated")
        
        # Run demonstrations
        demonstrate_basic_usage(config_mgr)
        demonstrate_database_management(config_mgr)
        demonstrate_security_features(config_mgr)
        demonstrate_external_apis(config_mgr)
        demonstrate_feature_flags(config_mgr)
        demonstrate_monitoring_config(config_mgr)
        demonstrate_performance_tuning(config_mgr)
        demonstrate_storage_config(config_mgr)
        demonstrate_type_safety(config_mgr)
        
        # Interactive hot reloading demo
        print("\n" + "=" * 60)
        user_input = input("Would you like to see hot reloading in action? (y/N): ")
        if user_input.lower() in ['y', 'yes']:
            demonstrate_hot_reloading(config_mgr)
        
        print("\n✨ Advanced example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()