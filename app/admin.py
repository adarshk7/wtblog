class User():
	id = 7834
	password = "14MzaosumaDmIn"

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)