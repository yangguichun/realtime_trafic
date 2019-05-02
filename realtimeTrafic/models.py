from realtimeTrafic import app, db
from flask_login import UserMixin



# 表示一条路径
class DrivePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # 源地址的经纬度
    origin = db.Column(db.Text)
    # 目标地址的经纬度
    dest = db.Column(db.Text)
    def to_json(self):
        dict = self.__dict__
        return dict


class RealTimePath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pathId = db.Column(db.Integer)
    queryTime = db.Column(db.DateTime)   
    # 距离，米 
    distance = db.Column(db.Float)
    # 耗时，秒
    duration = db.Column(db.Float)
    def to_json(self):
        dict = self.__dict__
        return dict


# # 充电站所有者，比如南方和顺，星星充电，粤易充
# class ApiType(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     def to_json(self):
#         dict = self.__dict__
#         # if "_sa_instance_state" in dict:
#         #     del dict["_sa_instance_state"]
#         return dict


# # 充电站
# class ChargeStation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     region = db.Column(db.Text)
#     stationName = db.Column(db.Text)
#     gunTotalCount = db.Column(db.Integer)
#     stationNo = db.Column(db.Integer)
#     stationCode = db.Column(db.Text)
#     apiId = db.Column(db.Integer)

#     def to_json(self):
#         dict = self.__dict__
#         # if "_sa_instance_state" in dict:
#         #     del dict["_sa_instance_state"]
#         return dict

    
# # 充电站状态
# class ChargeStationStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     stationId = db.Column(db.Integer)
#     queryTime = db.Column(db.DateTime)
#     usedGunCount = db.Column(db.Integer)
#     freeGunCount = db.Column(db.Integer)
#     fixedGunCount = db.Column(db.Integer)

#     def to_json(self):
#         dict = self.__dict__
#         # if "_sa_instance_state" in dict:
#         #     del dict["_sa_instance_state"]
#         return dict
    
# # 枪的状态
# class GunStatus(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     stationId = db.Column(db.Integer)
#     queryTime = db.Column(db.DateTime)
#     gunName = db.Column(db.Text)
#     power = db.Column(db.Integer)
#     status = db.Column(db.Integer)
#     def to_json(self):
#         dict = self.__dict__
#         # if "_sa_instance_state" in dict:
#         #     del dict["_sa_instance_state"]
#         return dict


user_role = db.Table(
        'user_role', 
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id')) 
    )

# 用户
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    password = db.Column(db.Text)
    lastLogintime = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=user_role, back_populates='users')

    def to_json(self):
        dict = self.__dict__
        # if "_sa_instance_state" in dict:
        #     del dict["_sa_instance_state"]
        return dict


role_authority = db.Table(
        'role_authority', 
        db.Column('role_id', db.Integer, db.ForeignKey('role.id')), 
        db.Column('auth_id', db.Integer, db.ForeignKey('authority.id'))
    )

# 角色
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    authorities = db.relationship('Authority', secondary=role_authority, back_populates='roles')
    users = db.relationship('User', secondary=user_role, back_populates='roles')
    def to_json(self):
        dict = self.__dict__
        return dict


# 权限
class Authority(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    roles = db.relationship('Role', secondary=role_authority, back_populates='authorities')
    def to_json(self):
        dict = self.__dict__
        return dict