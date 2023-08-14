create database medicos;

use medicos;

create table medicos(
id int not null primary key auto_increment,
nombre varchar(200),
ap varchar(200),
am varchar(200),
rfc varchar(200),
cedula varchar(200),
correo_electronico varchar(200),
rol varchar(100),
contraseña varchar(100) 
);

select * from medicos;
insert into medicos(nombre,ap,am,rfc,cedula,correo_electronico,rol,contraseña)
values
('Jose Luis','Bernardo','Gutierrez','BEGL1126','12345698','joseluis@gmail.com','General','12345'),
('Graciela','Alvarez','Gonzalez','Graci15','7896422','gracielagon1311@gmail.com','General','12345');

create table expedientes_pacientes(
id int not null primary key auto_increment,
nombre varchar(200),
ap varchar(200),
am varchar(200),
fecha_nacimiento date,
enfermedades varchar(200),
alergias varchar(200),
antecedentes varchar(200),
id_medico int not null,
foreign key (id_medico) references medicos (id) 
);
select * from expedientes_pacientes;

create table citas_exploraciones(
id int not null primary key auto_increment,
fecha date,
peso decimal(10,2),
temperatura decimal(10,2),
altura decimal(10,2),
latidos int,
saturacion int,
edad int,
id_expedientes_pacientes int not null,
foreign key (id_expedientes_pacientes) references expedientes_pacientes(id) 
);
select * from citas_exploraciones;

select TIMESTAMPDIFF(YEAR, fecha_nacimiento, CURDATE()) AS Edad from expedientes_pacientes;

create table diagnosticos(
id int not null primary key auto_increment,
diagnostico varchar (200),
medicamento varchar(200),
indicaciones varchar(150),
soli_estudios varchar (100),
id_citas int not null,
foreign key (id_citas) references citas_exploraciones(id)
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