# Job-Research
In an attempt to get a better understanding of the available jobs, I turned it into a data science project

**All this code is in PullJobData.py**

## Packages Used

* `Requests`
* `Pandas`
* `Json`
* `WordCloud`
* `MatPlotLib`
* `Seaborn`
* `Plotly`
* `Random`
* `Time`
* `Selenium`
* `Re`
* `NLTK`

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

This turned out pretty cool. Aside from it being very clear that experience is necessary, this also tells me what the main keywords are in these job postings. I found so parts to be interesting, such as insurance being common enough in the job field to be listed as a major word. These kinds of visualizations are my favorite, because there are always words you wouldn't expect which can be interesting.

Finally, I am starting to feel like I have an idea of what jobs are out there. But now how do I choose? Well, in order to solve this problem, I decided I had 3 primary priorities.
1. Whether or not I can work remote
2. Company's Field Dominance
3. Salary

Keeping these in mind I made this:

![Company Frequency Remote](https://github.com/chaseabrown/Job-Research/blob/main/CompanyFrequencyRemote.png "Company Frequency Remote")

**Sorry, I know this is hard to read on the README**

To break down this chart, the size of a square depends on the number of job postings from a given company. The way I see it, the more a company is hiring in a specific area, the more likely they are to have dominance in the field. This is not a perfect metric, but insightful nonetheless. The color of the square is about what percent of those listings are remote positions. This lets me see that companies like facebook are offering full remote positions in my field at a glance. Lastly, I put the average salaries of the positions listed inside each box, so I can clearly see around how much is being offered.

## Conclusion

All in all, this really helped me wrap my mind around the kind of positions I am looking for an helped me branch out to different opportunities that I might have missed before. 


