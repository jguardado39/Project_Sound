# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings

""" Class for Command """

class Command(BaseCommand):
	def handle(self, *args, **options):
		print "----------------------------------------------"
		print "------    Welcome to the sound setup    ------"
		print "----------------------------------------------"
		print ""

		print "Page administrator"
		print "----------------------------------------------"
		print ""

		""" Inputs for admin"""

		admin_user = raw_input("\tName: ")
		admin_email = raw_input("\tEmail: ")
		print ""

		# get authenication method
		authenication = self.setAuthentication()
		while not authenication:
			authenication = self.setAuthentication()

		self.setup(admin_user, admin_email, authenication)

	""" Authentication method """

	def setAuthentication(self):
		print "Please select your authenication method"
		print "----------------------------------------------"
		print "Available providers: Facebook, Twitter, Github"
		print ""

		print "Facebook"
		print "\tFacebook authentication requires a Facebook app setup on "\
			"http://developers.facebook.com/setup/"
		facebook = self.readAppData("Facebook")
		print ""

		print "Twitter"
		print "\tTwitter authentication requires setup of a Twitter app on "\
			"https://dev.twitter.com/apps/new"
		twitter = self.readAppData("Twitter")
		print ""

		print "Github"
		print "\tGithub authentication requires setup of a Github app on "\
			"https://github.com/settings/applications/new"
		github = self.readAppData("Github")
		print ""

		""" Verification of Authentication """

		if facebook is None and twitter is None and github is None:
			print "If you can be sassy, I shall be sassy with you."
			print "I will not let you go without selecting at least one of them."
			print ""
			return False

		return {"facebook": facebook, "twitter": twitter, "github": github}

	def readAppData(self, name):
		type = raw_input(
			"\tUse " + name + " for authentication? [Y/N] "
			),strip().upper()
		while type != "N" and type != "Y":
			type = raw_input(
				"\tInvalid answer, please enter 'Y' for yes or 'N' for no: "
				).strip()lower()

		if type == "Y":
			id = ""
			while id.strip() == "":
				id = raw_input("\t" + name + "app id: ")
				if id.strip() == "":
					print "\t\tInvalid app id"
			secret = ""
			while secret.strip() == "":
				secret = raw_input("\t" + name + " app secret: ")
				if secret.strip() == "":
					print "\t\tInvalid app id"
			return {"id": id, "secret": secret}
		return None

		""" Starting of the setup"""

	def setup(self, admin_user, admin_email, authentication):
		setup = open(setting.BASE_DIR + "/settings_local.example.py").read()
		setup = setup.replace("[admin_user]", admin_user)
		setup = setup.replace("[admin_email]", admin_email)

		auth_backends = []
		auth_backend_enabled = []

		if authentication["facebook"] is not None:
			auth_backends.append(
				"\"social_auth.backends.facebook.FacebookBackend\","
			)
			auth_backends_enabled.append("\"facebook\",")

		if authentication["twitter"] is not None:
			auth_backends.append(
				"\"social_auth.backends.twitter.TwitterBackend\","
			)
			auth_backends_enabled.append("\"twitter\",")

		if authentication["github"] is not None:
			auth_backends.append(
				"\"social_auth.backends.contrib.github.GithubBackend\","
			)
			auth_backends_enabled.append("\"github\",")


		setup = setup.replace(
			"[auth_backends]"
			"\n    ".join(auth_backends)
		)
		setup = setup.replace(
			"[auth_backends_enabled]",
			" ".join(auth_backends_enabled)
		)

		auth_data = ""
		for key,value in authentication.items():
			if value is None:
				continue

			if key == 'twitter':
				auth_data += "TWITTER_CONSUMER_KEY = \"" + \
					value["id"] + "\"\n"
				auth_data += "TWITTER_CONSUMER_SECRET = \"" + \
					value["secret"] + "\"\n"
			else:
				auth_data += key.upper() + "_APP_ID = \"" + \
					value["id"] + "\"\n"
				auth_data += key.upper() + "_API_SECRET = \"" + \
					value["secret"] + "\"\n"
			auth_data += "\n"

		setup = setup.replace("[auth_data]", auth_data)

		f = open(settings.SOUND_STORAGE_PATH + "/settings_local.py", "w+")
		f.write(setup)
		f.close()

		print "Setup finished"
		print "----------------------------------------------"