create database medicos;

use medicos;

create table medicos(
id int not null primary key auto_increment,
nombre varchar(200),
ap varchar(200),
am varchar(200),
rfc varchar(200),
correo_electronico varchar(200),
rol varchar(100),
contraseña varchar(100) 
);
select * from medicos;

insert into medicos(nombre,ap,am,rfc,correo_electronico,rol,contraseña)
values
('Jose Luis','Bernardo','Gutierrez','BEGL1126','joseluis@gmail.com','General','12345');


create table expedientes_pacientes(
id int not null primary key auto_increment,
nombre varchar(200),
ap varchar(200),
am varchar(200),
fecha_nacimiento date,
enfermedades varchar(200),
id_medico int not null,
foreign key (id_medico) references medicos (id) 
);
select * from expedientes_pacientes;

create table citas_exploraciones(
id int not null primary key auto_increment,
fecha date,
peso decimal(10,2),
altura decimal(10,2),
temperatura decimal(10,2),
latidos int,
saturacion int
);
select * from citas_exploraciones;

create table diagnosticos(
id int not null primary key auto_increment,
sintomas varchar (200),
dx varchar(200),
tratamiento varchar(150),
soli_estudios varchar (100)
);

create table recetas(
id int not null primary key auto_increment,
id_cita_exploracion int not null,
id_diagnostico int not null,
foreign key (id_cita_exploracion) references citas_exploraciones (id) on delete cascade on update cascade,
foreign key (id_diagnostico) references diagnosticos (id) on delete cascade on update cascade
);

create table drExploraciones (
id int not null primary key auto_increment,
id_medico int not null,
id_cita_exploracion int not null,
foreign key (id_medico) references medicos (id) on delete cascade on update cascade,
foreign key (id_cita_exploracion) references citas_exploraciones (id) on delete cascade on update cascade
);

