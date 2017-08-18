import opencv.saveFrame as save
import opencv.detect as detect
import sys
import os

def UsageError():
	print("UsageError:")
	print("Use \"python main.py saveframe foldername\" to Save Frame")
	print("Use \"python main.py detectface foldername\" to Detect Character Fase")
	print("Use \"python main.py manclassify foldername\" to Classify Training Data")

def PathError(foldername):
	print("No Such A Directory.")
	while True:
		ans = input("Create A New Directory Names \"%s\"? (Y/N) " % foldername)
		if ans in ["Y", "y"]:
			return True
		elif ans in ["N", "n"]:
			return False
		else:
			print("Please Enter Y or N Only.")

if __name__ == "__main__":

	cur_path = os.getcwd()

	if len(sys.argv) == 3:
		target_path = os.path.join(cur_path, "video\%s" % sys.argv[2])
 
		if '\\' in sys.argv[2]:
			print("Invalid Foldername.")
		else:
			if not os.path.exists(target_path):
				# To ask user whether to create a new directory or not
				wants_create = PathError(sys.argv[2])
				if wants_create:
					os.makedirs(target_path, exist_ok=True)
				else:
					print("Stop Processing.")


			if os.path.exists(target_path):
				os.makedirs(os.path.join(target_path, "video"), exist_ok=True)
				os.makedirs(os.path.join(target_path, "frame"), exist_ok=True)
				os.makedirs(os.path.join(target_path, "crop"), exist_ok=True)
				if sys.argv[1] == "saveframe":
					print("Starting to Save Frame...")
					save.saveFrame(target_path = target_path, interval = 24)
				elif sys.argv[1] == "detectface":
					print("Starting to Detect Face...")
					save.detect()
				elif sys.argv[1] == "manclassify":
					print("Starting to Man-classify...")

				else:
					UsageError()
	else:
		UsageError()