# Target Market Cost Savings
![brickornot](static/images/brickornot.jpg)
---
Using **Machine Learning** to narrow down marketing costs for a direct mailing campagin. Our model varifies **brick** homes near a specific location. **West Logan Square in Chicago has a diverse mix of brick and siding homes. This may be a good starting point for algorithm testing.** A **tuck pointing company** can use this Machine Learning algorithm to cut down on direct mailing costs and only target brick homes for sales. This model could be tweeked for other companies such as insurance, real estate, land-scaping, or roofing.

## Goals
* Use a geocoding script/api call, to return a list of residential addresses from a single point (lat/long) on a map. The goal is to retrieve a diverse mix of homes in a specific block radius. Look at python libraries similar to OverPy (overpass), GeoPy, or maybe even the google maps API itself.
* Use a Python script such as, https://andrewpwheeler.com/2015/12/28/using-python-to-grab-google-street-view-imagery/. This will grab a image of the homes we return from google street view.
* **Machine Learning**
    * Find a sample script for image recognition. This may be a good starting point https://www.youtube.com/watch?v=iGWbqhdjf2s
    * Train the model from a grab of homes to recognize a brick home. '1' values = yes brick, '0' value = not brick.
    * Test model
    * Use model on homes we get from our random selection scripts above.

* Final deployment on Heroku using a bootstrap website. A simple form entry of a single address, returns a table of brick homes, in a radius of that initial address entered.
* **This final table list of displayed brick homes will be the direct mail homes.**