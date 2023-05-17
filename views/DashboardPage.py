import flet as ft
from views.AppPage import AppPage
from views.components.NavRail import NavRail


class DashboardPage (AppPage):

    def __init__(self, root, route):
        super().__init__(root=root, route=route)

    def get_page(self) -> ft.View:
        self.page.controls = [
            ft.FilledButton(
                text="CREATE",
                icon=ft.icons.CREATE,
                on_click=lambda _: self.root.go('/create'),
            ),
            ft.FilledButton(
                text="HISTORY",
                icon=ft.icons.BOOK,
                on_click=lambda _: self.root.go('/history'),
            ),
        ]
        return self.page

    def did_mount(self):
        pass
