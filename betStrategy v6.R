library(reshape2)
library(ggplot2)


###### Helper Functions #######

pToBetOdds = function(p){
  #Convert from probablity to betting odds
  #Calculate the odds you would recieve if there is no edge
  #(no one takes a cut and everyone has the same information)
  #Example: A.odds = 3 means for a $1 bet on A, should A win
  #you would be entitled to $3 (plus the return of your $1 bet)
  return((1-p)/p)
}

#Betting strategies
greedyPort = function(model.p, vegas.odds){
  #Greedy strategy finds all of the expected payouts and
  #builds a portfolio consisting of only the highest expected
  #payout strategy
  
  #Pre-allocate portfolio
  n = length(model.p)
  port = array(0, n)
  
  #Find expected values
  payouts = model.p*(vegas.odds + 1) - 1
  
  #Find max
  maxInd = which.max(payouts)
  if(payouts[maxInd] > 0){
    port[maxInd] = 1
  }
  
  return(port)
}

kellyPort = function(model.p, vegas.odds){
  #Divides up portfolio based on the kelly criteria
  fstar = (model.p*(vegas.odds + 1) - 1)/vegas.odds
  port = fstar*(fstar > 0) #cannot short bets
  if(sum(port) > 1){
    #Normalize portfolio to sum to 1
    port = port/sum(port)
  }
  return(port)
}

evenPort = function(model.p, vegas.odds){
  #Evenly distributes portfolio among bets with positive expected returns
  payouts = model.p*(vegas.odds + 1) - 1
  port = (payouts > 0)
  if(sum(port)>0){
    port = port/sum(port)
  }
  return(port)
}

portReturn = function(port, vegas.odds, groundTruth.p){
  payouts = (groundTruth.p*(vegas.odds + 1) - 1)
  return(sum(payouts*port))
}

makeModelDfs = function(home.df, away.df, draw.df, normProb = FALSE){
  
  if(normProb){
    #Normalize probabilities to 1
    probSum = home.df$probability + away.df$probability + draw.df$probability
    home.df$probability = home.df$probability/probSum
    away.df$probability = away.df$probability/probSum
    draw.df$probability = draw.df$probability/probSum
  }
  
  #merge into one wide dataframe
  model.df.wide = data.frame(ID = draw.df$X,
                             Awaywin = away.df$Awaywin,
                             Draw = draw.df$Draw,
                             Homewin = home.df$Homewin,
                             Paway = away.df$probability,
                             Pdraw = draw.df$probability,
                             Phome = home.df$probability
                        )
  model.df.wide = cbind(model.df.wide, draw.df[,3:11])
  
  #drop incomplete cases
  model.df.wide = model.df.wide[complete.cases(model.df.wide),]
  
  #Create a long dataframe of all complete case games
  gameIDs = model.df.wide$ID
  
  home.df.long = melt(home.df[home.df$X %in% gameIDs,c("X","Homewin","B365H","BWH","LBH","probability")],
                      id.vars = c("X","Homewin","probability"))
  colnames(home.df.long) = c("ID","outcome","probability","oddsMaker","decimalOdds")
  home.df.long$bet = "home"
  
  away.df.long = melt(away.df[away.df$X %in% gameIDs,c("X","Awaywin","B365A","BWA","LBA","probability")],
                      id.vars = c("X","Awaywin","probability"))
  colnames(away.df.long) = c("ID","outcome","probability","oddsMaker","decimalOdds")
  away.df.long$bet = "away"
  
  draw.df.long = melt(draw.df[draw.df$X %in% gameIDs,c("X","Draw","B365D","BWD","LBD","probability")],
                      id.vars = c("X","Draw","probability"))
  colnames(draw.df.long) = c("ID","outcome","probability","oddsMaker","decimalOdds")
  draw.df.long$bet = "draw"
  
  #combine dataframes
  model.df.long = rbind(home.df.long, away.df.long, draw.df.long)
  
  #remove last letter from oddsMaker
  model.df.long$oddsMaker = substr(model.df.long$oddsMaker,1,nchar(as.character(model.df.long$oddsMaker))-1)
  
  #calculate vegas odds
  model.df.long$vegasOdds = model.df.long$decimalOdds - 1
  
  #reorder columns, sort, fix row names
  model.df.long = model.df.long[,c(1,6,4,5,7,3,2)]
  model.df.long = model.df.long[with(model.df.long, order(ID, bet, oddsMaker)), ]
  rownames(model.df.long) = NULL
  
  return(list(df.wide = model.df.wide,
              df.long = model.df.long))
}

randGameSet = function(games, setSize = 50, nSets = NULL){
  nGames = length(games)
  
  #set/check nSets
  nSets = min(floor(nGames/setSize), nSets) #cannot have nSets*setSize > nGames
  
  #randomize games
  randSample = sample(games, nSets*setSize)
  randSets = split(randSample,rep(1:nSets, each = setSize))
  
  #build datafram
  df = data.frame(period = seq(nSets), gameSet = NA)
  for(i in 1:nSets){
    df$gameSet[i] = randSets[as.character(i)]
  }
  
  return(df)
}

betStratSim = function(df.long, gameSets, strategy, fracBet = .2, bankRoll0 = 1){
  nSets = nrow(gameSets)
  gameSets$return = NA
  for(i in 1:nSets){
    bet.df = df.long[df.long$ID %in% gameSets[i,"gameSet"][[1]],]
    model.p = bet.df$probability
    vegas.odds = bet.df$vegasOdds
    groundTruth.p = (bet.df$outcome == "Yes")
    port = strategy(model.p, vegas.odds)
    ret = portReturn(port, vegas.odds, groundTruth.p)
    gameSets[i,"return"] = ret
  }
  gameSets$growth = 1 + gameSets$return*fracBet
  gameSets$growth = gameSets$growth*(gameSets$growth > 0) #growth can't be negative, lost all money
  gameSets$bankRoll = cumprod(gameSets$growth)*bankRoll0
  return(gameSets)
}

betStratSimMany = function(df.long, strategy, nSim = 20, fracBet = 0.2, bankRoll0 = 1, setSize = 50, nSets = NULL){
  
  games = unique(df.long$ID)
  nGames = length(games)
  #set/check nSets
  nSets = min(floor(nGames/setSize), nSets) #cannot have nSets*setSize > nGames
  
  results = data.frame(period = seq(nSets))
  
  #Run simulations
  for(i in 1:nSim){
    gameSets = randGameSet(games, setSize = setSize, nSets = nSets)
    gameSets = betStratSim(df.long, gameSets, strategy, fracBet = fracBet, bankRoll0 = bankRoll0)
    results[,as.character(i)] = gameSets$bankRoll
  }
  
  #Add in initial condition
  results = rbind(c(0,array(bankRoll0,ncol(results)-1)),results)
  return(results)
}

#Plot the simulation
plotSim = function(sim, title = "", lineColor = "black", bandColor = "grey12", show.legend = T, xlim = NULL, ylim = NULL){
  simData = as.matrix(sim[,-1])
  sim$mean = rowMeans(simData)
  sim$median = apply(simData, 1, median, na.rm = T)
  sim$sd = apply(simData,1, sd, na.rm = T)
  sim$lb95 = apply(simData, 1, quantile, probs = 0.05, na.rm = T)
  sim$ub95 = apply(simData, 1, quantile, probs = 0.95, na.rm = T)
  g = ggplot(data = sim, aes(x = period))
  g = g + geom_ribbon(aes(ymin = lb95, ymax = ub95, fill = "90% Interval"), alpha = 0.3) + scale_fill_manual("", values = bandColor)
  g = g + geom_line(aes(y = median, color = "median")) + scale_colour_manual("", values = lineColor)
  g = g + labs(x = "Bet Period", y = "Bank Roll", title = title)
  g = g + coord_cartesian(xlim = xlim, ylim = ylim)
  if(!show.legend){
    g = g + guides(fill = F, color = F)
  }
  return(g)
}

#get returns from simulation
simReturns = function(sim){
  n = nrow(sim)
  returns = (sim[2:n,-1]-sim[1:n-1,-1])/sim[1:n-1,-1]
  returns = cbind(period = sim[2:n,1], returns)
  return(returns)
}

simLogReturns = function(sim){
  n = nrow(sim)
  returns = log(sim[2:n,-1]/sim[1:n-1,-1])
  returns = cbind(period = sim[2:n,1], returns)
  return(returns)
}

#get mean, standard devation, and sharp ratio
mss = function(logReturns, nperyear = 104){
  retMat = as.matrix(logReturns[,-1])
  m = mean(retMat)
  s = sd(retMat)
  sharp = nperyear*m/(sqrt(nperyear)*s)
  return(list(m = m, s = s, sharp = sharp))
}

tableData = function(sim, period = 300){
  initial = as.matrix(sim[1, -1])
  periodResults = as.matrix(sim[sim$period == period, -1])
  returns = (periodResults - initial)/initial
  m = mean(returns)
  s = sd(returns)
  return(list(m = m, s = s))
}

###### Script #######

#Read in data
home.df = read.csv("log_reg_homewins.csv")
away.df = read.csv("log_reg_awaywins.csv")
draw.df = read.csv("log_reg_draws.csv")

#remove what we don't need
keepCols = c(1:11,28)
home.df = home.df[,keepCols]
away.df = away.df[,keepCols]
draw.df = draw.df[,keepCols]

#Make long and wide data frames
out1 = makeModelDfs(home.df, away.df, draw.df, normProb = FALSE)
out2 = makeModelDfs(home.df, away.df, draw.df, normProb = TRUE)
df.wide = out1$df.wide
df.long = out1$df.long
df.wide.norm = out2$df.wide
df.long.norm = out2$df.long

#Example Simulation
#sim1 = betStratSimMany(df.long.norm, kellyPort, nSim = 20, fracBet = .1)
#print(plotSim(sim1, title = "Kelly criteria"))
#print(mss(simReturns(sim1)))
