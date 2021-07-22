# Job-Research
In an attempt to get a better understanding of the available jobs, I turned it into a data science project

**All this code is in PullJobData.py**

## Getting the Data

Using RapidAPI, I was able to find an API that allowed me to pull job search results from Indeed, so I put in the search terms I was interested in and got about 1000 results.

The search terms were:
* AWS
* Amazon Web Services
* Data Science
* AI
* Machine Learning

Then I mixed those terms into a few search queries.

## Supplement Missing Data

This API call only returned a short portion of the description of each term and that was an issue because most of the crucial information is in the description. To solve this problem, I used Selenium to pull the full descriptions from Indeed.com using a Chrome Driver.

This allowed me to go ahead and pull the salary information from the job descriptions. To do this, I pulled any word that a $ in it then used a little logic to clear out the results that were obviously not salaries. This wasn't a perfect soluton, but it was quick and got close enough to what I was looking for.

If you would like to see the data after all of this, it is save in the  `jobListings.csv` file in this repo.

## Data Visualization

I am personally interested in a remote position, so for starters, I wanted to see what percent of the results are remote.

![Remote Pie Chart](https://github.com/chaseabrown/Job-Research/blob/main/RemotePieChart.png "Remote Pie Chart")

A third of the positions being remote is a great thing to see, but where are these jobs located?

![Job Postings By Location](https://github.com/chaseabrown/Job-Research/blob/main/JobPostingsByLocation.png "Job Postings By Location")

Texas, California, New York, Massachusetts, and Washington seem to be the top states where these companies are hiring from. This makes sense from what I know of the market as these are all states that are becoming tech hubs in their own ways. The city view just gave me a closer look at specifics.

Now that I am aware of the location and residency requirements of the job offerings, I wanted to get a look at what exactly these positions are hiring for. To do this, I used NLTK's stop word library to eliminate stop words from the job descritions. With this data I created a word frequency map to get an idea of what was being asked for.

![Description Word Map](https://github.com/chaseabrown/Job-Research/blob/main/DescriptionWordMap.png "Description Word Map")


