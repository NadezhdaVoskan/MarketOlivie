set ansi_nulls on
go
set ansi_padding on
go
set quoted_identifier on
go

create database Olivie_Dvorik
go

use Olivie_Dvorik
go

create table [dbo].[Roles]
(
  [ID_Role] [int] not null identity(1,1),
  [Role_Name] [varchar] (50) not null,
  constraint [PK_Role] primary key
  clustered ([ID_Role] ASC) on [PRIMARY],
  constraint [UQ_Role_Name] unique
  ([Role_Name])
)
go

insert into [Roles] ([Role_Name]) values
('Админ'),('Покупатель')
go

create table [Loyality]
(
	[ID_Loyality] [int] not null identity(1,1) primary key,
	[Name_Loyality] [VARCHAR] (50) not null unique,
	[Discount] [float] not null
)
go

insert into [Loyality] ([Name_Loyality], [Discount]) values
('None', 0),
('Bronze', 0.15),
('Silver', 0.25),
('Gold', 0.35)
go

create table [User]
(
	[ID_User] [int] not null identity(1,1) primary key,
	[Role_ID] [int] not null references [Roles] (ID_Role) on delete cascade,
	[Loyality_ID] [int] not null references [Loyality] (ID_Loyality) on delete cascade,
	[Phone_User] [VARCHAR](15) not null unique check ([Phone_User] like ('+[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')),
	[Password_User] [VARCHAR](50) not null,
	[Balance_User] [int] not null default(10000)
)
go

insert into [User] ([Role_ID], [Loyality_ID], [Phone_User], [Password_User], [Balance_User]) 
values (1, 1, '+79893241189', 'admin', 10000), (2, 1, '+79835093364', 'user', 10000)
go

select * from [User]
go


create table [Type_Ingridient]
(
	[ID_Type] [int] not null identity(1,1) primary key,
	[Name_Type] [VARCHAR] (50) not null unique
)
go

insert into Type_Ingridient (Name_Type)
values ('Картофель'),
('Морковь'),
('Яйцо'),
('Колбаса'),
('Огурцы'),
('Горошек'),
('Майонез')


create table [Ingridient]
(
	[ID_Ingridient] [int] not null identity(1,1) primary key,
	[Type_ID] [int] not null references [Type_Ingridient] (ID_Type) on delete cascade,
	[Name_Ingridient] [VARCHAR](50) not null unique,
	[Cost_Ingridient] [int] not null,
	[Count_Ingridient] [int] not null default(100)
)
go


insert into [Ingridient] (Type_ID, Name_Ingridient, Cost_Ingridient, Count_Ingridient)
values (1, 'Романо', 15, 100),
(1, '"Импала"', 20, 100),
(1, '"Луговской"', 22, 100),
(2, '"Лагуна"', 15, 100),
(2, '"Болеро"', 20, 100),
(3, 'Куринные', 30, 100),
(3, 'Перепелиные', 20, 100),
(4, '"Докторская"', 210, 100),
(4, '"Клинская "Молочная""', 234, 100),
(5, 'Соленые', 15, 100),
(5, 'Малосоленые', 14, 100),
(5, 'Маринованные', 30, 100),
(5, 'Свежие', 9, 100),
(6, 'Консервированный', 160, 100),
(6, 'Отваренный свежий', 130, 100),
(7, '"Ряба"', 84, 100),
(7, '"Моя семья"', 120, 100)
go


create table [Olivie_Buy]
(
	[ID_Olivie_Ingridient] [int] not null identity(1,1) primary key,
	[Structure_Olivie] [varchar](max) not null,
	[User_ID] [int] not null references [User] (ID_User) on delete cascade,
	[Count_Olivie] [int] not null,
	[Cost_Olivie] [int] not null,
	[Sum_Order] [int] not null,
	[Time_Order] [datetime] not null,
	[Foreign_Object] [bit]
)
go

UPDATE [Ingridient] SET [Count_Ingridient] = 101 WHERE [Name_Ingridient] = 'Консервированный'
go