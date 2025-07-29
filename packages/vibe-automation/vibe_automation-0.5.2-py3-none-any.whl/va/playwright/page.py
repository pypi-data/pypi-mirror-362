import logging
import asyncio
import atexit
import re
from typing import Any, Dict, Optional, Callable

from playwright.sync_api import Locator
from playwright._impl._page import Page as PageImpl
from playwright._impl._locator import Locator as LocatorImpl
from playwright._impl._element_handle import ElementHandle as ElementHandleImpl
from playwright.async_api._generated import (
    Page as PageAPI,
    Locator as LocatorAPI,
    ElementHandle as ElementHandleAPI,
)
from stagehand import StagehandPage
from .locator import PromptBasedLocator
from .step import print_pending_modifications, AsyncStepContextManager, execute_step
from ..agent.agent import Agent
from ..review import review, ReviewStatus
from ..constants import REVIEW_TIMEOUT


log = logging.getLogger("va.playwright")


def normalize_locator_string(js_locator: str) -> str:
    """
    Normalize a JavaScript-style locator string to Python format.

    Examples:
    - getByRole('textbox', { name: 'Customer name:' }) -> get_by_role('textbox', name="Customer name:")
    - getByText('Submit') -> get_by_text('Submit')
    - getByLabel('Email') -> get_by_label('Email')
    """
    if not js_locator:
        return js_locator

    # Convert camelCase method names to snake_case
    # Handle compound words like TestId first
    js_locator = re.sub(
        r"getBy([A-Z][a-z]+)([A-Z][a-z]+)",
        lambda m: f"get_by_{m.group(1).lower()}_{m.group(2).lower()}",
        js_locator,
    )
    # Handle simple cases
    js_locator = re.sub(
        r"getBy([A-Z][a-z]*)", lambda m: f"get_by_{m.group(1).lower()}", js_locator
    )

    # Convert JavaScript object syntax to Python keyword arguments
    def convert_js_object(match):
        obj_content = match.group(1).strip()

        # Split by commas, but be careful about commas inside strings
        parts = []
        current_part = ""
        in_string = False
        quote_char = None

        for char in obj_content:
            if char in ('"', "'") and not in_string:
                in_string = True
                quote_char = char
                current_part += char
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
                current_part += char
            elif char == "," and not in_string:
                parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char

        if current_part.strip():
            parts.append(current_part.strip())

        # Process each part into keyword arguments
        processed_parts = []
        for part in parts:
            part = part.strip()
            # Handle key: value pairs
            if ":" in part:
                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes from key if present
                if key.startswith('"') and key.endswith('"'):
                    key = key[1:-1]
                elif key.startswith("'") and key.endswith("'"):
                    key = key[1:-1]

                # Convert single quotes to double quotes for string values
                if value.startswith("'") and value.endswith("'"):
                    value = f'"{value[1:-1]}"'
                elif value == "true":
                    value = "True"
                elif value == "false":
                    value = "False"

                processed_parts.append(f"{key}={value}")
            else:
                processed_parts.append(part)

        return ", ".join(processed_parts)

    # Match JavaScript object literals like { name: 'value', other: 'test' }
    js_locator = re.sub(r"\{\s*([^}]+)\s*\}", convert_js_object, js_locator)

    return js_locator


# Monkey patch the Playwright Page implementation to add snapshotForAI method
async def _snapshot_for_ai(self, metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Take a snapshot of the page optimized for AI consumption.

    This method monkey-patches the missing snapshotForAI method from the server API
    into the Python Playwright Page class.

    Parameters:
    -----------
    metadata (Dict[str, Any], optional): Metadata for the snapshot operation

    Returns:
    --------
    str: A text-based accessibility snapshot of the page optimized for AI analysis
    """
    if metadata is None:
        metadata = {}

    # Call the server-side snapshotForAI method via the internal channel
    return await self._channel.send("snapshotForAI", None, {"metadata": metadata})


# Apply the monkey patch to both implementation and API classes
PageImpl.snapshot_for_ai = _snapshot_for_ai


# Also add it to the API wrapper class
async def _api_snapshot_for_ai(self, metadata: Optional[Dict[str, Any]] = None) -> str:
    """API wrapper for snapshot_for_ai method."""
    return await self._impl_obj.snapshot_for_ai(metadata)


PageAPI.snapshot_for_ai = _api_snapshot_for_ai


# Monkey patch the Playwright ElementHandle implementation to add generateLocatorString method
async def _element_generate_locator_string(self) -> Optional[str]:
    """
    Generate a locator string for the element handle.

    This method monkey-patches the missing generateLocatorString method from the server API
    into the Python Playwright ElementHandle class.

    Returns:
    --------
    Optional[str]: A locator string that can be used to locate the element, or None if not found
    """
    result = await self._channel.send("generateLocatorString", None)
    locator_string = result.get("value") if isinstance(result, dict) else result
    return (
        normalize_locator_string(locator_string) if locator_string else locator_string
    )


# Apply the monkey patch to ElementHandle classes
ElementHandleImpl._generate_locator_string = _element_generate_locator_string


# Also add it to the API wrapper class
async def _api_element_generate_locator_string(self) -> Optional[str]:
    """API wrapper for _generate_locator_string method."""
    return await self._impl_obj._generate_locator_string()


ElementHandleAPI._generate_locator_string = _api_element_generate_locator_string


# Monkey patch the Playwright Locator implementation to add generateLocatorString method
async def _generate_locator_string(self) -> Optional[str]:
    """
    Generate a locator string for the element.

    This method monkey-patches the missing generateLocatorString method from the server API
    into the Python Playwright Locator class.

    Returns:
    --------
    Optional[str]: A locator string that can be used to locate the element, or None if not found
    """

    async def task(handle, timeout):
        return await handle._generate_locator_string()

    return await self._with_element(task)


# Apply the monkey patch to both implementation and API classes
LocatorImpl.generate_locator_string = _generate_locator_string


# Also add it to the API wrapper class
async def _api_generate_locator_string(self) -> Optional[str]:
    """API wrapper for generate_locator_string method."""
    return await self._impl_obj.generate_locator_string()


LocatorAPI.generate_locator_string = _api_generate_locator_string


# Register the cleanup function to run at exit
atexit.register(print_pending_modifications)


class Page:
    def __init__(self, page: StagehandPage):
        self._stagehand_page = page
        self._login_handler = None
        self._agent = Agent()
        # Track any background login tasks (only for fallback case)
        self._current_login_task = None

    def get_by_prompt(
        self,
        prompt: str,
    ) -> PromptBasedLocator:
        """
        Returns a PromptBasedLocator that can be used with or without fallback locators

        Parameters:
        -----------
        prompt (str): The natural language description of the element to locate.
        timeout (int) (optional): Timeout value in seconds for the connection with backend API service.
        wait_for_network_idle (bool) (optional): Whether to wait for network reaching full idle state before querying the page. If set to `False`, this method will only check for whether page has emitted [`load` event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event).
        include_hidden (bool) (optional): Whether to include hidden elements on the page. Defaults to `True`.
        mode (ResponseMode) (optional): The response mode. Can be either `standard` or `fast`. Defaults to `fast`.
        experimental_query_elements_enabled (bool) (optional): Whether to use the experimental implementation of the query elements feature. Defaults to `False`.

        Returns:
        --------
        PromptBasedLocator: A locator that uses prompt-based element finding
        """
        return PromptBasedLocator(self, prompt)

    async def get_locator_by_prompt(
        self,
        prompt: str,
    ) -> Locator | None:
        """
        Internal method to get element by prompt - used by PromptBasedLocator

        Returns:
        --------
        Playwright [Locator](https://playwright.dev/python/docs/api/class-locator) | None: The found element or `None` if no matching elements were found.
        """

        results = await self._stagehand_page.observe(prompt)

        if not results:
            return None

        selector = results[0].selector
        return self._stagehand_page.locator(selector)

    async def _check_login_and_handle(self, login_handler):
        """Check if login is required and handle it"""
        try:
            # Use extract() to get a text response
            result = await self._stagehand_page.extract(
                "Is login required on this page? Answer with exactly 'yes' or 'no' (lowercase, no additional text)."
            )
            answer = result.extraction.lower()
            if answer == "yes":
                log.info("Login required detected, calling handler")
                if login_handler:
                    log.info("Calling login handler")
                    # handle sync and async login handlers
                    if asyncio.iscoroutinefunction(login_handler):
                        await login_handler()
                    else:
                        login_handler()
                    log.info("Login handler completed")
                else:
                    log.warning("Login required but no handler available")
            else:
                log.info("No login required")

        except Exception as e:
            log.error(f"Error in login check: {e}")
            raise Exception(f"Login check failed: {e}") from e

    def step(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 16,
    ) -> AsyncStepContextManager:
        """
        Execute a natural language command by generating and running Python code.

        This method returns a context manager that can be used with 'async with'.
        The LLM action generation is only triggered if the with block is empty (contains only pass).

        Parameters:
        -----------
        command (str): Natural language description of the action to perform
        context (Dict[str, Any], optional): Context variables available to the generated script
        max_retries (int): Maximum number of retry attempts. Defaults to 3.

        Returns:
        --------
        AsyncStepContextManager: Context manager for the step execution
        """
        if context is None:
            context = {}
        return AsyncStepContextManager(self, command, context, max_retries, self._agent)

    def _check_login_and_handle_on_page_load(self, *args, **kwargs):
        """Run the login handler if registered as a background task to block pending actions"""
        if self._login_handler:
            log.info("Page load detected, running login handler")
            self._current_login_task = asyncio.create_task(
                self._check_login_and_handle(self._login_handler)
            )
            self._current_login_task.add_done_callback(
                lambda t: setattr(self, "_current_login_task", None)
            )
        else:
            log.info("Page load detected but no login handler registered")

    async def _execute_step(
        self,
        command: str,
        context: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """
        Internal method to execute a natural language command.
        Now delegates to the pure function in step.py.
        """
        return await execute_step(
            command=command,
            context=context,
            max_retries=max_retries,
            page=self._stagehand_page,
            agent=self._agent,
        )

    async def _wait_for_login_task(self):
        """Wait for any background login task to complete"""
        if self._current_login_task:
            await self._current_login_task
            log.info("Background login task completed")

    def __getattr__(self, name):
        """Forward attribute lookups to the underlying Stagehand page."""
        attr = getattr(self._stagehand_page, name)

        # Only wrap callable attributes
        if not callable(attr):
            return attr

        # TODO: this is a hack to wait for login task to complete before executing the method, this will cause a deadlock if the method has any other page methods. Since HITL won't call any page methods, this is fine for now. We will need to find a better way to handle this.
        if asyncio.iscoroutinefunction(attr):
            # create async wrapper that waits for login task
            async def async_wrapper(*args, **kwargs):
                await self._wait_for_login_task()
                return await attr(*args, **kwargs)

            return async_wrapper
        else:
            # create sync wrapper that waits for login task
            def sync_wrapper(*args, **kwargs):
                if self._current_login_task:
                    try:
                        asyncio.get_running_loop()
                        # In async context, proceed without waiting
                        log.warning(
                            "Sync method called while in async context with pending login task - proceeding without waiting"
                        )
                    except RuntimeError:
                        # No event loop running, we can create one
                        asyncio.run(self._wait_for_login_task())
                return attr(*args, **kwargs)

            return sync_wrapper

    def on(self, event: str, handler: Optional[Callable[[str], None]] = None):
        """
        Register event handler for page.

        For "login_required" event, if no handler is provided, uses the default login handler
        that starts a HITL review. For other events, a handler is required.

        Parameters:
        -----------
        event (str): The event to listen for
        handler (Optional[Callable[[str], None]], optional): The handler function to call when the event occurs.
                   If not provided for "login_required" event, uses the default login handler.

        Examples:
        ---------
        # Use default login handler (HITL review)
        page.on("login_required")

        # Use custom login handler
        page.on("login_required", custom_login_handler)

        # Other events require a handler
        page.on("page_event", page_event_handler)
        """
        if event == "login_required":
            # Use default handler if none provided
            if handler is None:
                handler = self.default_login_handler

            # Only add page load listener if we don't have a handler yet
            if self._login_handler is None:
                self._stagehand_page.on(
                    "load", self._check_login_and_handle_on_page_load
                )
            # if handler is not the same as the existing handler, replace it
            if self._login_handler and handler != self._login_handler:
                log.info("Replacing existing login handler")
            self._login_handler = handler
        else:
            # For other events, handler is required
            if handler is None:
                raise ValueError(f"Handler is required for event '{event}'")
            self._stagehand_page.on(event, handler)

    def remove_listener(
        self, event: str, handler: Optional[Callable[[str], None]] = None
    ):
        """
        Remove event handler for page. If the event is "login_required", we will remove the listener that checks if login is required on page loads.

        Parameters:
        -----------
        event (str): The event to remove listener for
        handler (Callable[[str], None] | None): The handler function to remove.
        """
        if event == "login_required":
            self._stagehand_page.remove_listener(
                "load", self._check_login_and_handle_on_page_load
            )
            self._login_handler = None
            log.info("Login handler removed")
        else:
            self._stagehand_page.remove_listener(event, handler)

    def default_login_handler(self):
        """Default login handler that starts HITL review"""
        r = review("review-for-login", "Please log in to continue.")
        r.wait(REVIEW_TIMEOUT)  # 1000s timeout
        if r.status != ReviewStatus.READY:
            raise Exception("Login review not completed")
