#prompting for ratings
print("Enter the user based accuracy ratings for this article: ")
#reading reader ratings for current article
ratings = [ int(r) for r in input().split()]
number_of_ratings = len(ratings)
median_of_ratings = 0
ratings_to_check = []
clean_ratings = []
std_dev = None
current_mean = sum(ratings)/number_of_ratings
ratings.sort()

#PRE-PROCESSING TO ACCOUNT FOR ROGUE VALUES
if number_of_ratings % 2 == 1:
  median_of_ratings = ratings[int((number_of_ratings-1)/2)]
else:
  median_of_ratings = (ratings[int((number_of_ratings/2)-1)]+ ratings[int(number_of_ratings/2)])/2

# checking if sample size of ratings is large enough to filter outliers & potentially apply Central Limit Theorem if sample size large enough
# to asssume normal distribution of sample.
# assume size > 50 is large enough (can be modified depending upon number of readers newspaper has)
if number_of_ratings > 50:
  #if rating is smaller than half the median, or greater than 1.5 times the median, filter temporarily
  #lower and upper limits can be modified, depnding on how strict the filter is desired
  #filter negative ratings and ratings above 100
  while ratings:
    if ratings[0] < 0 or ratings[0] > 100 or ratings[0] < 0.5*median_of_ratings or ratings[0] > 1.5*median_of_ratings:
      ratings_to_check.append(ratings.pop(0))
    else:
      clean_ratings.append(ratings.pop(0))
  #check if there is at least some clean data to avoid division by 0 later
  if clean_ratings:
    filtered_mean = sum(clean_ratings)/len(clean_ratings)
  else:
    print("This article may contain inaccuracies.")
    exit(0)


  #if removing outliers makes spread more even, filter out, or else, stick to original.
  #minimum requirement for improvement in mean can be modified, depending on how strict filter criterion is required
  if abs(filtered_mean-median_of_ratings) > 0.5*abs(current_mean - median_of_ratings):
    for r in ratings_to_check:
      clean_ratings.append(r)

  #calculating potentially filtered mean after checks
  final_mean = sum(clean_ratings)/len(clean_ratings)
  #calculating variance and standard deviation after filtering
  #check sd despite applying Central Limit Theorem, just to be safe. Can be removed if strictness not required.
  var = sum((x - final_mean)**2 for x in clean_ratings) / len(clean_ratings)
  std_dev = var ** 0.5

if  not std_dev or std_dev > 20:
  #may not have enough ratings to generalize accuracy rating OR
  #data is too contaimnated 
  #so we disregard ratings and display a general nudge
  print("This article may contain inaccuracies.")
  exit(0)
else:
  #round to 2 decimal places and bold the rating
  print("Previous readers have reported an accuracy of "+"\033[1m" + (str(round(final_mean,2))) + "\033[0m"+"% for this article.")




