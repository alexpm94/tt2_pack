import csv
import os
import rospkg 

rospack = rospkg.RosPack()

class Usuario:

	def __init__(self,name):
		self.name=name
		self.users_csv=rospack.get_path('tt2_pack')+'/src/include/users.csv'+str(self.id_num)
		self.get_id()
		self.append_toCSV()
		self.create_dir()

	def get_id(self):
		try: 
			with open(self.users_csv, "rb") as f:
				reader = csv.reader(f)
				for last in reader: pass      # Loop through the whole file reading it all.
				line=last
				self.id_num=int(line[-1])+1
				return self.id_num
		except IOError:
			with open(self.users_csv, 'a') as csvfile:
				fieldnames = ['first_name', 'id_number']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				writer.writeheader()
				self.id_num=0
				return self.id_num

	def append_toCSV(self):
		with open(self.users_csv, 'a') as csvfile:
			fieldnames = ['first_name', 'id_number']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writerow({'first_name': self.name, 'id_number': self.id_num})

	def create_dir(self):
		self.directory=rospack.get_path('tt2_pack')+'/src/dataBase/s'+str(self.id_num)
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

	def getDirectory(self):
		return self.directory
