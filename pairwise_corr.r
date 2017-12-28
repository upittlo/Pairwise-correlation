rm(list = ls())
library(dplyr)
library(tidytext)
library(janeaustenr)
library(widyr)
library(jsonlite)
library(stringr)
library(textstem)

setwd("D:\\Project2017\\word correlation")

#raw = read.csv("dpreview.json")[,"content"]

raw <- stream_in(file("dpreview_revised.json"))
### order by date
raw = raw[order(as.Date(raw$posted_at),decreasing = T),]

### Use only 10W data for testing
raw = raw[1:100000,]

#################### Custom stop words  ####################
remove_words = c('hi','ok','etc','yes',"against","no"
                ,"its","were","once","about","after"
                ,"yourself","her","too","into","http",
                "us","thank","versus","com","would",
                "thanks","thing","cc","lot","bit","year",
                "even","though","way","day","time","vice","versa")

custom_stop_words <- bind_rows(data_frame(word = remove_words, 
                              lexicon = "custom"),stop_words)

##############################################################

############################################
####### Regular Expression   ###############
#############################################


reg_exp = function(s_input){
  s_output = gsub("(http\\S+|www\\S+|WWW\\S+)","",s_input)
  s_output = gsub('\\[/QUOTE\\]',' ',s_output)
  s_output = gsub('(-- hide signature --)(.*)$','',s_output)
  s_output = gsub('<[^>]*>','',s_output)
  s_output = gsub("[^[:alnum:]]", " ", s_output)
  #s_output = gsub('(\\.\\s+)','. ',s_output)
  return (s_output)                
}
###################################################

### Create row id as group
raw <- tibble::rowid_to_column(raw, "review_id")
raw$content = reg_exp(raw$content)


df_text = raw[,c("review_id","content")]

### str_detect(word,"[A-Za-z]") remove all "Pure" numerical words
### word lemmatize
### filter frequency lower than 30
### filter word length lower than 3


df_word_corr =df_text %>%
  unnest_tokens(word,content) %>%
  filter(!word %in% custom_stop_words$word) %>%
  mutate(word = lemmatize_words(word)) %>%
  filter(!word %in% stop_words$word) %>%
  filter(str_detect(word,"[A-Za-z]")) %>%
  filter(nchar(word)>3) %>%
  group_by(word) %>%
  filter(n() >= 30)%>%
  ungroup() %>%
  pairwise_cor(word,review_id,sort = TRUE) %>%
  filter(correlation >0) %>% 
  group_by(item1) %>%
  top_n(10) %>%
  ungroup()

df_word_corr

########  type word to see the result   ####


testword = tolower("benq")
df_word_corr %>%
  filter(item1 == testword)




#write.csv(df_word_corr,"word_corr(100000).csv")

#####################################
####################################

