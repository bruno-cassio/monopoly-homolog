-- Estrutura inicial do banco para o Simulador (PostgreSQL)

CREATE TABLE IF NOT EXISTS player_profile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    behavior_type VARCHAR(20) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS board_property (
    id SERIAL PRIMARY KEY,
    position INT NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
    purchase_price NUMERIC(10,2) NOT NULL,
    rent_price NUMERIC(10,2) NOT NULL,
    color_group VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    execution_time FLOAT,
    winner VARCHAR(100),
    details_json JSONB,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS game_result (
    id SERIAL PRIMARY KEY,
    log_id INT REFERENCES game_log(id),
    total_rounds INT,
    winner_id INT REFERENCES player_profile(id),
    duration FLOAT,
    finished_reason VARCHAR(50),
    status VARCHAR(20) DEFAULT 'IN_PROGRESS',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_round (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game_result(id),
    round_number INT NOT NULL,
    summary JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS game_property_state (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game_result(id),
    property_id INT REFERENCES board_property(id),
    owner_id INT REFERENCES player_profile(id),
    purchase_price NUMERIC(10,2),
    current_rent NUMERIC(10,2),
    times_rented INT DEFAULT 0,
    times_purchased INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS player_stats (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game_result(id),
    player_id INT REFERENCES player_profile(id),
    final_balance NUMERIC(10,2),
    properties_owned INT,
    properties_bought INT,
    rent_paid_qty INT,
    rent_received_qty INT,
    rent_paid_total NUMERIC(10,2),
    rent_received_total NUMERIC(10,2),
    total_spent NUMERIC(10,2),
    total_earned NUMERIC(10,2),
    turns_survived INT,
    avg_rent_paid NUMERIC(10,2),
    avg_rent_received NUMERIC(10,2),
    net_result NUMERIC(10,2),
    efficiency_ratio NUMERIC(10,2),
    total_transactions INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir jogadores padrão
INSERT INTO player_profile (name, behavior_type) VALUES
('Impulsivo', 'impulsivo'),
('Exigente', 'exigente'),
('Cauteloso', 'cauteloso'),
('Aleatório', 'aleatorio');

-- Inserir propriedades padrão (nomes de estádios europeus)
INSERT INTO board_property (position, name, purchase_price, rent_price, color_group) VALUES
(1, 'Rua Camp Nou', 100, 30, 'Azul'),
(2, 'Rua Santiago Bernabéu', 110, 35, 'Azul'),
(3, 'Rua Old Trafford', 120, 40, 'Verde'),
(4, 'Rua Anfield', 130, 45, 'Verde'),
(5, 'Rua Emirates', 140, 50, 'Roxo'),
(6, 'Rua Stamford Bridge', 150, 55, 'Roxo'),
(7, 'Rua Allianz Arena', 160, 60, 'Amarelo'),
(8, 'Rua San Siro', 170, 65, 'Amarelo'),
(9, 'Rua Parc des Princes', 180, 70, 'Vermelho'),
(10, 'Rua Signal Iduna Park', 190, 75, 'Vermelho'),
(11, 'Rua Johan Cruyff Arena', 200, 80, 'Laranja'),
(12, 'Rua Celtic Park', 210, 85, 'Laranja'),
(13, 'Rua Estádio da Luz', 220, 90, 'Rosa'),
(14, 'Rua Dragão', 230, 95, 'Rosa'),
(15, 'Rua Giuseppe Meazza', 240, 100, 'Marrom'),
(16, 'Rua Wanda Metropolitano', 250, 105, 'Marrom'),
(17, 'Rua King Power Stadium', 260, 110, 'Cinza'),
(18, 'Rua Etihad Stadium', 270, 115, 'Cinza'),
(19, 'Rua Tottenham Hotspur Stadium', 280, 120, 'Preto'),
(20, 'Rua Olímpico de Roma', 300, 130, 'Preto');
