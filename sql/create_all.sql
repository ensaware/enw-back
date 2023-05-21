/*
  _____                                        
 | ____|_ __  ___  __ ___      ____ _ _ __ ___ 
 |  _| | '_ \/ __|/ _` \ \ /\ / / _` | '__/ _ \
 | |___| | | \__ \ (_| |\ V  V / (_| | | |  __/
 |_____|_| |_|___/\__,_| \_/\_/ \__,_|_|  \___|
                                               
*/

-- ----------------------
-- Create career table --
-- ----------------------
CREATE TABLE IF NOT EXISTS career (
	id VARCHAR(60) NOT NULL DEFAULT (UUID()),
	name VARCHAR(100) NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified TIMESTAMP NULL,
	CONSTRAINT pk_career_id PRIMARY KEY (id),
	CONSTRAINT unq_career_name UNIQUE (name)
);


-- -----------------------
-- Create profile table --
-- -----------------------
CREATE TABLE IF NOT EXISTS profile (
	id VARCHAR(60) NOT NULL DEFAULT (UUID()),
	name VARCHAR(100) NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified TIMESTAMP NULL,
	CONSTRAINT pk_profile_id PRIMARY KEY (id),
	CONSTRAINT unq_profile_name UNIQUE (name)
);


-- --------------------
-- Create user table --
-- --------------------
CREATE TABLE IF NOT EXISTS user (
	id VARCHAR(60) NOT NULL DEFAULT (UUID()),
	provider_id VARCHAR(60) NOT NULL,
	provider VARCHAR(50) NOT NULL,
	display_name VARCHAR(255) NOT NULL,
	email VARCHAR(100) NOT NULL,
	picture VARCHAR(255) NULL,
	profile_id VARCHAR(60) NOT NULL,
	career_id VARCHAR(60) NULL,
	refresh_token VARCHAR(255) NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	modified TIMESTAMP NULL,
	CONSTRAINT pk_user_id PRIMARY KEY (id),
	CONSTRAINT unq_user_email UNIQUE (email),
	-- CONSTRAINT fk_user_profile_id FOREIGN KEY (profile_id) REFERENCES profile (id),
	-- CONSTRAINT fk_user_career_id FOREIGN KEY (career_id) REFERENCES career (id),
	CONSTRAINT unq_user_refresh_token UNIQUE (refresh_token)
);

-- Create indexes
CREATE INDEX idx_user_provider ON user (provider);