"""
Tests for Q-Memetic AI License System.

Tests the strict QuantumMeta license integration and enforcement.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from qmemetic_ai.licensing.manager import (
    LicenseManager,
    QMemeticLicenseError,
    validate_qmemetic_license,
    requires_license,
    _get_machine_id
)


class TestLicenseManager:
    """Test the LicenseManager class."""
    
    def test_machine_id_generation(self):
        """Test that machine ID is generated consistently."""
        machine_id_1 = _get_machine_id()
        machine_id_2 = _get_machine_id()
        
        assert machine_id_1 == machine_id_2
        assert len(machine_id_1) == 16
        assert isinstance(machine_id_1, str)
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', False)
    def test_license_manager_without_quantummeta(self):
        """Test license manager when QuantumMeta library is not available."""
        with pytest.raises(QMemeticLicenseError) as exc_info:
            LicenseManager()
        
        assert "quantummeta-license" in str(exc_info.value).lower()
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_license_manager_with_valid_license(self, mock_validate):
        """Test license manager with valid license."""
        mock_validate.return_value = True
        
        # Should not raise an exception
        manager = LicenseManager(license_key="test-key")
        assert manager.license_key == "test-key"
        assert manager.package_name == "qmemetic-ai"
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_license_manager_with_expired_license(self, mock_validate):
        """Test license manager with expired license."""
        from qmemetic_ai.licensing.manager import LicenseExpiredError
        mock_validate.side_effect = LicenseExpiredError("License expired")
        
        with pytest.raises(QMemeticLicenseError) as exc_info:
            LicenseManager(license_key="expired-key")
        
        assert "expired" in str(exc_info.value).lower()
    
    def test_license_status_without_quantummeta(self):
        """Test license status when QuantumMeta is not available."""
        with patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', False):
            with patch('qmemetic_ai.licensing.manager.validate_or_grace'):
                manager = LicenseManager.__new__(LicenseManager)  # Skip __init__
                manager.machine_id = "test-machine"
                manager.package_name = "qmemetic-ai"
                
                status = manager.get_license_status()
                
                assert status["valid"] is False
                assert "quantummeta" in status["error"].lower()
                assert status["machine_id"] == "test-machine"


class TestLicenseDecorators:
    """Test license enforcement decorators."""
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_requires_license_decorator_success(self, mock_validate):
        """Test requires_license decorator with valid license."""
        mock_validate.return_value = True
        
        @requires_license(features=["basic_evolution"])
        def test_function():
            return "success"
        
        result = test_function()
        assert result == "success"
        mock_validate.assert_called_with("qmemetic-ai", required_features=["basic_evolution"], grace_days=1)
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', False)
    def test_requires_license_decorator_no_quantummeta(self):
        """Test requires_license decorator without QuantumMeta library."""
        @requires_license(features=["basic_evolution"])
        def test_function():
            return "success"
        
        with pytest.raises(QMemeticLicenseError) as exc_info:
            test_function()
        
        assert "quantummeta-license" in str(exc_info.value).lower()
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_requires_license_decorator_feature_not_licensed(self, mock_validate):
        """Test requires_license decorator when feature is not licensed."""
        from qmemetic_ai.licensing.manager import FeatureNotLicensedError
        mock_validate.side_effect = FeatureNotLicensedError("Feature not licensed")
        
        @requires_license(features=["advanced_evolution"])
        def test_function():
            return "success"
        
        with pytest.raises(QMemeticLicenseError) as exc_info:
            test_function()
        
        assert "higher license tier" in str(exc_info.value).lower()


class TestLicenseValidation:
    """Test the validate_qmemetic_license function."""
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', False)
    def test_validate_without_quantummeta(self):
        """Test validation without QuantumMeta library."""
        with pytest.raises(QMemeticLicenseError) as exc_info:
            validate_qmemetic_license()
        
        assert "quantummeta-license" in str(exc_info.value).lower()
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_validate_with_valid_license(self, mock_validate):
        """Test validation with valid license."""
        mock_validate.return_value = True
        
        # Should not raise an exception
        validate_qmemetic_license()
        mock_validate.assert_called_with("qmemetic-ai", required_features=None, grace_days=1)
    
    @patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True)
    @patch('qmemetic_ai.licensing.manager.validate_or_grace')
    def test_validate_with_features(self, mock_validate):
        """Test validation with specific features."""
        mock_validate.return_value = True
        
        validate_qmemetic_license(features=["entanglement", "quantum_walk"])
        mock_validate.assert_called_with("qmemetic-ai", required_features=["entanglement", "quantum_walk"], grace_days=1)


class TestLicenseIntegration:
    """Integration tests for license system."""
    
    def test_grace_period_constant(self):
        """Test that grace period is set to 24 hours (1 day)."""
        # This test ensures the grace period is always 24 hours as specified
        with patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True):
            with patch('qmemetic_ai.licensing.manager.validate_or_grace') as mock_validate:
                mock_validate.return_value = True
                
                manager = LicenseManager()
                
                # Check that all validate_or_grace calls use grace_days=1
                for call in mock_validate.call_args_list:
                    if 'grace_days' in call.kwargs:
                        assert call.kwargs['grace_days'] == 1
    
    def test_package_name_consistency(self):
        """Test that package name is consistent across the system."""
        with patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True):
            with patch('qmemetic_ai.licensing.manager.validate_or_grace') as mock_validate:
                mock_validate.return_value = True
                
                manager = LicenseManager()
                assert manager.package_name == "qmemetic-ai"
                
                # Check validate_qmemetic_license uses same package name
                validate_qmemetic_license()
                mock_validate.assert_called_with("qmemetic-ai", required_features=None, grace_days=1)


class TestErrorMessages:
    """Test that license error messages are user-friendly and informative."""
    
    def test_error_message_includes_support_info(self):
        """Test that license errors include support information."""
        error = QMemeticLicenseError("Test error")
        error_str = str(error)
        
        assert "bajpaikrishna715@gmail.com" in error_str
        assert "machine id" in error_str.lower()  # Check for lowercase version
    
    def test_error_message_includes_machine_id(self):
        """Test that error messages include machine ID."""
        machine_id = "test-machine-123"
        error = QMemeticLicenseError("Test error", machine_id=machine_id)
        error_str = str(error)
        
        assert machine_id in error_str


# Test fixtures and utilities
@pytest.fixture
def mock_license_manager():
    """Create a mock license manager for testing."""
    with patch('qmemetic_ai.licensing.manager.QUANTUMMETA_AVAILABLE', True):
        with patch('qmemetic_ai.licensing.manager.validate_or_grace') as mock_validate:
            mock_validate.return_value = True
            manager = LicenseManager(license_key="test-key")
            yield manager


def test_development_mode_detection():
    """Test that development mode is properly detected."""
    # Test environment variable detection
    with patch.dict(os.environ, {'QMEMETIC_DEV': '1'}):
        # Development mode should be detected by the system
        pass  # This would be implemented based on actual dev mode detection logic


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
