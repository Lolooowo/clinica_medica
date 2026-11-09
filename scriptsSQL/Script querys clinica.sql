USE clinica_medica;

INSERT INTO tipo_sangre(tipo_sangre) VALUES ('A'), ('A+'), ('A-'), ('B'),('B+'),('B-'),('AB'),('AB+'),('AB-'), ('O'), ('O+'), ('O-');
SELECT * FROM tipo_sangre;

SELECT * FROM paciente;
SELECT * FROM alergia;
SELECT * FROM alergia_paciente;
SELECT p.id_paciente, p.nombres, p.apellidos, p.fecha_nacimiento, coalesce(ts.tipo_sangre, 'N/A') AS tipo_sangre FROM paciente p
LEFT JOIN paciente_sangre ps ON p.id_paciente = ps.id_paciente
LEFT JOIN tipo_sangre ts ON ps.id_paciente = ts.id_tipo_sangre ORDER BY p.id_paciente DESC; 

CREATE OR REPLACE VIEW `vista_personal_usuario` AS
SELECT
    p.id_personal,
    p.nombres,
    p.apellidos,
    COALESCE(r.nombre_rol, 'Sin rol') AS rol,
    u.nombre_usuario,
    CASE
        WHEN u.password_hash IS NULL THEN 'Pendiente'
        ELSE 'Configurada'
    END AS estado_contrasena,
    u.activo,
    COALESCE(nc.numero_colegiado, 'N/A') AS numero_colegiado
FROM personal p
LEFT JOIN usuario u ON p.id_personal = u.id_personal
LEFT JOIN personal_rol pr ON p.id_personal = pr.id_personal
LEFT JOIN rol r ON pr.id_rol = r.id_rol
LEFT JOIN personal_numero_colegiado pnc ON p.id_personal = pnc.id_personal
LEFT JOIN numero_colegiado nc ON pnc.id_numero_colegiado = nc.id_numero_colegiado;

SELECT * FROM vista_personal_usuario;



DELIMITER //
CREATE TRIGGER `paciente_before_insert`
BEFORE INSERT ON `paciente`
FOR EACH ROW
BEGIN
    IF NEW.fecha_nacimiento > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de nacimiento no puede ser futura';
    END IF;
    IF TRIM(NEW.nombres) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nombre del paciente no puede estar vacio';
	ELSEIF TRIM(NEW.apellidos) = '' THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'El apellido del paciente no puede quedar vacío';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER `paciente_before_update`
BEFORE UPDATE ON `paciente`
FOR EACH ROW
BEGIN
    IF NEW.fecha_nacimiento > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de nacimiento no puede ser futura';
    END IF;
    IF TRIM(NEW.nombres) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nombre del paciente no puede estar vacio';
        ELSEIF TRIM(NEW.apellidos) = '' THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'El apellido del paciente no puede quedar vacío';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER `alergia_before_insert`
BEFORE INSERT ON `alergia`
FOR EACH ROW
BEGIN
    SET NEW.nombre_alergia = LOWER(TRIM(NEW.nombre_alergia));
    IF NEW.nombre_alergia = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nombre de la alergia no puede estar vacio';
    END IF;
END//
DELIMITER //
CREATE TRIGGER `alergia_before_update`
BEFORE UPDATE ON `alergia`
FOR EACH ROW
BEGIN
    SET NEW.nombre_alergia = LOWER(TRIM(NEW.nombre_alergia));

    IF NEW.nombre_alergia = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El nombre de la alergia no puede estar vacio';
    END IF;
END//

DELIMITER ;
SHOW TRIGGERS;

DROP TRIGGER alergia_before_insert;

SELECT p.id_paciente, p.nombres, p.apellidos, p.fecha_nacimiento, 
            COALESCE(ts.tipo_sangre, 'N/A'), 
            COALESCE(GROUP_CONCAT(a.nombre_alergia SEPARATOR ', '), 'Sin alergias') 
            FROM paciente p 
            LEFT JOIN paciente_sangre ps ON p.id_paciente = ps.id_paciente 
            LEFT JOIN tipo_sangre ts ON ps.id_tipo_sangre = ts.id_tipo_sangre 
            LEFT JOIN alergia_paciente ap ON p.id_paciente = ap.id_paciente 
            LEFT JOIN alergia a ON ap.id_alergia = a.id_alergia 
            GROUP BY p.id_paciente, p.nombres, p.apellidos, p.fecha_nacimiento, ts.tipo_sangre 
            ORDER BY p.id_paciente DESC;

CREATE VIEW vista_pacientes AS
SELECT
    p.id_paciente,
    p.nombres,
    p.apellidos,
    p.fecha_nacimiento,
    COALESCE(ts.tipo_sangre, 'N/A') AS tipo_sangre,
    COALESCE(GROUP_CONCAT(a.nombre_alergia SEPARATOR ', '), 'Sin alergias') AS alergias
FROM paciente p
LEFT JOIN paciente_sangre ps ON p.id_paciente = ps.id_paciente
LEFT JOIN tipo_sangre ts ON ps.id_tipo_sangre = ts.id_tipo_sangre
LEFT JOIN alergia_paciente ap ON p.id_paciente = ap.id_paciente
LEFT JOIN alergia a ON ap.id_alergia = a.id_alergia
GROUP BY p.id_paciente, p.nombres, p.apellidos, p.fecha_nacimiento, ts.tipo_sangre;
            
SELECT * FROM vista_pacientes;
SELECT * FROM personal;
SELECT * FROM rol;



CREATE OR REPLACE VIEW `vista_personal` AS
SELECT
    p.id_personal,
    p.nombres,
    p.apellidos,
    COALESCE(r.nombre_rol, 'Sin rol') AS rol,
    COALESCE(nc.numero_colegiado, 'N/A') AS numero_colegiado
FROM personal p
LEFT JOIN personal_rol pr ON p.id_personal = pr.id_personal
LEFT JOIN rol r ON pr.id_rol = r.id_rol
LEFT JOIN personal_numero_colegiado pnc ON p.id_personal = pnc.id_personal
LEFT JOIN numero_colegiado nc ON pnc.id_numero_colegiado = nc.id_numero_colegiado;
 
INSERT INTO rol(nombre_rol) values ('Médico'), ('Enfermera'), ('Recepcionista');
SELECT * FROM vista_personal;
DELIMITER //

CREATE TRIGGER `numero_colegiado_before_insert`
BEFORE INSERT ON `numero_colegiado`
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM numero_colegiado
        WHERE numero_colegiado = NEW.numero_colegiado
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ese numero de colegiado ya esta registrado';
    END IF;
END//


DELIMITER //
CREATE TRIGGER `numero_colegiado_before_update`
BEFORE UPDATE ON `numero_colegiado`
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM numero_colegiado
        WHERE numero_colegiado = NEW.numero_colegiado
        AND id_numero_colegiado != NEW.id_numero_colegiado
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Ese numero de colegiado ya esta registrado';
    END IF;
END//

DELIMITER ;

DELIMITER //

CREATE TRIGGER `personal_after_insert`
AFTER INSERT ON `personal`
FOR EACH ROW
BEGIN
    DECLARE v_usuario VARCHAR(50);

    -- Iniciales
    SET v_usuario = CONCAT(
        LOWER(SUBSTRING(NEW.nombres, 1, 1)),
        '.',
        LOWER(SUBSTRING(NEW.apellidos, 1, 1)),
        NEW.id_personal
    );

    -- Normaliza vocales acentuadas a minusculas sin acento
    SET v_usuario = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(v_usuario,
        'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o'), 'ú', 'u');

    -- Inserta el usuario
    INSERT INTO usuario (id_personal, nombre_usuario, password_hash, activo)
    VALUES (NEW.id_personal, v_usuario, NULL, 1);
END//

DELIMITER ;

DELIMITER //

CREATE PROCEDURE `sp_consultas_pendientes` (
    IN p_id_medico INT
)
BEGIN
    SELECT
        c.id_consulta,
        CONCAT(p.nombres, ' ', p.apellidos) AS paciente,
        c.fecha_hora,
        c.motivo_visita,
        COALESCE(ts.tipo_sangre, 'N/A') AS tipo_sangre,
        COALESCE(GROUP_CONCAT(a.nombre_alergia SEPARATOR ', '), 'Sin alergias') AS alergias
    FROM consulta c
    JOIN paciente p ON c.id_paciente = p.id_paciente
    LEFT JOIN paciente_sangre ps ON p.id_paciente = ps.id_paciente
    LEFT JOIN tipo_sangre ts ON ps.id_tipo_sangre = ts.id_tipo_sangre
    LEFT JOIN alergia_paciente ap ON p.id_paciente = ap.id_paciente
    LEFT JOIN alergia a ON ap.id_alergia = a.id_alergia
    LEFT JOIN detalles_consulta dc ON c.id_consulta = dc.id_consulta
    WHERE c.id_medico = p_id_medico
      AND dc.id_consulta IS NULL
    GROUP BY c.id_consulta, p.nombres, p.apellidos, c.fecha_hora,
             c.motivo_visita, ts.tipo_sangre
    ORDER BY c.fecha_hora ASC;
END//

DELIMITER ;

INSERT INTO personal (nombres, apellidos) VALUES ('Juan', 'Perez');
SELECT * FROM usuario;
SELECT * FROM personal;
SELECT     p.id_personal,     p.nombres,     p.apellidos,     COALESCE(r.nombre_rol, 'Sin rol') AS rol,     COALESCE(nc.numero_colegiado, 'N/A') AS numero_colegiado FROM personal p LEFT JOIN personal_rol pr ON p.id_personal = pr.id_personal LEFT JOIN rol r ON pr.id_rol = r.id_rol LEFT JOIN personal_numero_colegiado pnc ON p.id_personal = pnc.id_personal LEFT JOIN numero_colegiado nc ON pnc.id_numero_colegiado = nc.id_numero_colegiado LIMIT 0, 1000;
CALL sp_consultas_pendientes(5);

SELECT
    dc.id_detalles_consulta,
    dc.id_consulta,
    dc.diagnostico,
    dc.nota_medica,
    c.fecha_hora
FROM detalles_consulta dc
JOIN consulta c        ON c.id_consulta = dc.id_consulta
ORDER BY dc.id_detalles_consulta DESC
LIMIT 1;


CREATE OR REPLACE VIEW vista_historial_paciente AS
SELECT
    p.id_paciente,
    CONCAT(p.nombres, ' ', p.apellidos) AS paciente,
    p.fecha_nacimiento,
    ts.tipo_sangre,
    COALESCE(GROUP_CONCAT(DISTINCT a.nombre_alergia SEPARATOR ', '), 'Sin alergias') AS alergias,
    c.id_consulta,
    c.fecha_hora AS fecha_consulta,
    c.motivo_visita AS motivo_visita,
    CONCAT(med.nombres, ' ', med.apellidos) AS medico,
    dc.diagnostico,
    dc.nota_medica,
    COALESCE(
        (SELECT GROUP_CONCAT(CONCAT('• ', dr.nombre_medicamento, ' (', dr.dosis, ')') SEPARATOR '\n')
         FROM receta r
         JOIN detalles_receta dr ON r.id_receta = dr.id_receta
         WHERE r.id_consulta = c.id_consulta),
        'Sin receta'
    ) AS receta_medica

FROM paciente p
LEFT JOIN paciente_sangre ps ON ps.id_paciente = p.id_paciente
LEFT JOIN tipo_sangre ts ON ts.id_tipo_sangre = ps.id_tipo_sangre
LEFT JOIN alergia_paciente ap ON ap.id_paciente = p.id_paciente
LEFT JOIN alergia a ON a.id_alergia = ap.id_alergia
LEFT JOIN consulta c ON c.id_paciente = p.id_paciente
LEFT JOIN personal med ON med.id_personal = c.id_medico
LEFT JOIN detalles_consulta dc ON dc.id_consulta = c.id_consulta
GROUP BY
    p.id_paciente, p.nombres, p.apellidos, p.fecha_nacimiento, ts.tipo_sangre,
    c.id_consulta, c.fecha_hora, c.motivo_visita, med.nombres, med.apellidos,
    dc.diagnostico, dc.nota_medica;
    
SELECT * FROM vista_historial_paciente WHERE id_paciente = 1;

SELECT * FROM usuario;
