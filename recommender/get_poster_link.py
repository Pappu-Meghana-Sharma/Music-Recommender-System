import requests
import base64
import time
import os
from dotenv import load_dotenv
load_dotenv()
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
class SpotifyAuthorization:
    def __init__(self,client_id,client_secret):
        self.client_id=client_id
        self.client_secret=client_secret
        self.token=None
        self.token_expire_time=0
    def get_token(self):
        """
        Generate the token in two cases:
        1. Token is not at all generated
        2. Token expired
        
        """
        if self.token is None or time.time()>self.token_expire_time:
            auth_string=f"{self.client_id}:{self.client_secret}"
            base64_auth_string=base64.b64encode(auth_string.encode()).decode()
            
            url="https://accounts.spotify.com/api/token"
            headers={"Authorization":f"Basic {base64_auth_string}"}
            
            data={"grant_type":"client_credentials"}
            
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()
            
            self.token=result['access_token']
            self.token_expire_time=time.time()+result['expires_in'] #generally 3600 seconds
            
        return self.token
            
def get_poster(TRACK_ID):       
    spotify_class=SpotifyAuthorization(CLIENT_ID,CLIENT_SECRET)
    ACCESS_TOKEN = spotify_class.get_token()
    
    #spotify track endpoint
    url = f"https://api.spotify.com/v1/tracks/{TRACK_ID}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }


    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        images = data.get("album", {}).get("images", [])
        if images:  # non-empty list
            return images[0]["url"]
        else:
            return "https://via.placeholder.com/300?text=No+Image" 
    except Exception as e:
        print(f"Error fetching poster for {TRACK_ID}: {e}")
        return "https://via.placeholder.com/300?text=Error"
        


if __name__=="__main__":
    TRACK_ID = "3eTbOx5tsMwmdrEAVJkR5z"
    poster_url = get_poster(TRACK_ID)
    print("Poster URL:", poster_url)
    
    
    