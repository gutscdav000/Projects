


def compoundedInterestCalculatorTotal(principal, interestRate, timesCompoundedYearly, yearsBorrowed):
    ## @params
    ## principal - initial amount borrowed
    ## interestRate - anual interest rate
    ## timesCompoundedYearly - number of times the interest is compounded yearly
    ## yearsBorrowed - number of years the amount is borrowed for
    ## @returns Amount of money accumulated after n years, including interest
    
    oneNum = 1 + (interestRate/timesCompoundedYearly)
    expNum = timesCompoundedYearly * yearsBorrowed
    result = oneNum ** expNum

    return (principal * result)

def interestCalculator(principal, interestRate, timesCompoundedYearly, yearsBorrowed):
    ## @params
    ## principal - initial amount borrowed
    ## interestRate - anual interest rate
    ## timesCompoundedYearly - number of times the interest is compounded yearly
    ## yearsBorrowed - number of years the amount is borrowed for
    ## @returns the interest that has been accumulated over the yearsBorrowed

    return compoundedInterestCalculatorTotal(principal, interestRate, timesCompoundedYearly, yearsBorrowed) - principal

def formatSim(interval, interest, totalDue):
    ## @params
    ## interval - time interval per calculation
    ## interest - only the calculated interest value
    ## totalDue - the interest + principal
    
    formatting = "\n|  {0:" + str(len(interval)) + "}  |||  {1:5.2f}  |  {2:5.2f}  \t|\n"
    formatting = formatting.format(interval, interest, totalDue)
    lineLen = len(formatting)
    horozontalLine = "-" * lineLen
    output = formatting + horozontalLine
    
    return output, lineLen


def interestGrowthSim(principal, interestRate, timesCompoundedYearly, yearsBorrowed):
    ## @params                                                                                                                                                                              
    ## principal - initial amount borrowed                                                                                                                                                                 
    ## interestRate - anual interest rate                                                                                                                                                                  
    ## timesCompoundedYearly - number of times the interest is compounded yearly                                                                                                                           
    ## yearsBorrowed - number of years the amount is borrowed for                                                                                                                            
    ## @returns the interest that has been accumulated over the yearsBorrowed 
    
    incrementer = 0
    timeLeft = yearsBorrowed * timesCompoundedYearly
    displayNumber = 1
    
    # branches to catch common timesCompoundedYearly or increment from [1, timesCompoundedYearly]
    intervalUnit = "\t"
    if int(timesCompoundedYearly) == 12:
        intervalUnit = "month"
    elif int(timesCompoundedYearly) == 52:
        intervalUnit = "week"
    elif int(timesCompoundedYearly) == 365:
        intervalUnit = "day"
    elif int(timesCompoundedYearly) == 1:
        intervalUnit = "year"
    
        
        
    #loop to continually decrement timeLeft and calculate metrics
    while(incrementer < timeLeft):

        #calculate metrics
        timeSpan = lambda t: t/timesCompoundedYearly 

        interest = interestCalculator(principal, interestRate, timesCompoundedYearly, timeSpan(incrementer))
        totalDue = compoundedInterestCalculatorTotal(principal, interestRate, timesCompoundedYearly, timeSpan(incrementer))
        #format/print metrics
        interval = str(intervalUnit) + " " + str(displayNumber)
        output, lineLen = formatSim(interval, interest, totalDue)

        if incrementer == 0:
            print(str(lineLen) + output)
        else:
            print(output)

        incrementer += 1
        displayNumber += 1


interestGrowthSim(11000,0.0429, 12, 2)
print()
