import argparse
from drive.auth import authenticate
from drive.folders import get_daily_folder, create_batch
from drive.upload import upload_file

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("files", nargs="+")
	args = parser.parse_args()
	
	service = authenticate()
	working_folder = get_daily_folder(service)
	batch_id = create_batch(service, working_folder)
	upload_file(service, batch_id, args.files)	

if __name__ == "__main__":
    main()
