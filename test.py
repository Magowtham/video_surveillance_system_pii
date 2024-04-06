import requests

# Replace 'YOUR_ACCESS_TOKEN' with your Google Drive access token
access_token = 'ya29.a0Ad52N38UEwYdWbP_CjZGJqofO-vhzZHGzIxjVnlH3k3J-7OrKbFYXcK7x-OsyYxZL-s-Dnr70Tk5zkLWV2Sp7x5axre-Fe1Es_ik3JdfcmENeJBoyvI4fzE6-m42zjFV4rY-KjRttIa6SwnV-BG394EhOkYyCZU0qB2ZaCgYKAZwSARASFQHGX2MiAchg84N5x4CE7dKFR4YC5Q0171'

# Replace 'FOLDER_ID' with the ID of the folder where you want to upload the video
# folder_id = 'FOLDER_ID'

# Replace 'video.mp4' with the name of your video file
video_file_path = './temp/short.avi'

# Google Drive API endpoint for uploading files
upload_url = f'https://www.googleapis.com/upload/drive/v3/files?uploadType=media&supportsAllDrives=true'

# Headers with Authorization token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'video/mp4',  # Adjust content type if your video format is different
}

# Read the video file content
with open(video_file_path, 'rb') as f:
    video_content = f.read()

# Send POST request to upload the video
response = requests.post(upload_url, headers=headers, data=video_content)

# Check if upload was successful
if response.status_code == 200:
    print('Video uploaded successfully to Google Drive.')
else:
    print('Failed to upload video to Google Drive. Status code:', response.status_code)
    print('Response:', response.text)
