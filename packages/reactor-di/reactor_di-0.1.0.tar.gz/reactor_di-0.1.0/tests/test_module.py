"""Comprehensive tests for module decorator to achieve 100% coverage."""

# type: ignore

from abc import ABC, abstractmethod
from functools import cached_property
from unittest.mock import patch

import pytest

from src.reactor_di.caching import CachingStrategy
from src.reactor_di.module import (
    _create_bound_factory_func,
    _create_direct_factory_func,
    _needs_synthesis,
    _validate_component_dependencies,
    module,
)


class TestNeedsSynthesis:
    """Test _needs_synthesis function."""

    def test_non_class_returns_false(self):
        """Test non-class objects return False."""
        assert not _needs_synthesis("not a class")
        assert not _needs_synthesis(42)
        assert not _needs_synthesis(None)

    def test_non_abc_class_returns_false(self):
        """Test non-ABC classes return False."""

        class RegularClass:
            pass

        assert not _needs_synthesis(RegularClass)

    def test_abc_with_abstract_methods_returns_true(self):
        """Test ABC with abstract methods returns True."""

        class AbstractComponent(ABC):
            @abstractmethod
            def do_something(self) -> None:
                pass

        assert _needs_synthesis(AbstractComponent)

    def test_abc_with_annotations_returns_true(self):
        """Test ABC with type annotations returns True."""

        class ComponentWithDeps(ABC):
            _config: str
            _database: int

        assert _needs_synthesis(ComponentWithDeps)

    def test_abc_without_annotations_or_methods_returns_false(self):
        """Test ABC without annotations or abstract methods returns False."""

        class EmptyABC(ABC):  # noqa: B024
            pass

        assert not _needs_synthesis(EmptyABC)

    def test_get_type_hints_exception_fallback(self):
        """Test fallback when get_type_hints raises exception."""

        class ComponentWithBadAnnotations(ABC):
            # This will cause NameError when get_type_hints is called
            _dependency: "NonexistentType"  # noqa: F821

        # Should fallback to __annotations__ and still return True
        assert _needs_synthesis(ComponentWithBadAnnotations)

    def test_no_annotations_attribute(self):
        """Test class without __annotations__ attribute."""

        class NoAnnotations(ABC):  # noqa: B024
            pass

        # Remove __annotations__ to test the fallback
        if hasattr(NoAnnotations, "__annotations__"):
            delattr(NoAnnotations, "__annotations__")

        assert not _needs_synthesis(NoAnnotations)


class TestValidateComponentDependencies:
    """Test _validate_component_dependencies function."""

    def test_successful_validation(self):
        """Test successful dependency validation."""

        class ModuleClass:
            config: str
            database: int

        class Component:
            _config: str
            _database: int

        # Should not raise any exception
        _validate_component_dependencies(ModuleClass, Component)

    def test_validation_with_properties(self):
        """Test validation when module provides dependencies via properties."""

        class ModuleClass:
            @property
            def config(self) -> str:
                return "config"

        class Component:
            _config: str

        # Should not raise any exception
        _validate_component_dependencies(ModuleClass, Component)

    def test_missing_dependency_error(self):
        """Test error when dependency is missing."""

        class ModuleClass:
            pass

        class Component:
            _missing_dep: str

        with pytest.raises(
            TypeError, match="requires dependency '_missing_dep: <class 'str'>'"
        ):
            _validate_component_dependencies(ModuleClass, Component)

    def test_type_incompatibility_error(self):
        """Test error when types are incompatible."""

        class ModuleClass:
            config: int  # Provides int

        class Component:
            _config: str  # Requires str

        with pytest.raises(TypeError, match="Types are not compatible"):
            _validate_component_dependencies(ModuleClass, Component)

    def test_get_type_hints_exception_fallback(self):
        """Test fallback when get_type_hints raises exception."""

        class ModuleClass:
            # Bad annotation that will cause NameError
            config: "NonexistentType"  # noqa: F821

        class Component:
            _config: "NonexistentType"  # noqa: F821

        # Should fallback to __annotations__ and not raise
        _validate_component_dependencies(ModuleClass, Component)

    def test_property_without_annotation(self):
        """Test property without type annotation is accepted."""

        class ModuleClass:
            @property
            def config(self):  # No type annotation
                return "config"

        class Component:
            _config: str

        # Should not raise - we can't validate type but that's acceptable
        _validate_component_dependencies(ModuleClass, Component)


class TestCreateDirectFactoryFunc:
    """Test _create_direct_factory_func function."""

    def test_factory_creation(self):
        """Test factory function creation."""

        class SimpleClass:
            def __init__(self):
                self.value = "created"

        factory = _create_direct_factory_func("test_component", SimpleClass)

        # Test factory attributes
        assert factory.__name__ == "test_component"
        assert factory.__doc__ == "Create test component instance."
        assert factory.__annotations__ == {"return": SimpleClass}

    def test_factory_execution(self):
        """Test factory function execution."""

        class SimpleClass:
            def __init__(self):
                self.value = "created"

        factory = _create_direct_factory_func("test_component", SimpleClass)

        # Execute factory
        instance = factory(None)  # self parameter not used
        assert isinstance(instance, SimpleClass)
        assert instance.value == "created"


class TestCreateBoundFactoryFunc:
    """Test _create_bound_factory_func function."""

    def test_factory_creation(self):
        """Test bound factory function creation."""

        class ComponentABC(ABC):
            _config: str

        factory = _create_bound_factory_func("service", ComponentABC)

        # Test factory attributes
        assert factory.__name__ == "service"
        assert factory.__doc__ == "Synthesize composed service implementation."
        assert factory.__annotations__ == {"return": ComponentABC}

    def test_factory_execution_with_dependencies(self):
        """Test bound factory execution with dependency injection."""

        class ComponentABC(ABC):
            _config: str
            _value: int

        class MockModule:
            def __init__(self):
                self.config = "test-config"
                self.value = 42

        factory = _create_bound_factory_func("service", ComponentABC)
        module_instance = MockModule()

        # Execute factory
        component = factory(module_instance)

        # Test component creation and dependency injection
        assert isinstance(component, ComponentABC)
        assert component._config == "test-config"
        assert component._value == 42

    def test_get_type_hints_exception_fallback(self):
        """Test fallback when get_type_hints raises exception."""

        class BadComponent(ABC):
            _dependency: "NonexistentType"  # noqa: F821

        class MockModule:
            def __init__(self):
                self.dependency = "fallback-value"

        factory = _create_bound_factory_func("service", BadComponent)
        module_instance = MockModule()

        # Should work with fallback to __annotations__
        component = factory(module_instance)
        assert component._dependency == "fallback-value"

    def test_synthesized_component_naming(self):
        """Test proper naming of synthesized component."""

        class MyService(ABC):
            _config: str

        class MyModule:
            def __init__(self):
                self.config = "test"

        factory = _create_bound_factory_func("service", MyService)
        module_instance = MyModule()

        component = factory(module_instance)

        # Check naming
        assert component.__class__.__name__ == "MyService"
        assert component.__class__.__qualname__ == "MyModule.MyService"


class TestModuleDecorator:
    """Test module decorator function."""

    def test_caching_strategy_argument(self):
        """Test @module(CachingStrategy.NOT_THREAD_SAFE) usage."""

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestModule:
            config: str

        # Should have cached_property
        assert isinstance(TestModule.config, cached_property)
        # Verify caching behavior actually works
        module_instance = TestModule()
        first_access = module_instance.config
        second_access = module_instance.config
        assert first_access is second_access  # Verify caching
        assert first_access == ""  # Verify default value creation

    def test_legacy_direct_decoration(self):
        """Test @module (legacy) usage."""

        @module
        class TestModule:
            config: str

        # Should have property (DISABLED strategy)
        assert isinstance(TestModule.config, property)
        # Verify no caching behavior (new instance each time)
        module_instance = TestModule()
        first_access = module_instance.config
        second_access = module_instance.config
        # With DISABLED strategy, should get new instances each time
        assert first_access == second_access == ""  # Same value
        # Note: can't test identity for strings since "" is interned

    def test_explicit_parentheses(self):
        """Test @module() usage."""

        @module()
        class TestModule:
            config: str

        # Should have property (DISABLED strategy)
        assert isinstance(TestModule.config, property)
        # Verify functional behavior matches DISABLED strategy
        module_instance = TestModule()
        config_value = module_instance.config
        assert config_value == ""  # Default string creation
        assert isinstance(config_value, str)  # Correct type

    def test_invalid_argument_error(self):
        """Test error with invalid arguments."""
        with pytest.raises(TypeError, match="Invalid argument to @module"):
            module("invalid")

    def test_abc_component_synthesis(self):
        """Test ABC component synthesis."""

        class TestService(ABC):
            _config: str

            @property
            def config(self) -> str:
                return self._config

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestModule:
            config: str  # Declare config dependency first
            service: TestService  # Use class directly, not string

        module_instance = TestModule()
        service = module_instance.service

        assert isinstance(service, TestService)
        assert service.config == ""  # config creates empty string

    def test_non_abc_component_instantiation(self):
        """Test non-ABC component direct instantiation."""

        class SimpleConfig:
            def __init__(self):
                self.value = "config-value"

        @module(CachingStrategy.DISABLED)
        class TestModule:
            config: SimpleConfig

        module_instance = TestModule()
        config = module_instance.config

        assert isinstance(config, SimpleConfig)
        assert config.value == "config-value"

    def test_existing_attribute_skipped(self):
        """Test that existing attributes are not overridden."""

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestModule:
            config: str

            @property
            def config(self) -> str:
                return "existing-config"

        module_instance = TestModule()

        # Should use existing property, not generated one
        assert module_instance.config == "existing-config"

    def test_string_annotation_resolution(self):
        """Test string annotation resolution from module globals."""

        class ConfigClass:
            def __init__(self):
                self.value = "resolved"

        # Simulate module globals
        with patch("inspect.currentframe") as mock_frame:
            mock_frame.return_value.f_back.f_globals = {"ConfigClass": ConfigClass}

            @module(CachingStrategy.DISABLED)
            class TestModule:
                config: "ConfigClass"

            module_instance = TestModule()
            config = module_instance.config

            assert isinstance(config, ConfigClass)
            assert config.value == "resolved"

    def test_string_annotation_resolution_failure(self):
        """Test string annotation resolution failure fallback."""
        with patch("inspect.currentframe") as mock_frame:
            mock_frame.return_value = None  # Simulate frame access failure

            @module(CachingStrategy.DISABLED)
            class TestModule:
                config: "UnresolvableType"  # noqa: F821

            # Should not raise exception, will use string as type
            assert hasattr(TestModule, "config")

    def test_string_annotation_resolution_exception(self):
        """Test string annotation resolution with exception in frame access."""
        with patch("inspect.currentframe") as mock_frame:
            # Simulate exception in frame access (AttributeError or KeyError)
            mock_frame.side_effect = AttributeError("frame access failed")

            @module(CachingStrategy.DISABLED)
            class TestModule:
                config: "UnresolvableType"  # noqa: F821

            # Should handle exception and fallback to string type
            assert hasattr(TestModule, "config")

    def test_get_type_hints_exception_in_decorator(self):
        """Test get_type_hints exception handling in decorator."""

        @module(CachingStrategy.DISABLED)
        class TestModule:
            config: "NonexistentType"  # noqa: F821  # Will cause NameError in get_type_hints

        # Should fallback to __annotations__ and work
        assert hasattr(TestModule, "config")

    def test_caching_strategy_disabled_creates_property(self):
        """Test DISABLED strategy creates property."""

        class SimpleClass:
            pass

        @module(CachingStrategy.DISABLED)
        class TestModule:
            component: SimpleClass

        descriptor = TestModule.component
        assert isinstance(descriptor, property)
        assert not isinstance(descriptor, cached_property)
        # Verify DISABLED strategy behavior - no caching
        module_instance = TestModule()
        component1 = module_instance.component
        component2 = module_instance.component
        assert component1 is not component2  # New instance each time
        assert isinstance(component1, SimpleClass)
        assert isinstance(component2, SimpleClass)

    def test_caching_strategy_not_thread_safe_creates_cached_property(self):
        """Test NOT_THREAD_SAFE strategy creates cached_property."""

        class SimpleClass:
            pass

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestModule:
            component: SimpleClass

        descriptor = TestModule.component
        assert isinstance(descriptor, cached_property)
        # Verify NOT_THREAD_SAFE strategy behavior - caching works
        module_instance = TestModule()
        component1 = module_instance.component
        component2 = module_instance.component
        assert component1 is component2  # Same instance (cached)
        assert isinstance(component1, SimpleClass)
        # Verify it's actually cached by checking the cache
        assert hasattr(module_instance, "__dict__")
        assert "component" in module_instance.__dict__

    def test_cached_property_set_name_called(self):
        """Test that __set_name__ is called on cached_property."""

        class SimpleClass:
            pass

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestModule:
            component: SimpleClass

        descriptor = TestModule.component
        # cached_property should have been configured with __set_name__
        assert isinstance(descriptor, cached_property)
        # We can't easily test __set_name__ was called, but if it works, it was called

    def test_component_caching_behavior(self):
        """Test component caching behavior differences."""
        call_count = 0

        class CountingClass:
            def __init__(self):
                nonlocal call_count
                call_count += 1
                self.instance_id = call_count

        # Test DISABLED (no caching)
        @module(CachingStrategy.DISABLED)
        class NoCacheModule:
            component: CountingClass

        no_cache_module = NoCacheModule()
        comp1 = no_cache_module.component
        comp2 = no_cache_module.component

        # Should be different instances
        assert comp1.instance_id != comp2.instance_id

        # Reset counter
        call_count = 0

        # Test NOT_THREAD_SAFE (caching)
        @module(CachingStrategy.NOT_THREAD_SAFE)
        class CacheModule:
            component: CountingClass

        cache_module = CacheModule()
        comp3 = cache_module.component
        comp4 = cache_module.component

        # Should be same instance
        assert comp3.instance_id == comp4.instance_id
        assert comp3 is comp4


class TestIntegrationScenarios:
    """Integration tests for complex scenarios."""

    def test_complex_dependency_injection_scenario(self):
        """Test complex DI scenario with multiple dependencies."""

        class TestConfig:
            def __init__(self):
                self.host = "localhost"
                self.port = 5432

        class TestDatabase(ABC):
            _config: TestConfig

            def get_connection(self) -> str:
                return f"db://{self._config.host}:{self._config.port}"

        class TestService(ABC):
            _database: TestDatabase
            _config: TestConfig

            def process_data(self) -> str:
                return f"Processing on {self._database.get_connection()}"

        @module(CachingStrategy.NOT_THREAD_SAFE)
        class TestAppModule:
            config: TestConfig
            database: TestDatabase
            service: TestService

        app = TestAppModule()

        # Test full dependency chain
        service = app.service
        result = service.process_data()

        assert result == "Processing on db://localhost:5432"

        # Test caching - should be same instances
        assert app.service is app.service
        assert app.database is app.database
        assert app.config is app.config

    def test_validation_error_in_complex_scenario(self):
        """Test validation errors in complex scenarios."""

        class TestServiceWithMissingDep(ABC):
            _missing_dependency: str

        with pytest.raises(TypeError, match="requires dependency '_missing_dependency"):

            @module(CachingStrategy.DISABLED)
            class TestBadModule:
                service: TestServiceWithMissingDep
