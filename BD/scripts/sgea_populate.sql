-- SCRIPT DE CRIAÇÃO E POPULAÇÃO INICIAL DO BANCO DE DADOS (sgea_populate.sql)

-- 1. Criação da Tabela Usuário
CREATE TABLE Usuario (
    usuario_id INT PRIMARY KEY NOT NULL,
    nome CHAR(50) NOT NULL,
    telefone CHAR(50) NOT NULL,
    instituicao_ensino CHAR(50), -- Opcional, pois na sua ER o NOT NULL foi removido, mas no requisito é obrigatório para alunos/professores. Manteremos como NOT NULL para simular o requisito.
    login CHAR(50) NOT NULL UNIQUE,
    senha CHAR(50) NOT NULL, -- Em um projeto real, use hash para senhas!
    perfil CHAR(50) NOT NULL CHECK (perfil IN ('Aluno', 'Professor', 'Organizador'))
);

-- 2. Criação da Tabela Evento
CREATE TABLE Evento (
    evento_id INT PRIMARY KEY NOT NULL,
    organizador_id INT NOT NULL,
    tipo_evento CHAR(50) NOT NULL,
    data_inicial DATE NOT NULL,
    data_final DATE NOT NULL,
    horario CHAR(50) NOT NULL,
    local CHAR(50) NOT NULL,
    quantidade_participantes INT NOT NULL,
    FOREIGN KEY (organizador_id) REFERENCES Usuario(usuario_id)
);

-- 3. Criação da Tabela Inscrição
CREATE TABLE Inscricao (
    inscricao_id INT PRIMARY KEY NOT NULL,
    usuario_id INT NOT NULL,
    evento_id INT NOT NULL,
    UNIQUE (usuario_id, evento_id), -- Garante que um usuário só se inscreve uma vez no mesmo evento
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    FOREIGN KEY (evento_id) REFERENCES Evento(evento_id)
);

-- 4. Criação da Tabela Certificado
CREATE TABLE Certificado (
    certificado_id INT PRIMARY KEY NOT NULL,
    inscricao_id INT NOT NULL UNIQUE,
    data_emissao DATE NOT NULL,
    texto_certificado CHAR(50) NOT NULL,
    status_emissao CHAR(50) NOT NULL CHECK (status_emissao IN ('Pendente', 'Emitido')),
    FOREIGN KEY (inscricao_id) REFERENCES Inscricao(inscricao_id)
);

-- POPULAÇÃO INICIAL (Dados de Exemplo)

-- Inserir Usuários (Organizadores, Aluno, Professor)
INSERT INTO Usuario (usuario_id, nome, telefone, instituicao_ensino, login, senha, perfil) VALUES
(1, 'João Organizador', '9999-1111', 'Universidade X', 'joao.org', 'senha123', 'Organizador'),
(2, 'Maria Professor', '9999-2222', 'Universidade X', 'maria.prof', 'senha123', 'Professor'),
(3, 'Carlos Aluno', '9999-3333', 'Faculdade Y', 'carlos.aluno', 'senha123', 'Aluno');


-- Inserir Eventos (organizador_id deve ser de um usuário 'Organizador')
INSERT INTO Evento (evento_id, organizador_id, tipo_evento, data_inicial, data_final, horario, local, quantidade_participantes) VALUES
(101, 1, 'Palestra', '2025-11-15', '2025-11-15', '14:00', 'Auditório Principal', 100),
(102, 1, 'Minicurso', '2025-12-01', '2025-12-03', '19:00', 'Sala B-201', 50),
(103, 1, 'Seminário', '2026-01-20', '2026-01-20', '10:00', 'Online (Zoom)', 200);

-- Inserir Inscrições (usuário 2 inscrito no evento 101, usuário 3 inscrito no evento 101)
INSERT INTO Inscricao (inscricao_id, usuario_id, evento_id) VALUES
(201, 2, 101),
(202, 3, 101),
(203, 2, 102);

-- Inserir Certificados
INSERT INTO Certificado (certificado_id, inscricao_id, data_emissao, texto_certificado, status_emissao) VALUES
(301, 201, '2025-11-20', 'Certificado de Participação na Palestra', 'Emitido'),
(302, 202, '2025-11-20', 'Certificado de Participação na Palestra', 'Emitido');