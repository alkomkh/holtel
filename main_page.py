import flet as ft
import sqlite3


async def view(db: sqlite3.Connection, page_:ft.Page):
    cursor = db.cursor()
    return ft.View("/main", [

    ])