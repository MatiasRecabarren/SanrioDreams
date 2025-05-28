DROP TABLE detalle_pedido CASCADE CONSTRAINTS;
DROP TABLE pedido CASCADE CONSTRAINTS;
DROP TABLE resenna CASCADE CONSTRAINTS;
DROP TABLE notificacion CASCADE CONSTRAINTS;
DROP TABLE carrito CASCADE CONSTRAINTS;
DROP TABLE stock CASCADE CONSTRAINTS;
DROP TABLE producto CASCADE CONSTRAINTS;
DROP TABLE empleado CASCADE CONSTRAINTS;
DROP TABLE usuario CASCADE CONSTRAINTS;
DROP TABLE pago CASCADE CONSTRAINTS;
DROP TABLE metodo_pago CASCADE CONSTRAINTS;
DROP TABLE tipo_empleado CASCADE CONSTRAINTS;
-----------------------

-- Primero las tablas independientes
CREATE TABLE metodo_pago (
    id_metodo_pago NUMBER(5) PRIMARY KEY,
    tipo VARCHAR2(50) NOT NULL
);

CREATE TABLE tipo_empleado (
    id_tipo_empleado NUMBER(5) PRIMARY KEY,
    descripcion VARCHAR2(100) NOT NULL
);

-- Usuario ahora con rut como id, nombre y apellido separados, tel�fono como number
CREATE TABLE usuario (
    id_usuario VARCHAR2(12) PRIMARY KEY, -- RUT como identificador
    nombre VARCHAR2(50) NOT NULL,
    apellido VARCHAR2(50) NOT NULL,
    correo VARCHAR2(100) NOT NULL,
    contrasenna VARCHAR2(100) NOT NULL,
    direccion VARCHAR2(255) NOT NULL,
    telefono NUMBER(9), -- 9 d�gitos sin +56
    rol VARCHAR2(20) NOT NULL
);

-- Empleado con rut tambi�n
CREATE TABLE empleado (
    id_empleado VARCHAR2(12) PRIMARY KEY, -- RUT como identificador
    fecha_contratacion DATE NOT NULL,
    id_tipo_empleado NUMBER(5),
    FOREIGN KEY (id_tipo_empleado) REFERENCES tipo_empleado(id_tipo_empleado)
);

-- Producto
CREATE TABLE producto (
    id_producto NUMBER(5) PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(255),
    precio NUMBER(10) NOT NULL,
    imagen  VARCHAR2(255),
    disponible CHAR(2) NOT NULL
);
SELECT * FROM producto;
INSERT INTO producto (id_producto, nombre, descripcion, precio, imagen, disponible) VALUES
(6, 'Peluche Hello Kitty', 'Peluche original de Hello Kitty de 25 cm, suave y coleccionable', 12990, 'hello_kitty_peluche.jpg', 'SI');



-- Stock
CREATE TABLE stock (
    id_stock NUMBER(5) PRIMARY KEY,
    cantidad NUMBER(5) NOT NULL,
    ubicacion_detalle VARCHAR2(255) NOT NULL,
    id_producto NUMBER(5),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Carrito
CREATE TABLE carrito (
    id_carrito NUMBER(5) PRIMARY KEY,
    fecha_creacion DATE NOT NULL,
    estado VARCHAR2(20) NOT NULL
);

-- Notificaci�n relacionada al usuario
CREATE TABLE notificacion (
    id_notificacion NUMBER(5) PRIMARY KEY,
    titulo VARCHAR2(100) NOT NULL,
    mensaje VARCHAR2(255) NOT NULL,
    fecha_envio DATE NOT NULL,
    id_usuario VARCHAR2(12),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Rese�a del producto
CREATE TABLE resenna (
    id_resenna NUMBER(5) PRIMARY KEY,
    comentario VARCHAR2(255),
    valoracion NUMBER(2),
    id_usuario VARCHAR2(12),
    id_producto NUMBER(5),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);

-- Pago
CREATE TABLE pago (
    id_pago NUMBER(5) PRIMARY KEY,
    fecha_pago DATE NOT NULL,
    monto_total NUMBER(10,2) NOT NULL,
    estado VARCHAR2(20) NOT NULL,
    id_metodo_pago NUMBER(5),
    FOREIGN KEY (id_metodo_pago) REFERENCES metodo_pago(id_metodo_pago)
);

-- Pedido
CREATE TABLE pedido (
    id_pedido NUMBER(5) PRIMARY KEY,
    fecha_pedido DATE NOT NULL,
    estado VARCHAR2(20) NOT NULL,
    total NUMBER(10,2) NOT NULL,
    id_usuario VARCHAR2(12),
    id_empleado VARCHAR2(12),
    id_pago NUMBER(5),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
    FOREIGN KEY (id_pago) REFERENCES pago(id_pago)
);

-- Detalle de pedido
CREATE TABLE detalle_pedido (
    id_detalle NUMBER(5) PRIMARY KEY,
    cantidad NUMBER(5) NOT NULL,
    productos VARCHAR2(255),
    total NUMBER(10,2) NOT NULL,
    id_pedido NUMBER(5),
    id_producto NUMBER(5),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_producto) REFERENCES producto(id_producto)
);
