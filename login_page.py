import flet as ft
import sqlite3


async def view(db: sqlite3.Connection, page_: ft.Page):
    cursor = db.cursor()

    async def login(_):
        res = cursor.execute(
            f"SELECT user_id FROM users WHERE login='{login_field.value}' AND password='{password_field.value}'").fetchall()
        if res:
            page_.session.set("id", res[0][0])
            page_.session.set("login", True)
            await page_.go_async("/")
        else:
            dlg = ft.AlertDialog(title=ft.Text("Неверное имя пользователя или пароль!"))
            page_.dialog = dlg
            dlg.open = True
            await page_.update_async()

    login_field = ft.TextField(label="Логин")
    password_field = ft.TextField(label="Пароль", password=True, can_reveal_password=True)

    return ft.View(
        "/login", [
            ft.Card(ft.Column(controls=[
                ft.Text("Вход", size=20),
                login_field,
                password_field,
                ft.TextButton(text="Войти", on_click=login),
            ], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400),
                margin=30)], vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
