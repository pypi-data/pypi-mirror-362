"""Enterprise app class."""

from reflex.app import App
from reflex.config import get_config
from reflex.utils import console, prerequisites
from reflex.utils.exec import is_prod_mode
from reflex_cli.utils.hosting import save_token_to_config

from reflex_enterprise import constants
from reflex_enterprise.config import ConfigEnterprise
from reflex_enterprise.environment import environment
from reflex_enterprise.utils import (
    check_config_option_in_tier,
    is_deploy_context,
    is_new_session,
)


class AppEnterprise(App):
    """Enterprise app class."""

    def __post_init__(self):
        """Post-initialization."""
        super().__post_init__()
        self._check_and_setup_access_token()
        self._check_login()
        self._verify_and_setup_badge()
        self._verify_and_setup_proxy()

    def _check_and_setup_access_token(self):
        if environment.REFLEX_ACCESS_TOKEN.is_set():
            access_token = environment.REFLEX_ACCESS_TOKEN.get()
            if access_token is not None:
                save_token_to_config(access_token)

    def _check_login(self):
        """Check if the user is logged in.

        Raises:
            RuntimeError: If the user is not logged in.
        """
        current_tier = prerequisites.get_user_tier()

        if (
            current_tier == "anonymous"
            and not environment.REFLEX_BACKEND_ONLY.get()
            and not environment.CI.get()
        ):
            msg = (
                "`reflex-enterprise` is free to use but you must be logged in. "
                "Run `reflex login` or set the environment variable REFLEX_ACCESS_TOKEN with your token."
            )
            raise RuntimeError(msg)

        # Identify user to Koala Analytics after successful login
        self._identify_user_to_koala()

    def _verify_and_setup_badge(self):
        config = get_config()
        deploy = is_deploy_context()

        check_config_option_in_tier(
            option_name="show_built_with_reflex",
            allowed_tiers=(
                ["pro", "team", "enterprise"] if deploy else ["team", "enterprise"]
            ),
            fallback_value=True,
            help_link=constants.SHOW_BUILT_WITH_REFLEX_INFO,
        )

        if is_prod_mode() and config.show_built_with_reflex:
            self._setup_sticky_badge()

    def _verify_and_setup_proxy(self):
        config = get_config()
        deploy = is_deploy_context()

        if (
            isinstance(config, ConfigEnterprise)
            and config.use_single_port
            and not environment.REFLEX_BACKEND_ONLY.get()
        ):
            if deploy:
                console.warn(
                    "Single port mode is not supported when deploying to Reflex Cloud. Ignoring the setting."
                )
                return
            if is_new_session():
                console.info("Single port proxy mode enabled")
            # Enable proxying to frontend server.
            from .proxy import proxy_middleware

            self.register_lifespan_task(proxy_middleware)

    def _identify_user_to_koala(self):
        """Identify user to Koala Analytics if telemetry is enabled."""
        try:
            from reflex_cli.utils.hosting import authenticated_token

            from .koala import identify_koala_user

            # Get user information from authenticated token
            _, user_info = authenticated_token()
            if user_info and "email" in user_info:
                identify_koala_user(user_info["email"])
        except Exception:
            # Silently fail if we can't get user info or send to Koala
            pass


App = AppEnterprise
