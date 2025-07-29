from typing import ClassVar

from routelit import AssetTarget, RouteLitBuilder  # type: ignore[import-untyped]


class RLBuilder(RouteLitBuilder):  # type: ignore[no-any-unimported]
    """
    A builder for a RouteLit application with a sidebar.
    The related frontend uses silicon.css for styling.
    This Builder serves as example on how to create a RouteLit application with a sidebar.
    You could use this same idea to create other areas, such as a header, footer, etc.
    """

    static_assets_targets: ClassVar[list[AssetTarget]] = [  # type: ignore[no-any-unimported]
        {
            "package_name": "routelit_silicon",
            "path": "static",
        }
    ]

    def _init_sidebar(self) -> "RLBuilder":
        new_element = self._create_element(
            name="sidebar",
            key="sidebar",
        )
        return self._build_nested_builder(new_element)  # type: ignore[no-any-return]

    def _init_root(self) -> "RLBuilder":
        new_element = self._create_element(
            name="root",
            key="root",
        )
        return self._build_nested_builder(new_element)  # type: ignore[no-any-return]

    def _on_init(self) -> None:
        # we could configure the sidebar to be set by default by calling `self._config_sidebar()` here
        # self._config_sidebar()
        pass

    def _config_sidebar(self) -> None:
        self._root = self._init_root()
        with self._root:
            self._sidebar = self._init_sidebar()
            self._main = self._init_main()
        self._parent_element = self._main._parent_element  # type: ignore[has-type]
        self.active_child_builder = self._main

    def set_config(self, use_sidebar: bool = True) -> None:
        """
        Set the configuration for the builder.
        It should be called before any other method is called.
        This method should be called only once, and cannot be undone.
        If you need to undo the configuration, rerun the view with `use_sidebar=False`

        Args:
            use_sidebar (bool): Whether to use a sidebar.
        """
        if use_sidebar:
            self._config_sidebar()

    @property
    def sidebar(self) -> "RLBuilder":
        """
        Get the sidebar element.

        Returns:
            RouteLitComponentsBuilder: The sidebar element.

        Example:
        ```python
        def view(ui: RouteLitComponentsBuilder):
            ui.set_config(use_sidebar=True)
            with ui.sidebar:
                ui.text("Hello, world!")

            # or without context
            ui.sidebar.text("Hello, world!")
        ```
        """
        return self._sidebar

    def _init_main(self) -> "RLBuilder":
        new_element = self._create_element(
            name="main",
            key="main",
        )
        return self._build_nested_builder(new_element)  # type: ignore[no-any-return]
