import flet as ft
from controllers.AuthController import login
from views.AppPage import AppPage
from pocketbase.utils import ClientResponseError


class LoginPage (AppPage):
    username = ft.Ref[ft.TextField]()
    password = ft.Ref[ft.TextField]()

    def __init__(self, root, route):
        super().__init__(root=root, route=route)
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.did_mount = self.did_mount

    def did_mount(self):
        self.username.current.value = 'user'
        self.password.current.value = '12345678'

    def get_page(self,) -> ft.View:
        self.page.controls = [
            ft.Image(src="icon.png", width=100, height=100),
            ft.TextField(
                ref=self.username,
                label="Username",
                width=500,
                prefix_icon=ft.icons.PERSON
            ),
            ft.TextField(
                ref=self.password,
                password=True,
                can_reveal_password=True,
                label="Password",
                width=500,
                prefix_icon=ft.icons.PASSWORD
            ),
            ft.Container(height=32),
            ft.FilledButton(
                text="LOGIN",
                on_click=self.on_login,
                width=500
            )
        ]

        return self.page

    def on_login(self, _):
        try:
            login(username=self.username.current.value,
                  password=self.password.current.value)
            self.root.go(route='/dashboard')
        except ClientResponseError:
            ok = ft.Ref[ft.TextButton]()
            dialog = ft.AlertDialog(
                modal=True, content=ft.Text('Username or password not found'),
                actions=[
                    ft.TextButton('OK', ref=ok)
                ]
            )

            def on_close(_):
                dialog.open = False
                self.root.update()
            ok.current.on_click = on_close

            self.root.dialog = dialog
            dialog.open = True
            self.root.update()
