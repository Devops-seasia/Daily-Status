from azure.storage.blob import BlobServiceClient
storage_account_key = "gG47EhHIPr+e2xaLTYxSWiwifIj1/tgTTQJPq+8bVB27o1VyCVN2vzWGnY4yXzM6wH8D6fVZjcza+ASt9wFzag=="
storage_account_name = "myblobstorageaccount123"
connection_string = "DefaultEndpointsProtocol=https;AccountName=myblobstorageaccount123;AccountKey=0j9SfznXw6hMlmbswkt/p8Uii/iccW2XOiXJy51BGh3j9zLS53xFUafa+JT0uTRG5pvGQWt5zR2c+AStcreldw==;EndpointSuffix=core.windows.net"
container_name = "myfiles"

def uploadToBlobStorage(file_path,file_name):
   blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
   with open(file_path,'rb') as data:
      blob_client.upload_blob(data)
      print(f'Uploaded {file_name}.')
# calling a function to perform upload
uploadToBlobStorage('/home/kali/Upload-file-to-blob/shubham.txt','shubham.txt')