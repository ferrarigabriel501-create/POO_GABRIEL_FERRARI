class LimiteEmprestimosExcedido(Exception):
    pass


class LivroIndisponivel(Exception):
    pass


class UsuarioNaoEncontrado(Exception):
    pass


class LivroNaoEncontrado(Exception):
    pass


class Livro:
    def __init__(self, isbn, titulo, autor, disponivel=True):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.disponivel = disponivel

    def emprestar(self):
        self.disponivel = False

    def devolver(self):
        self.disponivel = True


class Usuario:
    def __init__(self, matricula, nome, limite):
        self.matricula = matricula
        self.nome = nome
        self.livros_emprestados = []
        self.limite = limite

    def pegar_emprestado(self, livro):
        if len(self.livros_emprestados) >= self.limite:
            raise LimiteEmprestimosExcedido(
                f"{self.nome} atingiu o limite de {self.limite} livros."
            )

        if not livro.disponivel:
            raise LivroIndisponivel(
                f"O livro '{livro.titulo}' não está disponível."
            )

        self.livros_emprestados.append(livro)
        livro.emprestar()

    def devolver_livro(self, livro):
        if livro in self.livros_emprestados:
            self.livros_emprestados.remove(livro)
            livro.devolver()


class Aluno(Usuario):
    def __init__(self, matricula, nome):
        super().__init__(matricula, nome, 3)


class Professor(Usuario):
    def __init__(self, matricula, nome):
        super().__init__(matricula, nome, 5)


class Biblioteca:
    def __init__(self):
        self.acervo = []
        self.usuarios_cadastrados = []

    def cadastrar_usuario(self, usuario):
        self.usuarios_cadastrados.append(usuario)

    def cadastrar_livro(self, livro):
        self.acervo.append(livro)

    def buscar_usuario(self, matricula):
        for usuario in self.usuarios_cadastrados:
            if usuario.matricula == matricula:
                return usuario
        raise UsuarioNaoEncontrado("Usuário não encontrado.")

    def buscar_livro(self, isbn):
        for livro in self.acervo:
            if livro.isbn == isbn:
                return livro
        raise LivroNaoEncontrado("Livro não encontrado.")

    def registrar_emprestimo(self, matricula, isbn):
        usuario = self.buscar_usuario(matricula)
        livro = self.buscar_livro(isbn)
        usuario.pegar_emprestado(livro)

    def consultar_livros_emprestados(self):
        for usuario in self.usuarios_cadastrados:
            print(f"\nUsuário: {usuario.nome} ({usuario.matricula})")
            if len(usuario.livros_emprestados) == 0:
                print("Nenhum livro emprestado.")
            else:
                for livro in usuario.livros_emprestados:
                    print(f"- {livro.titulo} ({livro.isbn})")

# TESTE DO SISTEMA

biblioteca = Biblioteca()

biblioteca.cadastrar_livro(Livro("LIV001", "Titulo 1", "Autor 1"))
biblioteca.cadastrar_livro(Livro("LIV002", "Titulo 2", "Autor 2"))
biblioteca.cadastrar_livro(Livro("LIV003", "Titulo 3", "Autor 3"))
biblioteca.cadastrar_livro(Livro("LIV004", "Titulo 4", "Autor 4"))
biblioteca.cadastrar_livro(Livro("LIV005", "Titulo 5", "Autor 5"))

aluno1 = Aluno("ALUNOXX1", "Nome 1")
aluno2 = Aluno("ALUNOXX2", "Nome 2")
professor1 = Professor("PROFXX1", "Professor")

biblioteca.cadastrar_usuario(aluno1)
biblioteca.cadastrar_usuario(aluno2)
biblioteca.cadastrar_usuario(professor1)

try:
    biblioteca.registrar_emprestimo("ALUNOXX1", "LIV001")
    biblioteca.registrar_emprestimo("ALUNOXX1", "LIV002")
    biblioteca.registrar_emprestimo("ALUNOXX1", "LIV003")

    # Esse vai gerar exceção porque aluno só pode pegar 3
    biblioteca.registrar_emprestimo("ALUNOXX1", "LIV004")

except Exception as e:
    print("Erro:", e)

biblioteca.consultar_livros_emprestados()