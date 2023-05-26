# web-scraper-newsletter
What is this about? In short: Scrapping music concert data from a web page and sending the content to email subscribers.
This is, however, only a little (first) side project that is limited to scrapping data from the German webpage www.livegigs.de with preset search filters (venue range, music genre, ...). Though, other websites are of course also conceivable, the code is only intended to show in a simple way how such a project could be put into practice. The result of the web-scrap is being transformed to a DataFrame, which then will be sent to email recipients.

To automatize this job, I used a crontab job that runs every minute. Why is this? The actual goal is to send the data on a monthly basis, but this would mean that I have to be on my computer at that exact moment once a month for the job to be executed (unless one uses a server for that kind of task). To avoid this, the script creates an empty .txt file (as a log-file, so to speak), and checks before each execution whether the file has already been created for the current month (the file name is: `<current_month>_<current_year>.txt`). If yes, the export is not executed, if not, the export takes place and the file is created for the first time for this month. This works because it is quite likely that I sit on my computer once a month and then at that exact moment the script can be executed.

To set up a crontab job, you can, for instance, refer to [here](https://blog.dennisokeeffe.com/blog/2021-01-19-running-cronjobs-on-your-local-mac). In my case, the crontab job looks like the following:

`* * * * * source /path/to/venv/bin/activate && /path/to/venv/bin/python3 /path/to/script/ska_web_scrap.py`

Of course, other intervals at which the export is carried out are also conceivable. The [Crontab Guru](https://crontab.guru) can help you to extract the desired cron schedule expressions. By using log-files, you can also easily trace in which periods the newsletter has been actually sent out. Note that for privacy reasons, I had to replace email adresses, passwords etc. by dummy values. Alsp note that the email settings refer to an outlook mail account but a simple google search should give you the configs for other mail providers such as gmail.

To improve this project, the code could be refactored in such way that it expects an input when calling the script in which we can specify the recipients email adresses for instance (*something like python3 my_script.py --your_email@gmail.com*). Additionally, the html view of the DataFrame could surely be beautified.

## Getting started

I recommend to use a [virtual environment](https://docs.python.org/3/library/venv.html). Once installed, install the packages from the requirements-file:

`pip install -r requirements.txt`

And that's it! You are ready to go.

