create database my_store;
use my_store;

create table PRODUCT
(
	ProductID varchar(10),
	ProductName varchar(255),
	Category varchar(100),
	Price decimal(10, 2),
	Stock int,
	primary key (ProductID)
);

create table CUSTOMER
(
	CustomerID varchar(10),
	CustomerName varchar(255),
	CustomerPhone varchar(15),
	primary key (CustomerID)
);

create table EMPLOYEE
(
	EmployeeID varchar(10),
	EmployeeName varchar(255),
	EmployeePhone varchar(15),
	EmployeePosition varchar(100),
	primary key (EmployeeID)
);

create table INVOICE
(
	InvoiceID varchar(10),
	CustomerID varchar(10),
	EmployeeID varchar(10),
	PurchaseDate datetime,
	TotalCost decimal(15, 2),
	primary key (InvoiceID),
	foreign key (CustomerID) references CUSTOMER(CustomerID),
	foreign key (EmployeeID) references EMPLOYEE(EmployeeID)
);

create table INVOICE_DETAIL
(
	InvoiceID varchar(10),
	Ordinal int not null,
	ProductID varchar(10),
	Quantity int check(Quantity > 0),
	Cost decimal(15, 2),
	primary key (InvoiceID, Ordinal),
	foreign key (InvoiceID) references INVOICE(InvoiceID),
	foreign key (ProductID) references PRODUCT(ProductID)
);

create table SUPPLIER
(
	SupplierID varchar(10),
	SupplierName varchar(255),
	SupplierPhone varchar(15),
	SupplierAddress varchar(255),
	primary key (SupplierID)
);

create table IMPORT_ORDER
( 
	ImportOrderID varchar(10),
	SupplierID varchar(10),
	ImportDate datetime,
	TotalCost decimal(15, 2),
	primary key (ImportOrderID),
	foreign key (SupplierID) references SUPPLIER(SupplierID)
);

create table IMPORT_ORDER_DETAIL
( 
	ImportOrderID varchar(10),
	Ordinal int not null,
	ProductID varchar(10),
	Quantity int,
	CostPerUnit decimal(10, 2),
	primary key (ImportOrderID, Ordinal),
	foreign key (ImportOrderID) references IMPORT_ORDER(ImportOrderID),
	foreign key (ProductID) references PRODUCT(ProductID)
)


