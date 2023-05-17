import flet as ft
from views.AppPage import AppPage

# Register this page on root.py
#
# pages: list[AppPage] = [
#     LoginPage(root=page, route='/')
#     PageTemplate(root=page, route='/route') <----- route must not repeat
# ]
# Required


class PageTemplate (AppPage):

    # Required
    def __init__(self, root, route):
        super().__init__(root=root, route=route)

    # Required
    # Will be called after the page is loaded
    def get_page(self) -> ft.View:
        # Access to root page
        # self.root.go('/')

        # Add components to Page
        self.page.controls = [
            ft.Text('Hello World!')
        ]
        # Required
        return self.page

    # Optional
    # Will be called after get_page() is called
    def did_mount(self):
        pass
