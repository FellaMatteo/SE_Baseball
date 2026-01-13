import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "SE_Baseball"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def popola_dd_anno(self, annate):
        self.dd_anno.options.clear()

        for anno in annate:
            self.dd_anno.options.append(ft.dropdown.Option(str(anno)))

        self.update()


    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Squadre di Baseball", size=30, weight=ft.FontWeight.BOLD)

        # TODO

        # Riga 1
        self.dd_anno = ft.Dropdown(
            label="Anno",
            width=200,
            alignment=ft.alignment.top_left,
            on_change=self.controller.read_dd_anno if self.controller else None,
            options=[ft.dropdown.Option(str(y)) for y in self.controller.popola_dd_anno()]
        )

        row1 = ft.Row([ft.Container(self.txt_titolo, width=500),
                               ft.Container(None, width=0),
                               ft.Container(self.dd_anno, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)

        # Riga 2
        self.txt_out_squadre = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        cont = ft.Container(self.txt_out_squadre, width=300, height=200, alignment=ft.alignment.top_left,
                            bgcolor=ft.Colors.SURFACE)
        self.pulsante_crea_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self.controller.handle_crea_grafo)
        row2 = ft.Row([cont, self.pulsante_crea_grafo],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)

        # Riga 3
        self.dd_squadra = ft.Dropdown(label="Squadra", width=200)
        self.pulsante_dettagli = ft.ElevatedButton(text="Dettagli", on_click=self.controller.handle_dettagli)
        self.pulsante_percorso = ft.ElevatedButton(text="Percorso", on_click=self.controller.handle_percorso)
        row3 = ft.Row([ft.Container(self.dd_squadra, width=250),
                               ft.Container(self.pulsante_dettagli, width=250),
                               ft.Container(self.pulsante_percorso, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)

        for i in range(0,200):
            self.txt_out_squadre.controls.append(ft.Text(f"Squadra {i}"))

        self.txt_risultato = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            row1,
            ft.Divider(),

            row2,
            ft.Divider(),

            row3,
            self.txt_risultato
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
