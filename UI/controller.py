import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        anno = int(self._view.dd_anno.value)

        self._model.crea_grafo(anno)

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        nodo_di_partenza = str(self._view.dd_squadra.value)

        squadre_adiacenti_peso = self._model.cerca_adiacenti(nodo_di_partenza)

        self._view.txt_risultato.controls.clear()
        for squadra in squadre_adiacenti_peso:
            self._view.txt_risultato.controls.append(ft.Text(f"{squadra[0]}, - peso: {squadra[1]}"))

        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        nodo_partenza = str(self._view.dd_squadra.value)

        percorso, peso_max = self._model.compute_best_set(nodo_partenza)

        self._view.txt_risultato.controls.clear()

        self._view.txt_risultato.controls.append(
            ft.Text(f"Percorso Ottimo Trovato! Peso Totale: {peso_max}")
        )

        # 4. STAMPO I DETTAGLI DEGLI ARCHI
        # Scorro la lista dei nodi a coppie (A -> B, B -> C...) per leggere i pesi intermedi
        for i in range(len(percorso) - 1):
            nodo_da = percorso[i]
            nodo_a = percorso[i + 1]

            # Recupero il peso del singolo arco dal grafo (attraverso il model)
            peso_arco = self._model.G[nodo_da][nodo_a]['weight']

            self._view.txt_risultato.controls.append(ft.Text(f"{nodo_da} --> {nodo_a} (peso: {peso_arco})"))

        self._view.update()


    """ Altri possibili metodi per gestire di dd_anno """""
    def popola_dd_anno(self):
        return self._model.recupera_annate()

    def read_dd_anno(self, e):
        anno = int(self._view.dd_anno.value)
        squadre = self._model.recupera_squadre(anno)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(squadre)}"))

        for squadra in squadre:
            for s in squadre.values():
                self._view.txt_out_squadre.controls.append(ft.Text(f"{squadra}, {s}"))

        # ORA POPOLO ANCHE IL DROPDOWN DELLE SQUADRE
        self._view.dd_squadra.options = [ft.dropdown.Option(nome) for nome in squadre.values()]

        self._view.update()

