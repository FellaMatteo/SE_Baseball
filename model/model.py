from itertools import combinations

from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.annate = []
        self.G = nx.Graph()
        self.squadre = []
        self.salari_per_squadra ={}

        # Ricorsione
        self.percorso_migliore = []
        self.best_score = 0


    def recupera_annate(self):
        return DAO.get_annate()

    def recupera_squadre(self, anno):
        diz_squadre = DAO.filtra_squadre_per_anno(anno)
        self.squadre = diz_squadre.values()

        return diz_squadre

    def recupera_salari(self, anno):
        self.salari_per_squadra = DAO.get_salari_per_squadra(anno)

    def crea_grafo(self, anno):
        self.G.clear()

        # AGGIUNGO I NODI
        nodi = self.squadre
        self.G.add_nodes_from(nodi)

        salari = DAO.get_salari_per_squadra(anno)

        # QUESTO E' IL PASSAGGIO PIU IMPORTANTE... MAPPO GLI ELEMENTI RECUPERATI NEL DAO IN MODO DA USARE LA LOGICA DEGLI OGGETTI
        mappa_salari = {}

        # Scorro la lista degli oggetti restituiti dal DAO
        for s in salari:
            nome_squadra, stipendio = s
            mappa_salari[nome_squadra] = stipendio

        # 4. Aggiungo gli archi
        for s1, s2 in combinations(nodi, 2):
            salario1 = mappa_salari[s1]
            salario2 = mappa_salari[s2]

            peso = salario1 + salario2

            self.G.add_edge(s1, s2, weight=peso)



    def cerca_adiacenti(self, nodo_di_partenza):
        vicini = list(self.G.neighbors(nodo_di_partenza))

        vicini_con_peso = []
        for vicino in vicini:
            peso = self.G[nodo_di_partenza][vicino]['weight']

            vicini_con_peso.append((vicino, peso))

        return vicini_con_peso

    def compute_best_set(self, nodo_partenza):
        self.percorso_migliore = []
        self.best_score = 0

        parziale = [nodo_partenza]

        self.ricorsione(parziale)

        return self.percorso_migliore, self.best_score


    def ricorsione(self, parziale):
        # Calcoliamo il peso totale del percorso che abbiamo in mano adesso
        peso_attuale = 0
        for i in range(len(parziale) - 1):
            u = parziale[i]
            v = parziale[i + 1]
            # Recuperiamo il peso dal grafo
            peso_attuale += self.G[u][v]['weight']

        # HO FATTO MEGLIO DI PRIMA?
        if peso_attuale > self.best_score:
            self.best_score = peso_attuale
            self.percorso_migliore = list(parziale)

        # --- FASE 2: IDENTIFICAZIONE DEI CANDIDATI ---
        ultimo_nodo = parziale[-1]

        # Dobbiamo trovare il peso dell'arco che ci ha portato qui per verificare la decrescenza.
        # Se siamo al primo nodo (len=1), non c'è un "prima", quindi accettiamo qualsiasi peso.
        # Usiamo float('inf') (infinito) perché qualsiasi numero è minore di infinito.
        peso_ultimo_arco = float('inf')

        if len(parziale) > 1:
            penultimo_nodo = parziale[-2]
            peso_ultimo_arco = self.G[penultimo_nodo][ultimo_nodo]['weight']

        vicini_ammissibili = []

        # Scorriamo tutti i vicini fisici del nodo
        for vicino in self.G.neighbors(ultimo_nodo):
            # Recuperiamo il peso dell'arco verso il vicino
            peso_arco = self.G[ultimo_nodo][vicino]['weight']

            if (vicino not in parziale) and (peso_arco < peso_ultimo_arco):
                # Salviamo una tupla (NomeNodo, Peso) per poter ordinare dopo
                vicini_ammissibili.append((vicino, peso_arco))

        # --- FASE 3: POTATURA (PRUNING) CON K ---
        # Ordiniamo i vicini per peso decrescente (dal più grande al più piccolo)
        vicini_ammissibili.sort(key=lambda x: x[1], reverse=True)

        K = 3  # Parametro richiesto dal testo
        # Tagliamo la lista: teniamo solo i primi K elementi
        candidati_scelti = vicini_ammissibili[:K]

        # --- FASE 4: PASSO AVANTI E BACKTRACKING ---

        for nodo_candidato, peso_candidato in candidati_scelti:
            # 1. Aggiungo il nodo
            parziale.append(nodo_candidato)

            # 2. Ricorsione (scendo in profondità)
            self.ricorsione(parziale)

            # 3. Backtracking (rimuovo l'ultimo nodo per provare le altre strade)
            parziale.pop()
