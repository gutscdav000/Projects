%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is the readme file for my compound interest python simulator%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

+	compoundInterest.py	+

gets ran as any other python script. It contains most of the functions upon which
the rest of the files have been created

+   compoundInterestCommandLine.py	+

this file has been set up to take command line arguments to run the simulator function. if the wrong number of arguments is given or if they are of the wrong datatype (i.e. not an integer or float) then the script will error out.
template: 
	  python3 compoundInterestCommandLine.py <principal> <interest rate> <times compounded yearly> <years borrowed>

principal - float or int of the total principal of the loan
interest rate- the interest rate for the loan as a decimal
times compounded yearly - the number of times the loan is compounded per year
years borrowed - the number of years before the loan is terminated

ex:
	python3 compoundInterestCommandLine.py 11000 0.0429 12 2

+	realTimeSimulator.py		       +
