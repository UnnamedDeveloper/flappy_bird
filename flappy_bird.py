from flappy_bird import FlappyBird

if __name__ == "__main__":
	application = FlappyBird()
	if application.run():
		print("Program exited successfully")
	else:
		print("The progrem exiteed unsuccessfully")
