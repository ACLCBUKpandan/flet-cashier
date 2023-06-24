# Do not modify this file.
import flet as ft

class AppPage():
    def __init__(self,
                 root: ft.Page,
                 route: str):
        self.root: ft.Page = root
        self.page: ft.View = ft.View(route)
        self.page.did_mount = self.did_mount

    def get_page(self) -> ft.View:
        return self.page

    def did_mount(self):
        pass
