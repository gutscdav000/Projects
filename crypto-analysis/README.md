MY EXPERIENCE:

I saw an awesome article/tutorial on analyzing crypto currency with python. I've not used any powerful python libraries 
like plotly, nor have I used jupyter notebooks before. After I went through the tutorial I went back through and tried to 
organize, strengthen, and play with the code. 

MESSAGE TO NON-CODERS/BUSINESS/FINANCE PEOPLE:

You must install Anaconda before you are able to use jupyter notebooks which is the 
environment in which I created this project. You do not need to download Python in addition
to Anaconda because Anaconda contains a Python interpreter of its own. the first time you 
open up your environment 

every time you use this environment you must run the following commands in the terminal
in the folder in which you put the project:

MAC/LINUX:

source activate crypto-analysis
jupyter notebook

- after you run the second command the notebook will open up in your browser.
  When you are finished with the environment you'll have to use the keystroke ctrl + c
  to interupt the environment, and then press y and then enter to kill the notebook session.
  Finally run the following command to deactivate the project.
  
source deactivate

WINDOWS:

activate crypto-analysis
jupyter notebook

- after you run the second command the notebook will open up in your browser.
  When you are finished with the environment you'll have to use the keystroke ctrl + c
  to interupt the environment, and then press y and then enter to kill the notebook session.
  Finally run the following command to deactivate the project.
  
deactivate

NOTES TO ALL USERS:

- the first time you run the environment you must install the Python libraries necessary
  for the project by running the following in the terminal:
  "conda install numpy pandas nb_conda jupyter plotly quandl"
  What I have discovered is that often times when I spin up a new environment and run the code
  the graph's won't show up in the output. if you kill the current jupyter
  notebook and run the command:
  "conda install plotly quandl"
  and try restarting your jupyter notebook, I've found that in most cases this fixes the
  issue. I think most of the time it is the plotly library being dodgy, but I have found 
  instances where it was quandl. If you want to try installing just plotly and restarting 
  the jupyter notebook this might save you a little time. 
  
  
