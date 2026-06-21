import io
from io import BytesIO
from PIL import Image, ImageDraw
from PIL import Image
from imgurpython import ImgurClient
#client_id get from imgur apllication
#my own client id

class Screen_shoot:
    from PIL import Image, ImageDraw
    import io
    def screen_shot(self, screen):
        image = Image.open(io.BytesIO(screen))

        # Save Pillow Image to memory as PNG
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Upload to FreeImage.host
        files = {
            "source": ("screenshot.png", buffer, "image/png")
        }
        data = {
            "key": "anonymous",
            "action": "upload"
        }

        response = requests.post("https://freeimage.host/api/1/upload", files=files, data=data)
        if response.status_code == 200:
            return response.json()["image"]["url"]
        else:
            raise Exception(f"Upload failed: {response.text}")





            # Step 1: Save image to memory buffer
            # buffer = io.BytesIO()
            # screen.save(buffer, format="PNG")
            # buffer.seek(0)
            #
            # # Step 2: Upload to freeimage.host
            # url = "https://freeimage.host/api/1/upload"
            # files = {
            #     "source": ("screenshot.png", buffer, "image/png")
            # }
            # data = {
            #     "key": "anonymous",  # Anonymous upload
            #     "action": "upload"
            # }
            #
            # response = requests.post(url, files=files, data=data)
            #
            # if response.status_code == 200:
            #     return response.json()["image"]["url"]
            # else:
            #     raise Exception(f"Upload failed: {response.text}")

    # # Example usage:
    # # Create an image with Pillow
    # image = Image.new("RGB", (300, 100), color="skyblue")
    # draw = ImageDraw.Draw(image)
    # draw.text((10, 40), "Hello from Pillow!", fill="black")
    #
    # # Upload and get URL
    # screenshot = Screen_shoot()
    # url = screenshot.screen_shot(image)
    # print("Image URL:", url)

    # def screen_shot(self,screen):
    #         # Step 1: Get server
    #         # server_response = requests.get("https://api.gofile.io/getServer")
    #         server_response = requests.get("https://apiv2.gofile.io/getServer")
    #
    #         server = server_response.json()["data"]["server"]
    #
    #         # Step 2: Upload the file
    #         with open(screen, 'rb') as f:
    #             files = {'file': f}
    #             upload_url = f"https://{server}.gofile.io/uploadFile"
    #             response = requests.post(upload_url, files=files)
    #             if response.status_code == 200:
    #                 return response.json()["data"]["downloadPage"]
    #             else:
    #                 raise Exception("Upload failed")















        # filename=screen.filename


        # driver.save_screenshot(screenshot_filename)

        # client = ImgurClient(client_id, None)
        #
        # uploaded_image = client.upload_from_path(screenshot_filename, config=None, anon=True)
        # return uploaded_image['link']

        # Upload the image to Imgur

        # Replace 'YOUR_CLIENT_ID' with your actual Imgur client ID
        # client_id = '696d29db30f5a10'  # my own account client id
        #
        # # Upload the image to Imgur
        # # with open(screen, "rb") as f:
        #
        # response = requests.post(
        #         "https://api.imgur.com/3/upload",
        #         headers={"Authorization": f"Client-ID {client_id}"},
        #         files={"image": screen},
        #     )
        # data = response.json()
        #
        # if response.status_code == 200:
        #     imgur_url = data["data"]["link"]
        #     return imgur_url
        #
        # else:
        #     print("Image upload failed.")
