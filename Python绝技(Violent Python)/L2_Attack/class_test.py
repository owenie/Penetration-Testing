# -*- coding: utf-8 -*-
import time

class Player():
	
	def __init__(self,ll,mj,zl,kind,level=0):
		#self.name = name   #玩家名字
		self.power = ll    	#力量
		self.agility = mj  	#敏捷
		self.wit = zl      	#智力
		self.kind = kind   	#类型
		self.level = level 	#等级
		
	def calculate(self):     #定义计算玩家属性值方法
		self.redbaseValue = 100 + self.power * 5
		self.bluebaseValue = 50 + self.wit * 5
		self.armor = 5 + self.agility * 3
		return (self.power,self.agility,\
			   self.wit,self.kind,self.level,\
			   self.redbaseValue,self.bluebaseValue,self.armor)

	def attack(self):
		if self.kind == 1: #力量

			self.attack = 10 + self.power

		if self.kind == 2: #敏捷

			self.attack = 7 + self.agility

		if self.kind == 3: #智力

			self.attack = 5 + self.wit
		return self.attack

	def update(self,ud=1):    #定义玩家升级方法
		self.level += ud
		self.power += 2 * ud
		self.agility +=	 2 * ud
		self.wit += 2 * ud
		return (self.level,self.power,self.agility,self.wit)

	def hurt(self,ss=1):      #定义玩家伤害方法
		self.redbaseValue = self.redbaseValue - ((self.armor * 0.06)/(1 + self.armor * 0.06) * ss)
		return self.redbaseValue

	def status(self):         #定义查看玩家状态方法
		return (self.redbaseValue,self.bluebaseValue,self.armor,self.attack())
print('正在实例化玩家...')
lilei = Player(3,1,1,1)   #实例化玩家
time.sleep(1)
print('正在计算玩家属性...')
print ('力量：{}'.format(lilei.calculate()[0])) #计算玩家属性值
print ('敏捷：{}'.format(lilei.calculate()[1]))
print ('智力：{}'.format(lilei.calculate()[2]))
print ('类型：{}'.format(lilei.calculate()[3]))
print ('等级：{}'.format(lilei.calculate()[4]))
print ('血量：{}'.format(lilei.calculate()[5]))
print ('蓝量：{}'.format(lilei.calculate()[6]))
print ('护甲：{}'.format(lilei.calculate()[7]))
time.sleep(1)
print('玩家升级...')
#print (lilei.update(3))   #玩家升级方法
print ('等级：{}'.format(lilei.update(3)[0])) #计算玩家属性值
print ('力量：{}'.format(lilei.update(3)[1]))
print ('敏捷：{}'.format(lilei.update(3)[2]))
print ('智力：{}'.format(lilei.update(3)[3]))
time.sleep(1)
print('查看玩家状态')
print (lilei.status())    #查看玩家状态
time.sleep(1)
print('玩家伤害值')
print (lilei.hurt(100))   #查看玩家伤害