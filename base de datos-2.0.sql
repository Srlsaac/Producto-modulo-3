-- Base de datos 
CREATE DATABASE IF NOT EXISTS hotelpro;
USE hotelpro;

-- Tabla clientes

CREATE TABLE clientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    documento   VARCHAR(20)  NOT NULL UNIQUE,
    telefono    VARCHAR(20),
    correo      VARCHAR(100)
);


-- Tabla habitaciones 
CREATE TABLE habitaciones (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    numero  VARCHAR(10)  NOT NULL UNIQUE,
    tipo    VARCHAR(50)  NOT NULL,
    estado  VARCHAR(30)  NOT NULL DEFAULT 'disponible',
    tarifa  DECIMAL(10,2) NOT NULL
);

-- Tabla reservas 
CREATE TABLE reservas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente      INT NOT NULL,
    id_habitacion   INT NOT NULL,
    fecha_llegada   DATE NOT NULL,
    fecha_salida    DATE NOT NULL,
    estado          VARCHAR(30) NOT NULL DEFAULT 'confirmada',
    FOREIGN KEY (id_cliente)    REFERENCES clientes(id),
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id)
);

-- Tabla checkin 
CREATE TABLE checkin (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva  INT NOT NULL,
    fecha_entrada   DATETIME,
    fecha_salida    DATETIME,
    estado      VARCHAR(30) NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (id_reserva) REFERENCES reservas(id)
);


-- STORED PROCEDURES


-- CLIENTES 
DELIMITER //

CREATE PROCEDURE sp_crear_cliente(IN p_nombre VARCHAR(100), IN p_apellido VARCHAR(100),
    IN p_documento VARCHAR(20), IN p_telefono VARCHAR(20), IN p_correo VARCHAR(100))
BEGIN
    INSERT INTO clientes(nombre, apellido, documento, telefono, correo)
    VALUES(p_nombre, p_apellido, p_documento, p_telefono, p_correo);
END //

CREATE PROCEDURE sp_obtener_clientes()
BEGIN
    SELECT * FROM clientes;
END// 

CREATE PROCEDURE sp_actualizar_cliente(IN p_id INT, IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100), IN p_documento VARCHAR(20),
    IN p_telefono VARCHAR(20), IN p_correo VARCHAR(100))
BEGIN
    UPDATE clientes SET nombre=p_nombre, apellido=p_apellido, documento=p_documento,
    telefono=p_telefono, correo=p_correo WHERE id=p_id;
END//

CREATE PROCEDURE sp_eliminar_cliente(IN p_id INT)
BEGIN
    DELETE FROM clientes WHERE id=p_id;
END//

-- HABITACIONES 
CREATE PROCEDURE sp_crear_habitacion(IN p_numero VARCHAR(10), IN p_tipo VARCHAR(50),
    IN p_estado VARCHAR(30), IN p_tarifa DECIMAL(10,2))
BEGIN
    INSERT INTO habitaciones(numero, tipo, estado, tarifa)
    VALUES(p_numero, p_tipo, p_estado, p_tarifa);
END//

CREATE PROCEDURE sp_obtener_habitaciones()
BEGIN
    SELECT * FROM habitaciones;
END//

CREATE PROCEDURE sp_actualizar_habitacion(IN p_id INT, IN p_numero VARCHAR(10),
    IN p_tipo VARCHAR(50), IN p_estado VARCHAR(30), IN p_tarifa DECIMAL(10,2))
BEGIN
    UPDATE habitaciones SET numero=p_numero, tipo=p_tipo, estado=p_estado,
    tarifa=p_tarifa WHERE id=p_id;
END//

CREATE PROCEDURE sp_eliminar_habitacion(IN p_id INT)
BEGIN
    DELETE FROM habitaciones WHERE id=p_id;
END//

-- RESERVAS 
CREATE PROCEDURE sp_crear_reserva(IN p_id_cliente INT, IN p_id_habitacion INT,
    IN p_fecha_llegada DATE, IN p_fecha_salida DATE, IN p_estado VARCHAR(30))
BEGIN
    INSERT INTO reservas(id_cliente, id_habitacion, fecha_llegada, fecha_salida, estado)
    VALUES(p_id_cliente, p_id_habitacion, p_fecha_llegada, p_fecha_salida, p_estado);
END//

CREATE PROCEDURE sp_obtener_reservas()
BEGIN
    SELECT r.id, c.nombre, c.apellido, h.numero, r.fecha_llegada, r.fecha_salida, r.estado
    FROM reservas r
    JOIN clientes c ON r.id_cliente = c.id
    JOIN habitaciones h ON r.id_habitacion = h.id;
END//

CREATE PROCEDURE sp_actualizar_reserva(IN p_id INT, IN p_fecha_llegada DATE,
    IN p_fecha_salida DATE, IN p_estado VARCHAR(30))
BEGIN
    UPDATE reservas SET fecha_llegada=p_fecha_llegada, fecha_salida=p_fecha_salida,
    estado=p_estado WHERE id=p_id;
END//

CREATE PROCEDURE sp_eliminar_reserva(IN p_id INT)
BEGIN
    DELETE FROM reservas WHERE id=p_id;
END//

-- CHECKIN 
CREATE PROCEDURE sp_crear_checkin(IN p_id_reserva INT, IN p_fecha_entrada DATETIME)
BEGIN
    INSERT INTO checkin(id_reserva, fecha_entrada, estado)
    VALUES(p_id_reserva, p_fecha_entrada, 'activo');
END//

CREATE PROCEDURE sp_obtener_checkins()
BEGIN
    SELECT ck.id, r.id AS reserva, c.nombre, c.apellido, h.numero,
    ck.fecha_entrada, ck.fecha_salida, ck.estado
    FROM checkin ck
    JOIN reservas r ON ck.id_reserva = r.id
    JOIN clientes c ON r.id_cliente = c.id
    JOIN habitaciones h ON r.id_habitacion = h.id;
END//

CREATE PROCEDURE sp_checkout(IN p_id INT, IN p_fecha_salida DATETIME)
BEGIN
    UPDATE checkin SET fecha_salida=p_fecha_salida, estado='completado' WHERE id=p_id;
END//

CREATE PROCEDURE sp_eliminar_checkin(IN p_id INT)
BEGIN
    DELETE FROM checkin WHERE id=p_id;
END//

DELIMITER ;