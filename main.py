from drive.auth import authenticate
from drive.folders import get_daily_folder, create_batch
from drive.upload import upload_file

def main():
    service = authenticate()
    working_folder = get_daily_folder(service)    
    batch_id = create_batch(service, working_folder)
    upload_file(service, batch_id)	

if __name__ == "__main__":
    main()
