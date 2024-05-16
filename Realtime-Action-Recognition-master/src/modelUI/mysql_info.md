# 資料庫說明

## 教學

- <https://chwang12341.medium.com/mysql-學習筆記-四-mysql中的資料類型-data-type-如何創建tables資料表-如何操作資料表-快速為自己創建一個資料表-927e0c365d6e>
- <https://blog.build-school.com/2022/07/22/資料庫正規化筆記/>
- <https://aws.amazon.com/tw/compare/the-difference-between-graph-and-relational-database/>
- 


## [在 Linux 上安裝 MySQL 或 MariaDB](https://blog.cre0809.com/archives/476/)

### 安裝資料庫

`apt-get -y update && apt-get -y upgrade`
- 安裝 MySQL 
  - `apt-get -y install mysql-server`
- 安裝 MariaDB
  - `apt-get -y install mariadb-server`

### 進行安全設定
- MySQL
  - `mysql_secure_installation`
- MariaDB
  - `mysql_secure_installation`
    
```
NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
    SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user.  If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none): 
```
- 由於目前 root 並沒有設定任何密碼，這步我們直接按 Enter 即可。

```
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] Y
```
- 這裡詢問我們是否需要為 root 設定密碼，我這裡選擇 Y。

```
By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] Y
```
- 是否刪除匿名用戶，輸入 Y。

```
Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] Y
```
- 是否關閉 root 遠程登入，輸入 Y。

```
By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] Y
```
- 是否移除測試資料庫，選擇 Y。

```
Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] Y
```
- 現在重新載入權限讓剛剛的設置保存嗎，選擇 Y。

### 建立資料庫

- 進入資料庫
  - `mysql -u root -p`
- 建立資料庫
  - `CREATE DATABASE testdb;`

### 新增使用者並授予權限

- 進入資料庫
  - `mysql -u root -p`
- 新增使用者
  - `CREATE USER user@localhost IDENTIFIED BY '123456';`
- 授予使用者權限
  - `GRANT ALL PRIVILEGES ON testdb.* TO user@localhost;`
  - `GRANT ALL PRIVILEGES ON *.* TO user@localhost;`
- 保存設定並離開
  - `FLUSH PRIVILEGES;`
  - `exit`

## 資料庫伺服器設定

### 資料格式

### 使用者

- 使用者：root
  - 密碼：NCUCSIE

### 資料庫

- test
  - 使用者：root
    - 密碼：NCUCSIE
    - 權限：ALL PRIVILEGES
- Taekwondo

### 資料庫安全設定

```
(tfpose-env) root@cfb89bdbefe0:/home/UI# mysql_secure_installation

Securing the MySQL server deployment.

Connecting to MySQL using a blank password.

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No: n

Skipping password set for root as authentication with auth_socket is used by default.
If you would like to use password authentication instead, this can be done with the "ALTER_USER" command.
See https://dev.mysql.com/doc/refman/8.0/en/alter-user.html#alter-user-password-management for more information.

By default, a MySQL installation has an anonymous user,
allowing anyone to log into MySQL without having to have
a user account created for them. This is intended only for
testing, and to make the installation go a bit smoother.
You should remove them before moving into a production
environment.

Remove anonymous users? (Press y|Y for Yes, any other key for No) : y
Success.


Normally, root should only be allowed to connect from
'localhost'. This ensures that someone cannot guess at
the root password from the network.

Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
Success.

By default, MySQL comes with a database named 'test' that
anyone can access. This is also intended only for testing,
and should be removed before moving into a production
environment.


Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y
 - Dropping test database...
Success.

 - Removing privileges on test database...
Success.

Reloading the privilege tables will ensure that all changes
made so far will take effect immediately.

Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y
Success.

All done! 
```

