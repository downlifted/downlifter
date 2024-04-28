# downlifter
Download unlimited NFTs from IPFS QUICK & EASY, 

You will need to get the IPFS URI from Etherscan by viewing the contract, for example the Bored Ape URI is set
To get this URI Simply find the Etherscan, click CONTRACT, find the URI and that will be what you paste into the 
Code, Just edit 

base_url = "https://ipfs.io/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/"

To your specific collection.

There's also an option for how many items you want to get, you can edit that in the code where it says

# Define the range for this instance
start_image_number = last_processed_image + 1
end_image_number = start_image_number + 10001
total_images = end_image_number - start_image_number

Simply change 10001 to your deired number of NFTs to download.

Also, because some NFTS are to small I have told it to resize them all to 1000x1000

To edit that find:

                img = Image.open(img_filename)
                img_resized = img.resize((1000, 1000))
                img_resized.save(img_filename)


HAVE FUN - HAPPY SCRAPING!
