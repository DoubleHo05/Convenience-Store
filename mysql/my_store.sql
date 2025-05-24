create database my_store;
use my_store;

create table CATEGORY
(
	CategoryID char(3),
	CategoryName varchar(100),
	primary key (CategoryID)
);

create table PRODUCT
(
	ProductID char(5),
	ProductName varchar(200),
	Category char(3),
	Price decimal(10, 2),
	Stock int,
	primary key (ProductID)
);

create table EMPLOYEE
(
	EmployeeID char(4),
	EmployeeName varchar(255),
	EmployeePhone varchar(15),
	EmployeePosition varchar(30),
	primary key (EmployeeID)
);

create table INVOICE
(
	InvoiceID char(14),
	EmployeeID char(4),
	PurchaseDate datetime,
	Total decimal(15, 2),
	primary key (InvoiceID),
	foreign key (EmployeeID) references EMPLOYEE(EmployeeID)
);

create table INVOICE_DETAIL
(
	InvoiceID char(14),
	Number int not null check(Number > 0),
	ProductID char(5),
	Quantity int check(Quantity > 0),
	SubTotal decimal(15, 2),
	primary key (InvoiceID, Number),
	foreign key (InvoiceID) references INVOICE(InvoiceID),
	foreign key (ProductID) references PRODUCT(ProductID)
);

create table SUPPLIER
(
	SupplierID char(3),
	SupplierName varchar(255),
	SupplierPhone varchar(35),
	SupplierAddress varchar(255),
	primary key (SupplierID)
);

create table IMPORT_ORDER
( 
	ImportOrderID char(14),
	SupplierID char(3),
	ImportDate datetime,
	Total decimal(15, 2),
	primary key (ImportOrderID),
	foreign key (SupplierID) references SUPPLIER(SupplierID)
);

create table IMPORT_ORDER_DETAIL
( 
	ImportOrderID char(14),
	Number int not null check(Number > 0),
	ProductID char(5),
	Quantity int check(Quantity > 0),
	SubTotal decimal(10, 2),
	primary key (ImportOrderID, Number),
	foreign key (ImportOrderID) references IMPORT_ORDER(ImportOrderID),
	foreign key (ProductID) references PRODUCT(ProductID)
)