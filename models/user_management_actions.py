from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from .base import Base


class UserManagementActions(Base):
  __tablename__ = 'UserManagementActions'
  actionID = Column(Integer, primary_key=True, autoincrement=True)
  adminID = Column(Integer)
  userID = Column(Integer)  # sharding criteria
  actionType = Column(Enum('Ban', 'Warn', 'Suspend', 'Reactivate'))
  actionTimestamp = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')
  reason = Column(String(500))
  actionStatus = Column(Enum('Pending', 'Completed', 'Canceled'))
  actionMessage = Column(String(500))

  @property
  def admin(self):
    return self.adminID

  @admin.setter
  def admin(self, adminID):
    self.adminID = adminID

  @property
  def user(self):
    return self.userID

  @user.setter
  def user(self, userID):
    self.userID = userID
