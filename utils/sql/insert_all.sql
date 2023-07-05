/*
  _____                                        
 | ____|_ __  ___  __ ___      ____ _ _ __ ___ 
 |  _| | '_ \/ __|/ _` \ \ /\ / / _` | '__/ _ \
 | |___| | | \__ \ (_| |\ V  V / (_| | | |  __/
 |_____|_| |_|___/\__,_| \_/\_/ \__,_|_|  \___|
                                               
*/

-- ------------------------------
-- Insert 'estudiante' profile --
-- ------------------------------
INSERT INTO profile (name) VALUES ('estudiante');

-- ----------------------------
-- Insert 'profesor' profile --
-- ----------------------------
INSERT INTO profile (name) VALUES ('profesor');

-- ----------------------------------
-- Insert 'administrativo' profile --
-- ----------------------------------
INSERT INTO profile (name) VALUES ('administrativo');

-- ---------------------------------
-- Insert 'administrador' profile --
-- ---------------------------------
INSERT INTO profile (name) VALUES ('administrador');


-- ----------------
-- Insert career --
-- ----------------
INSERT INTO career (name)
    SELECT 'Administración de Empresas' UNION
    SELECT 'Ingeniería de Sistemas' UNION
    SELECT 'Ingeniería Industrial' UNION
    SELECT 'Licenciatura en Pedagogía de la Primera Infancia' UNION
    SELECT 'Negocios Internacionales' UNION
    SELECT 'Psicología' UNION
    SELECT 'Técnica Profesional en Procesos Contables' UNION
    SELECT 'Técnica Profesional en Procesos Logísticos y de Comercio Exterior' UNION
    SELECT 'Técnica Profesional en Procesos Turísticos y Hoteleros' UNION
    SELECT 'Derecho';


-- ----------------------
-- Insert content_type --
-- ----------------------
INSERT INTO content_type (model)
    SELECT 'permission' UNION
    SELECT 'user';


-- --------------------
-- Insert permission --
-- --------------------
INSERT INTO permission (content_type_id, code_name, description)
    SELECT id, CONCAT(model, ':create'), 'Crear permisos' FROM content_type WHERE model = 'permission' UNION
    SELECT id, CONCAT(model, ':read'), 'Leer permisos' FROM content_type WHERE model = 'permission' UNION
    SELECT id, CONCAT(model, ':update'), 'Editar permisos' FROM content_type WHERE model = 'permission' UNION
    SELECT id, CONCAT(model, ':delete'), 'Eliminar permisos' FROM content_type WHERE model = 'permission' UNION
    SELECT id, CONCAT(model, ':create'), 'Crear Usuarios' FROM content_type WHERE model = 'user' UNION
    SELECT id, CONCAT(model, ':read'), 'Leer Usuarios' FROM content_type WHERE model = 'user' UNION
    SELECT id, CONCAT(model, ':update'), 'Editar Usuarios' FROM content_type WHERE model = 'user' UNION
    SELECT id, CONCAT(model, ':delete'), 'Eliminar Usuarios' FROM content_type WHERE model = 'user'