# Target Market Cost Savings
![brickornot](static/images/brickornot.jpg)
---
Using **Machine Learning** to cut down marketing costs for a sales or marketing campagin. Our model varifies **brick** homes or homes with siding. **Evanston, IL has a diverse mix of brick and siding homes. Evanston also had a very nice address data set. This was a great starting point for algorithm testing.** A **real estate, tuck-pointing, or painting company** can use this Machine Learning algorithm to cut down on direct marketing costs and only target brick or siding homes. This model could be tweeked for other companies such as insurance, land-scaping, or roofing.

## Goals (Some Achieved)
* Use a geocoding script/api call, to return a list of residential addresses from a single point (lat/long) or address. The goal is to retrieve a diverse mix of homes in a specific area. Look at python libraries similar to OverPy (overpass), GeoPy, or maybe even the google maps API itself.
  
* ***We have already built a custom dataset***

# **Machine Learning** (we have a working model now)
  * Find a sample script for image recognition. This may be a good starting point https://www.youtube.com/watch?v=iGWbqhdjf2s
  * Train the model from a grab of homes to recognize a brick home. '1' values = yes brick, '0' value = not brick.
  * Test model
  * Use model on homes we get from our random selection scripts above.

# To Do Next

* Web template for all pages (bootstrap, Grant's blue and gray template?) - Paule
* Learn Heroku and deploy on Heroku - Paule
* Update Grant's jupyter lab file of model - Dave & Eric
* Landing Page - Presenting our model - Eric
* model output
* visualizations
* predictions and examples
* A form to upload a house image and identify if brick or not.
* Section/page to Smarten the Algorithm - Dave
* loads inputs into a database
* lets users know when they've reached 100

  
Model - fine tuning - Grant & Dave
* use 500 x 500 pictures?
* use overfitting procedures?
* more data?
# EXTRA (maybe)
* A simple form entry of a single address, returns a table of brick homes, in a radius of that initial address entered. 
* **This final table will list homes for sales/marketing.**