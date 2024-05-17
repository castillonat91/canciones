CREATE DATABASE agenda;
use agenda;
CREATE TABLE personas(
  id_persona int auto_increment primary key,
  nombre_persona varchar(60),
  apellido_persona varchar(60),
  email varchar(60),
  direccion varchar(60),
  telefono int,
  user_persona varchar(60),
  contrasena varchar(255)
);

alter table personas add roles varchar(50);

CREATE TABLE canciones(
	  id_can int auto_increment primary key,
    titulo varchar(60) not null,
    artista varchar(60) not null,
    genero varchar(60) not null,
    precio decimal(10,0) not null,
    duracion varchar(20) not null,
    lanzamiento date not null,
    img blob
);

CREATE TABLE compras(
	id_compra int auto_increment primary key,
    fechaCompra date not null,
    precio decimal(10,0) not null,
    Mpago varchar(50) not null,
    id_can int not null,
    id_persona int not null,
    foreign key(id_can) references canciones(id_can),
    foreign key(id_persona) references personas(id_persona)
);
describe canciones;
describe personas;
select * from personas;
select * from canciones;
select * from compras;