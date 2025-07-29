"""Tests for async uptodate function support in template caching."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from jinja2 import Template

from jinja2_async_environment import AsyncEnvironment


class TestAsyncUptodateSupport:
    """Test cases for async uptodate function support."""

    @pytest.mark.asyncio
    async def test_is_template_up_to_date_with_sync_uptodate(self) -> None:
        """Test _is_template_up_to_date with synchronous uptodate function."""
        env = AsyncEnvironment()
        
        # Create a mock template with a sync uptodate function
        template = MagicMock(spec=Template)
        template.is_up_to_date = lambda: True
        
        result = await env._is_template_up_to_date(template)
        assert result is True
        
        # Test with uptodate returning False
        template.is_up_to_date = lambda: False
        result = await env._is_template_up_to_date(template)
        assert result is False

    @pytest.mark.asyncio
    async def test_is_template_up_to_date_with_async_uptodate(self) -> None:
        """Test _is_template_up_to_date with asynchronous uptodate function."""
        env = AsyncEnvironment()
        
        # Create a mock template with an async uptodate function
        template = MagicMock(spec=Template)
        
        async def async_uptodate_true() -> bool:
            return True
            
        async def async_uptodate_false() -> bool:
            return False
        
        template.is_up_to_date = async_uptodate_true
        result = await env._is_template_up_to_date(template)
        assert result is True
        
        # Test with async uptodate returning False
        template.is_up_to_date = async_uptodate_false
        result = await env._is_template_up_to_date(template)
        assert result is False

    @pytest.mark.asyncio
    async def test_is_template_up_to_date_coroutine_detection(self) -> None:
        """Test that coroutine functions are properly detected and awaited."""
        import inspect
        env = AsyncEnvironment()
        
        # Test with async function
        template = MagicMock(spec=Template)
        
        async def async_uptodate() -> bool:
            return True
        
        template.is_up_to_date = async_uptodate
        # Verify it's detected as a coroutine function
        assert inspect.iscoroutinefunction(template.is_up_to_date)
        result = await env._is_template_up_to_date(template)
        assert result is True
        
        # Test with sync function
        def sync_uptodate() -> bool:
            return False
        
        template.is_up_to_date = sync_uptodate
        # Verify it's NOT detected as a coroutine function
        assert not inspect.iscoroutinefunction(template.is_up_to_date)
        result = await env._is_template_up_to_date(template)
        assert result is False

    @pytest.mark.asyncio
    async def test_is_template_up_to_date_with_non_callable(self) -> None:
        """Test _is_template_up_to_date with non-callable uptodate attribute."""
        env = AsyncEnvironment()
        
        # Create a mock template with a non-callable uptodate attribute
        template = MagicMock(spec=Template)
        template.is_up_to_date = True
        
        result = await env._is_template_up_to_date(template)
        assert result is True
        
        # Test with False value
        template.is_up_to_date = False
        result = await env._is_template_up_to_date(template)
        assert result is False

    @pytest.mark.asyncio
    async def test_is_template_up_to_date_with_mock_magic(self) -> None:
        """Test _is_template_up_to_date with MagicMock template."""
        env = AsyncEnvironment()
        
        # Create a MagicMock template (simulates test scenarios)
        template = MagicMock()
        template.is_up_to_date = lambda: True
        
        result = await env._is_template_up_to_date(template)
        assert result is True

    @pytest.mark.asyncio
    async def test_get_from_cache_with_async_uptodate(self) -> None:
        """Test that _get_from_cache properly handles async uptodate functions."""
        env = AsyncEnvironment()
        env.auto_reload = True
        env.cache = {"test_key": MagicMock(spec=Template)}
        
        # Create a template with an async uptodate function
        template = env.cache["test_key"]
        
        async def async_uptodate() -> bool:
            return True
            
        template.is_up_to_date = async_uptodate
        template.globals = MagicMock()
        template.globals.update = MagicMock()
        
        # Test that _get_from_cache can handle async uptodate
        result = await env._get_from_cache("test_key", {"test": "globals"})
        assert result is template
        template.globals.update.assert_called_once_with({"test": "globals"})

    @pytest.mark.asyncio
    async def test_get_from_cache_with_sync_uptodate(self) -> None:
        """Test that _get_from_cache properly handles sync uptodate functions."""
        env = AsyncEnvironment()
        env.auto_reload = True
        env.cache = {"test_key": MagicMock(spec=Template)}
        
        # Create a template with a sync uptodate function
        template = env.cache["test_key"]
        template.is_up_to_date = lambda: True
        template.globals = MagicMock()
        template.globals.update = MagicMock()
        
        # Test that _get_from_cache can handle sync uptodate
        result = await env._get_from_cache("test_key", {"test": "globals"})
        assert result is template
        template.globals.update.assert_called_once_with({"test": "globals"})

    @pytest.mark.asyncio
    async def test_get_from_cache_with_stale_async_uptodate(self) -> None:
        """Test that _get_from_cache returns None when async uptodate returns False."""
        env = AsyncEnvironment()
        env.auto_reload = True
        env.cache = {"test_key": MagicMock(spec=Template)}
        
        # Create a template with an async uptodate function that returns False
        template = env.cache["test_key"]
        
        async def async_uptodate_stale() -> bool:
            return False
            
        template.is_up_to_date = async_uptodate_stale
        
        # Test that _get_from_cache returns None for stale templates
        result = await env._get_from_cache("test_key", {"test": "globals"})
        assert result is None