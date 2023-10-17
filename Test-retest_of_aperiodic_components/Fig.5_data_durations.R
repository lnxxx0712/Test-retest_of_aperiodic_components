library(tidyverse)
library(ggpubr)
library(rstatix)
library(readxl)
library(stats)
library(ggplot2)

setwd("F:/...")
data <- read_excel("exp_icc.xlsx")

filtered_data <- data[data$time_interval == "Long", ]

data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      sd = sd(x[[col]], na.rm=TRUE),
      se = sd(x[[col]], na.rm=TRUE) / sqrt(length(x[[col]])))  
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

df3 <- data_summary(filtered_data, varname="ICC_value", 
                    groupnames=c("state", "time_duration"))

# Histogram plot
p <- ggplot(df3, aes(x=state, y=ICC_value, fill=time_duration)) + 
  
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.75, ymax = 1),
            fill = "lightgray", alpha = 0.5, inherit.aes = FALSE) +
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.6, ymax = 0.75),
            fill = "gainsboro", alpha = 0.5, inherit.aes = FALSE) +
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.4, ymax = 0.6),
            fill = "whitesmoke", alpha = 0.5, inherit.aes = FALSE)+
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = 0.4),
            fill = "white", alpha = 0.5, inherit.aes = FALSE)+
  
  geom_bar(stat="identity", position=position_dodge(),width = .7,
           color="Black") +  
  
  geom_errorbar(aes(ymin=ICC_value-se, ymax=ICC_value+se), width=.1,  
                position=position_dodge(.7)) +  
  ylim(0,1)+
  
  scale_fill_brewer(palette="Blues") + 
  
  theme_minimal()+
  
  theme_bw() +
  theme(
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_text(size = 12, face = "bold"),
    axis.title.y = element_text(size = 12, face = "bold")
  )

p

# Pairwise comparisons between time_duration groups
pwc <- filtered_data %>%
  group_by(state) %>%
  pairwise_t_test(
    ICC_value ~ time_duration, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc

