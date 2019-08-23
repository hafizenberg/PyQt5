from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import datetime

import pymysql as Mysqldb

from PyQt5.uic import loadUiType

ui,_ = loadUiType('library.ui')
login,_ = loadUiType('login.ui')

class Login(QWidget , login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
    def Handel_Login(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        self.cur.execute('''SELECT * FROM user''')
        data = self.cur.fetchall()
        for row in data :
            if username == row[1] and password == row[3]:
                self.window2 = MainApp()
                self.close()
                self.window2.show()
            else:
                self.label_3.setText('try again')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_changes()
        self.Handle_Buttons()
        self.Show_Category()
        self.Show_Author()
        self.Show_Publisher()
        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()
        self.Show_All_Operation()
        self.Add_New_User()
        self.Login()
        self.Edit_User()



    def Handle_UI_changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)

        self.pushButton_2.clicked.connect(self.Open_Day_to_Day_Tab)
        self.pushButton_3.clicked.connect(self.Open_Books_Tab)
        self.pushButton_5.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_7.clicked.connect(self.Add_New_Book)
        self.pushButton_8.clicked.connect(self.Search_Books)
        self.pushButton_10.clicked.connect(self.Edit_Books)
        self.pushButton_11.clicked.connect(self.Delete_Books)

        self.pushButton_9.clicked.connect(self.Add_New_User)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_13.clicked.connect(self.Edit_User)


        self.pushButton_16.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_14.clicked.connect(self.Add_Publisher)

        self.pushButton_6.clicked.connect(self.Handle_Day_Operations)

    def Show_Themes(self):
        self.groupBox_3.show()

    def Hiding_Themes(self):
        self.groupBox_3.hide()


    def Open_Day_to_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Add_New_Book(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_6.text()
        book_desc = self.textEdit.toPlainText()
        book_code = self.lineEdit_7.text()
        book_category = self.comboBox_3.currentIndex()
        book_author = self.comboBox_4.currentIndex()
        book_publisher = self.comboBox_8.currentIndex()
        book_price = self.lineEdit_8.text()

        self.cur.execute('''
        INSERT INTO book(book_name,book_desc,book_code,book_category,book_author,book_publisher,book_price) VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''',(book_name,book_desc,book_code,book_category,book_author,book_publisher,book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book added')
        self.lineEdit_6.clear()
        self.textEdit.clear()
        self.lineEdit_7.clear()
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.lineEdit_8.clear()


    def Search_Books(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_9.text()
        self.cur.execute('''SELECT * FROM book WHERE book_name = %s''',(book_name,))
        data = self.cur.fetchone()
        self.lineEdit_9.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_4.setText(data[3])
        self.comboBox_3.setCurrentIndex(data[4])
        self.comboBox_4.setCurrentIndex(data[5])
        self.comboBox_8.setCurrentIndex(data[6])
        self.lineEdit_5.setText(str(data[7]))

    def Edit_Books(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        book_name = self.lineEdit_3.text()
        book_desc = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_4.text()
        book_category = self.comboBox_5.currentIndex()
        book_author = self.comboBox_6.currentIndex()
        book_publisher = self.comboBox_7.currentIndex()
        book_price = self.lineEdit_5.text()

        search_book_name = self.lineEdit_9.text()

        self.cur.execute('''
        UPDATE book SET book_name=%s,book_desc=%s,book_code=%s,book_category=%s,book_author=%s,book_publisher=%s,book_price=%s
        ''',(book_name,book_desc,book_code,book_category,book_author,book_publisher,book_price))

        self.db.commit()
        self.statusBar().showMessage('Book updated')
    def Delete_Books(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()
        book_name = self.lineEdit_9.text()
        warning = QMessageBox.warning(self,'delete book','are you sure?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = '''DELETE FROM book WHERE book_name=%s'''
            self.cur.execute(sql , [(book_name)])
            self.db.commit()
            self.statusBar().showMessage('deleted')

    def Add_New_User(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()


        username = self.lineEdit_2.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password2 = self.lineEdit_12.text()
        if password == password2:
            self.cur.execute('''INSERT INTO user(user_name, user_email, user_password) VALUES(%s,%s,%s)''',(username,email,password))
            self.db.commit()
            self.statusBar().showMessage('New user added')
        else:
            self.label_31.text('Please add a valid password twice')

    def Login(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_13.text()
        password = self.lineEdit_14.text()
        sql = '''SELECT * FROM user'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                self.statusBar().showMessage('Valid')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_19.setText(row[1])
                self.lineEdit_20.setText(row[2])
                self.lineEdit_18.setText(row[3])

    def Edit_User(self):
        username = self.lineEdit_19.text()
        email = self.lineEdit_20.text()
        password = self.lineEdit_18.text()
        password2 = self.lineEdit_17.text()

        if password == password2:
            self.cur.execute('''UPDATE user SET user_name=%s, user_email=%s,user_password=%s WHERE user_name=%s''',(username,email,password,username))
            self.db.commit()
            self.statusBar().showMessage('')
        else:
            self.label_32.text('Try again')

    def Show_Category(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        if data :
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_4.setItem(row,column,QTableWidgetItem(str(item)))
                    column +=1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    def Add_Category(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_21.text()

        self.cur.execute('''
        INSERT INTO category(category_name) VALUES (%s)
        ''',(category_name,))
        self.db.commit()
        self.statusBar().showMessage('New category added')
        self.lineEdit_21.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()

    def Show_Author(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM author''')
        data = self.cur.fetchall()
        if data :
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
                    column +=1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)


    def Add_Author(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()
        author_name = self.lineEdit_16.text()

        self.cur.execute('''
        INSERT INTO author(author_name) VALUES (%s)
        ''',(author_name,))
        self.db.commit()
        self.statusBar().showMessage('New author added')
        self.lineEdit_16.setText('')
        self.Show_Author()
        self.Show_Author_Combobox()

    def Show_Publisher(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        if data :
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row , form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(item)))
                    column +=1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def Add_Publisher(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()
        publisher_name = self.lineEdit_15.text()

        self.cur.execute('''
        INSERT INTO publisher(publisher_name) VALUES (%s)
        ''',(publisher_name,))
        self.db.commit()
        self.statusBar().showMessage('New publisher added')
        self.lineEdit_15.setText('')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()

    def Show_Category_Combobox(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_5.addItem(category[0])

    def Show_Author_Combobox(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM author''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_6.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        self.comboBox_8.clear()
        for publisher in data:
            self.comboBox_8.addItem(publisher[0])
            self.comboBox_7.addItem(publisher[0])


    def Handle_Day_Operations(self):
        book_name = self.lineEdit.text()
        client_name = self.lineEdit_22.text()
        type = self.comboBox.currentIndex()
        days_number = self.comboBox_2.currentIndex() +1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days=days_number)

        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''INSERT INTO dayoperation(book_name,client_name,type,days_number,today_date,to_date) VALUES(%s,%s,%s,%s,%s,%s)''',(book_name,client_name,type,days_number,today_date,to_date))

        self.db.commit()
        self.statusBar().showMessage("new entry")
        self.Show_All_Operation()

    def Show_All_Operation(self):
        self.db = Mysqldb.connect(host='localhost' , user='root',password='hafiz',db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT * FROM dayoperation''')
        data = self.cur.fetchall()
        self.tableWidget.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                    self.tableWidget.setItem(row,column,QTableWidgetItem(str(item)))
                    column +=1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
