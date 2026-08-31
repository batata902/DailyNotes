PRAGMA encoding = "UTF-8";

CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS news(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL UNIQUE,
    body TEXT NOT NULL,
    author TEXT NOT NULL,
    category INTEGER,

    FOREIGN KEY (category) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS subscribers(
    id INTEGER PRIMARY KEY,
    email TEXT NOT NULL UNIQUE
);


INSERT OR IGNORE INTO users(email, password) VALUES ('admin@dailynote.corp', '1583981ce28aa0bbd133ac7a1e7e9eda');

INSERT OR IGNORE INTO category(title) VALUES ('Tecnologia'), ('Política'), ('Ciência'), ('Esportes'), ('Entretenimento');

INSERT OR IGNORE INTO news (title, body, author, category) VALUES
(
    'Nova tecnologia promete revolucionar os computadores',
    'Pesquisadores apresentaram uma nova tecnologia capaz de aumentar significativamente o desempenho dos computadores.',
    'João Silva',
    1
),
(
    'Empresa lança novo sistema operacional',
    'Uma empresa de tecnologia anunciou seu novo sistema operacional com foco em segurança e desempenho.',
    'Maria Santos',
    1
),
(
    'Python ganha nova atualização',
    'A comunidade Python anunciou uma nova versão da linguagem com diversas melhorias.',
    'Carlos Oliveira',
    1
),
(
    'Congresso debate novas medidas econômicas',
    'Parlamentares se reuniram nesta semana para discutir novas medidas para a economia.',
    'Ana Costa',
    2
),
(
    'Governo anuncia novo programa nacional',
    'O governo anunciou um novo programa destinado a melhorar serviços públicos.',
    'Pedro Almeida',
    2
),
(
    'Eleições municipais se aproximam',
    'Partidos começam a organizar suas campanhas para as próximas eleições municipais.',
    'Lucas Ferreira',
    2
),
(
    'Astrônomos descobrem novo exoplaneta',
    'Uma equipe internacional de astrônomos identificou um novo planeta fora do Sistema Solar.',
    'Fernanda Lima',
    3
),
(
    'Pesquisa revela novos dados sobre o universo',
    'Cientistas publicaram novos resultados sobre a formação e evolução do universo.',
    'Rafael Martins',
    3
),
(
    'Cientistas desenvolvem novo material sustentável',
    'Pesquisadores desenvolveram um material que pode reduzir o impacto ambiental da indústria.',
    'Juliana Rocha',
    3
),
(
    'Time local conquista campeonato',
    'O time local venceu a final e conquistou o título após uma partida emocionante.',
    'Bruno Souza',
    4
),
(
    'Grande final acontece neste domingo',
    'As duas melhores equipes da competição se enfrentam neste domingo pela grande final.',
    'Gabriel Mendes',
    4
),
(
    'Atleta quebra recorde nacional',
    'Um atleta brasileiro conseguiu superar o recorde nacional durante a competição.',
    'Marcos Pereira',
    4
),
(
    'Novo filme chega aos cinemas',
    'O novo filme de ação estreia nos cinemas nesta semana e já chama atenção do público.',
    'Beatriz Gomes',
    5
),
(
    'Série se torna sucesso mundial',
    'A nova série lançada recentemente alcançou milhões de espectadores em diversos países.',
    'Larissa Alves',
    5
),
(
    'Festival de música anuncia atrações',
    'O festival anunciou sua programação oficial com diversos artistas nacionais e internacionais.',
    'Daniel Ribeiro',
    5
);

INSERT OR IGNORE INTO subscribers (email) VALUES
    ('alice@example.com'),
    ('bruno@example.com'),
    ('carlos@example.com'),
    ('daniela@example.com'),
    ('eduardo@example.com'),
    ('fernanda@example.com'),
    ('gabriel@example.com'),
    ('helena@example.com'),
    ('igor@example.com'),
    ('juliana@example.com'),
    ('lucas@example.com'),
    ('mariana@example.com'),
    ('nicolas@example.com'),
    ('olivia@example.com'),
    ('paulo@example.com'),
    ('rafaela@example.com'),
    ('ricardo@example.com'),
    ('sabrina@example.com'),
    ('thiago@example.com'),
    ('vanessa@example.com'),
    ('william@example.com'),
    ('amanda@example.com'),
    ('beatriz@example.com'),
    ('caio@example.com'),
    ('diego@example.com'),
    ('elisa@example.com'),
    ('felipe@example.com'),
    ('gabriela@example.com'),
    ('henrique@example.com'),
    ('isabela@example.com');
