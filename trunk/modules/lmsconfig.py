from ConfigParser import ConfigParser
import os

class LmsCfg:
	def __init__(self, path):
		config = ConfigParser()
		config.read(os.path.join(path, 'lms.cfg'))
		self.dbpath = config.get('lmssettings', 'dbpath')
		self.aws_enable = config.getboolean('lmssettings', 'amazonlookup')
		if self.aws_enable:
			self.aws_id = config.get('lmssettings', 'awsid')
			self.aws_key = config.get('lmssettings', 'awskey')
		else:
			self.aws_id = ''
			self.aws_key = ''
			
def getcfg(path):
	cfg = LmsCfg(path)
	return cfg	