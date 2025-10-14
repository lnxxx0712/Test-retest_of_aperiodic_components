library(tidyverse)
library(ggpubr)
library(rstatix)
library(readxl)
library(stats)
library(ggplot2)

setwd("F:/5type_result/ICC/AR_300/combine/new")
data <- read_excel("combine.xlsx")

filtered_data <- data[data$methods == "FOOOF",]

# summary statstics
filtered_data %>%
  group_by(state, time_interval,index) %>%
  get_summary_stats(ICC_value, type = "mean_sd") %>%
  mutate(mean = round(mean, 5))

## check assumptions
# Outliers
filtered_data %>%
  group_by(state, time_interval, index) %>%
  identify_outliers(ICC_value)

# Normality assumption
filtered_data %>%
  group_by(state, time_interval, index) %>%
  shapiro_test(ICC_value)

ggqqplot(filtered_data, "ICC_value", ggtheme = theme_bw()) +
  facet_grid(state + index~ time_interval, labeller = "label_both")

# computation
res.aov <- anova_test(
  data = filtered_data[filtered_data$index == "Exponent",], # Change to Exponent/Offset
  dv = ICC_value, wid = ch_id,
  within = c(state, time_interval)  
)
get_anova_table(res.aov)


## Post-hoc tests
# Two-way ANOVA at each state level
one.way <- filtered_data[filtered_data$index == "Exponent",] %>%
  group_by(state) %>%
  anova_test(dv = ICC_value, wid = ch_id, within = time_interval)%>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way

# Pairwise comparisons between time_interval groups
pwc <- filtered_data %>%
  group_by(state, index) %>%
  pairwise_t_test(
    ICC_value ~ time_interval, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc

# Effect of time at each level of treatment
one.way2 <- filtered_data[filtered_data$index == "Exponent",] %>%
  group_by(time_interval) %>%
  anova_test(dv = ICC_value, wid = ch_id, within = state) %>%
  get_anova_table() %>%
  adjust_pvalue(method = "bonferroni")
one.way2

# Pairwise comparisons between time points
pwc2 <- filtered_data %>%
  group_by(time_interval,index) %>%
  pairwise_t_test(
    ICC_value ~ state, paired = TRUE,
    p.adjust.method = "bonferroni"
  )
pwc2

## Histagram plot
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
                    groupnames=c("state","index", "time_interval"))

p <- ggplot(df3, aes(x=time_interval, y=ICC_value, fill=state)) + 
  
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.75, ymax = 1),
            fill = "lightgray", alpha = 0.5, inherit.aes = FALSE) +
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.6, ymax = 0.75),
            fill = "gainsboro", alpha = 0.5, inherit.aes = FALSE) +
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = 0.4, ymax = 0.6),
            fill = "whitesmoke", alpha = 0.5, inherit.aes = FALSE)+
  geom_rect(aes(xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = 0.4),
            fill = "white", alpha = 0.5, inherit.aes = FALSE)+
  
  geom_bar(stat="identity", position=position_dodge(),width = .5,
           color="Black") +  
  
  facet_wrap(~index, ncol = 1) +  
  
  geom_errorbar(aes(ymin=ICC_value-se, ymax=ICC_value+se), width=.1,  
                position=position_dodge(.5)) +  
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
