import os

from flappy_bird import FlappyBird

if __name__ == "__main__":
	try:
		application = FlappyBird()
		if application.run():
			print("Program exited successfully")
		else:
			print("The progrem exiteed unsuccessfully")
	except Exception as e:
		print(e)
		input("Press enter to exit...")
