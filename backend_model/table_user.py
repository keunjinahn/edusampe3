# -*- coding: utf-8 -*-

print ("module [backend_model.table_user.py] loaded")
from backend_model.database import DBManager
db = DBManager.db

from datetime import datetime

class Users(db.Model):
    __tablename__ = 'tb_users'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.String(48))
    user_pw = db.Column('user_pw', db.String(256))
    user_name = db.Column('user_name', db.String(48))
    sub_group_name = db.Column('sub_group_name', db.String(48))
    sub_school_name = db.Column('sub_school_name', db.String(48))
    area_code = db.Column('area_code', db.String(48))
    user_type = db.Column('user_type', db.Integer, default=4)  # 1:관리자, 2:공제사업처, 3:지역본부, 4:사용자, 5:회원(M~), 6:학교(S~)
    user_status = db.Column('user_status', db.Integer, default=1)  # 1:Active, 2:Deactive
    phone = db.Column('phone', db.String(30))
    telephone = db.Column('telephone', db.String(30))
    email = db.Column('email', db.String(48))
    token = db.Column('token', db.String(128))  # added
    last_logon_time = db.Column('last_logon_time', db.DateTime)
    created_date = db.Column('created_date', db.DateTime, default=datetime.now)
    password_date = db.Column('password_date', db.DateTime, default=datetime.now)
    dept_name = db.Column('dept_name', db.String(128))
    fk_school_id = db.Column('fk_school_id', db.Integer)

    def serialize(self):
        resultJSON = {
            # property (a)
            "id": self.id
            , "user_id": self.user_id
            , "user_name": self.user_name
            , "sub_group_name": self.sub_group_name
            , "sub_school_name": self.sub_school_name
            , "area_code": self.area_code
            , "user_type": self.user_type
            , "user_status": self.user_status
            , "phone": self.phone
            , "telephone": self.telephone
            , "email": self.email
            , "token": self.token
            , "last_logon_time": self.last_logon_time
            , "created_date": self.created_date
            , "password_date": self.password_date
            , "dept_name": self.dept_name
            , "fk_school_id": self.fk_school_id
        }
        return resultJSON
