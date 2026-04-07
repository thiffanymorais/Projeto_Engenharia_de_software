import sqlite3
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_name="biblioteca.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS USUARIO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo_usuario TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ALUNO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                FOREIGN KEY(usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PROFESSOR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                FOREIGN KEY(usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SUPER_ADMIN (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                FOREIGN KEY(usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS EMPRESTIMO (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                livro TEXT NOT NULL,
                data_emprestimo TEXT NOT NULL,
                data_prevista_devolucao TEXT,
                dias_extensao INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'ABERTO',
                FOREIGN KEY(usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS RESERVA (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                livro TEXT NOT NULL,
                data_reserva TEXT NOT NULL,
                data_cancelamento TEXT,
                status TEXT NOT NULL DEFAULT 'ATIVA',
                FOREIGN KEY(usuario_id) REFERENCES USUARIO(id) ON DELETE CASCADE
            )
        ''')
        self._garantir_colunas_emprestimo()
        self._garantir_colunas_reserva()
        self.conn.commit()

        self._seed_super_admin()

    def _seed_super_admin(self):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = 'Admin'")
        if not self.cursor.fetchone():
            self.cursor.execute(
                "INSERT INTO USUARIO (username, senha, tipo_usuario) VALUES (?, ?, ?)",
                ("Admin", "admin123", "SuperAdmin")
            )
            admin_id = self.cursor.lastrowid
            self.cursor.execute(
                "INSERT INTO SUPER_ADMIN (usuario_id) VALUES (?)",
                (admin_id,)
            )
            self.conn.commit()

    def _garantir_colunas_emprestimo(self):
        self.cursor.execute("PRAGMA table_info(EMPRESTIMO)")
        colunas = [linha[1] for linha in self.cursor.fetchall()]

        if "data_prevista_devolucao" not in colunas:
            self.cursor.execute(
                "ALTER TABLE EMPRESTIMO ADD COLUMN data_prevista_devolucao TEXT"
            )
        if "dias_extensao" not in colunas:
            self.cursor.execute(
                "ALTER TABLE EMPRESTIMO ADD COLUMN dias_extensao INTEGER NOT NULL DEFAULT 0"
            )

    def _garantir_colunas_reserva(self):
        self.cursor.execute("PRAGMA table_info(RESERVA)")
        colunas = [linha[1] for linha in self.cursor.fetchall()]
        if "data_cancelamento" not in colunas:
            self.cursor.execute(
                "ALTER TABLE RESERVA ADD COLUMN data_cancelamento TEXT"
            )

    def cadastrar_usuario(self, username: str, senha: str, tipo_usuario: str):
        try:
            self.cursor.execute(
                "INSERT INTO USUARIO (username, senha, tipo_usuario) VALUES (?, ?, ?)",
                (username, senha, tipo_usuario)
            )
            usuario_id = self.cursor.lastrowid

            if tipo_usuario == "Aluno":
                self.cursor.execute(
                    "INSERT INTO ALUNO (usuario_id) VALUES (?)",
                    (usuario_id,)
                )
            elif tipo_usuario == "Professor":
                self.cursor.execute(
                    "INSERT INTO PROFESSOR (usuario_id) VALUES (?)",
                    (usuario_id,)
                )

            self.conn.commit()
            return True, "Bem-vindo à Biblioteca Universitária!"
        except sqlite3.IntegrityError:
            return False, "O nome de usuário já está em uso na base."

    def buscar_usuario(self, username: str, senha: str):
        self.cursor.execute(
            "SELECT username, tipo_usuario FROM USUARIO WHERE username = ? AND senha = ?",
            (username, senha)
        )
        return self.cursor.fetchone()

    def registrar_emprestimo(self, username: str, livro: str):
        self.cursor.execute(
            "SELECT id FROM USUARIO WHERE username = ?",
            (username,)
        )
        resultado = self.cursor.fetchone()
        if not resultado:
            return False, "Usuário não encontrado."

        usuario_id = resultado[0]
        self.cursor.execute(
            """
            SELECT id FROM EMPRESTIMO
            WHERE usuario_id = ? AND livro = ? AND status = 'ABERTO'
            """,
            (usuario_id, livro)
        )
        if self.cursor.fetchone():
            return False, "Este livro já está em seus empréstimos abertos."

        data_emprestimo = datetime.now()
        data_prevista = data_emprestimo + timedelta(days=15)
        self.cursor.execute(
            """
            INSERT INTO EMPRESTIMO (
                usuario_id, livro, data_emprestimo, data_prevista_devolucao, dias_extensao, status
            )
            VALUES (?, ?, ?, ?, 0, 'ABERTO')
            """,
            (
                usuario_id,
                livro,
                data_emprestimo.strftime("%d/%m/%Y %H:%M"),
                data_prevista.strftime("%d/%m/%Y")
            )
        )
        self.conn.commit()
        return True, "Livro alugado com sucesso."

    def listar_emprestimos_abertos(self, username: str):
        self.cursor.execute(
            "SELECT id FROM USUARIO WHERE username = ?",
            (username,)
        )
        resultado = self.cursor.fetchone()
        if not resultado:
            return []

        usuario_id = resultado[0]
        self.cursor.execute(
            """
            SELECT id, livro, data_emprestimo, data_prevista_devolucao, dias_extensao
            FROM EMPRESTIMO
            WHERE usuario_id = ? AND status = 'ABERTO'
            ORDER BY id DESC
            """,
            (usuario_id,)
        )
        return self.cursor.fetchall()

    def obter_status_livro(self, username: str, livro: str):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return "desconhecido"
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT usuario_id FROM EMPRESTIMO
            WHERE livro = ? AND status = 'ABERTO'
            LIMIT 1
            """,
            (livro,)
        )
        emprestimo = self.cursor.fetchone()

        self.cursor.execute(
            """
            SELECT id FROM RESERVA
            WHERE livro = ? AND usuario_id = ? AND status = 'ATIVA'
            LIMIT 1
            """,
            (livro, usuario_id)
        )
        reserva_do_usuario = self.cursor.fetchone() is not None

        if not emprestimo:
            return "reservado_por_voce" if reserva_do_usuario else "disponivel"

        if emprestimo[0] == usuario_id:
            return "alugado_por_voce"

        return "reservado_por_voce" if reserva_do_usuario else "alugado"

    def devolver_emprestimo(self, username: str, emprestimo_id: int):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return False, "Usuário não encontrado."
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT livro FROM EMPRESTIMO
            WHERE id = ? AND usuario_id = ? AND status = 'ABERTO'
            """,
            (emprestimo_id, usuario_id)
        )
        registro = self.cursor.fetchone()
        if not registro:
            return False, "Empréstimo não encontrado ou já encerrado."
        livro = registro[0]

        self.cursor.execute(
            "UPDATE EMPRESTIMO SET status = 'DEVOLVIDO' WHERE id = ?",
            (emprestimo_id,)
        )

        self.cursor.execute(
            """
            SELECT id FROM RESERVA
            WHERE livro = ? AND status = 'ATIVA'
            ORDER BY id ASC
            LIMIT 1
            """,
            (livro,)
        )
        reserva = self.cursor.fetchone()
        if reserva:
            self.cursor.execute(
                "UPDATE RESERVA SET status = 'CONCLUIDA' WHERE id = ?",
                (reserva[0],)
            )

        self.conn.commit()
        return True, "Livro devolvido com sucesso."

    def estender_emprestimo(self, username: str, emprestimo_id: int):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return False, "Usuário não encontrado."
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT livro, data_prevista_devolucao, dias_extensao
            FROM EMPRESTIMO
            WHERE id = ? AND usuario_id = ? AND status = 'ABERTO'
            """,
            (emprestimo_id, usuario_id)
        )
        emprestimo = self.cursor.fetchone()
        if not emprestimo:
            return False, "Empréstimo não encontrado ou já encerrado."

        livro, data_prevista_texto, dias_extensao = emprestimo
        if dias_extensao >= 15:
            return False, "Limite de extensão atingido (máximo de 15 dias)."

        self.cursor.execute(
            """
            SELECT id FROM RESERVA
            WHERE livro = ? AND usuario_id <> ? AND status = 'ATIVA'
            LIMIT 1
            """,
            (livro, usuario_id)
        )
        if self.cursor.fetchone():
            return False, "Não é possível estender: livro reservado por outra pessoa."

        if data_prevista_texto:
            base_data = datetime.strptime(data_prevista_texto, "%d/%m/%Y")
        else:
            base_data = datetime.now() + timedelta(days=15)
        nova_data = base_data + timedelta(days=15)
        novos_dias_extensao = dias_extensao + 15
        self.cursor.execute(
            """
            UPDATE EMPRESTIMO
            SET data_prevista_devolucao = ?, dias_extensao = ?
            WHERE id = ?
            """,
            (nova_data.strftime("%d/%m/%Y"), novos_dias_extensao, emprestimo_id)
        )
        self.conn.commit()
        return True, f"Reserva estendida. Nova devolução: {nova_data.strftime('%d/%m/%Y')}."

    def reservar_livro(self, username: str, livro: str):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return False, "Usuário não encontrado."
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT id FROM EMPRESTIMO
            WHERE livro = ? AND status = 'ABERTO' AND usuario_id <> ?
            LIMIT 1
            """,
            (livro, usuario_id)
        )
        if not self.cursor.fetchone():
            return False, "Este livro não está alugado por outra pessoa no momento."

        self.cursor.execute(
            """
            SELECT id FROM RESERVA
            WHERE livro = ? AND usuario_id = ? AND status = 'ATIVA'
            """,
            (livro, usuario_id)
        )
        if self.cursor.fetchone():
            return False, "Você já possui uma reserva ativa para este livro."

        self.cursor.execute(
            """
            INSERT INTO RESERVA (usuario_id, livro, data_reserva, status)
            VALUES (?, ?, ?, 'ATIVA')
            """,
            (usuario_id, livro, datetime.now().strftime("%d/%m/%Y %H:%M"))
        )
        self.conn.commit()
        return True, "Reserva registrada com sucesso."

    def listar_reservas_ativas(self, username: str):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return []
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT id, livro, data_reserva
            FROM RESERVA
            WHERE usuario_id = ? AND status = 'ATIVA'
            ORDER BY id DESC
            """,
            (usuario_id,)
        )
        return self.cursor.fetchall()

    def listar_reservas_canceladas(self, username: str):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return []
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT livro, data_reserva, data_cancelamento
            FROM RESERVA
            WHERE usuario_id = ? AND status = 'CANCELADA'
            ORDER BY id DESC
            LIMIT 10
            """,
            (usuario_id,)
        )
        return self.cursor.fetchall()

    def cancelar_reserva(self, username: str, reserva_id: int):
        self.cursor.execute("SELECT id FROM USUARIO WHERE username = ?", (username,))
        resultado = self.cursor.fetchone()
        if not resultado:
            return False, "Usuário não encontrado."
        usuario_id = resultado[0]

        self.cursor.execute(
            """
            SELECT id FROM RESERVA
            WHERE id = ? AND usuario_id = ? AND status = 'ATIVA'
            """,
            (reserva_id, usuario_id)
        )
        if not self.cursor.fetchone():
            return False, "Reserva não encontrada ou já encerrada."

        self.cursor.execute(
            """
            UPDATE RESERVA
            SET status = 'CANCELADA', data_cancelamento = ?
            WHERE id = ?
            """,
            (datetime.now().strftime("%d/%m/%Y %H:%M"), reserva_id)
        )
        self.conn.commit()
        return True, "Reserva cancelada com sucesso."

    def fechar_conexao(self):
        self.conn.close()