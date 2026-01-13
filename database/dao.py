from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_annate():
        conn = DBConnect.get_connection()

        annate = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  DISTINCT year
                    FROM team
                    WHERE year >= 1980
                    ORDER BY year DESC"""

        cursor.execute(query)

        for row in cursor:
            annate.append(row["year"])

        cursor.close()
        conn.close()
        return annate

    @staticmethod
    def filtra_squadre_per_anno(anno):
        conn = DBConnect.get_connection()

        squadre = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  DISTINCT team_code, name
                    FROM team
                    WHERE year = %s
                """

        cursor.execute(query, (anno,))

        for row in cursor:
            squadre[row["team_code"]] = row["name"]

        cursor.close()
        conn.close()
        return squadre


    @staticmethod
    def get_salari_per_squadra(anno):
        conn = DBConnect.get_connection()

        salari = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.name, SUM(s.salary) AS salary
                        FROM team t, salary s
                        WHERE t.id = s.team_id AND t.year = %s
                        GROUP BY t.name
                    """

        cursor.execute(query, (anno,))

        for row in cursor:
            salari.append((row["name"], row["salary"]))

        cursor.close()
        conn.close()
        return salari