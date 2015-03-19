data_raw <- read.csv("~/PycharmProjects/Dianping/dataRetr/dpshops/nb_restaurant_score_by_year_name.csv")
data_train <- data_raw[, c(4,5,6,7,10,11)]
data_train_matrix <- as.matrix(scale(data_train))
names(data_train_matrix) <- names(data_train)
require(kohonen)
som_grid <- somgrid(xdim = 20, ydim=20, topo="hexagonal")  
system.time(som_model <- som(data_train_matrix, 
                             grid=som_grid, 
                             rlen=100, 
                             alpha=c(0.05,0.01), 
                             n.hood = "circular",
                             keep.data = TRUE ))

## custom palette as per kohonen package (not compulsory)
source('~/Downloads/2014-01-SOM-Example-code_release/coolBlueHotRed.R')

plot(som_model, type = "changes")
#counts within nodes
plot(som_model, type = "counts", main="Node Counts", palette.name=coolBlueHotRed)
#map quality
plot(som_model, type = "quality", main="Node Quality/Distance", palette.name=coolBlueHotRed)
#neighbour distances
plot(som_model, type="dist.neighbours", main = "SOM neighbour distances", palette.name=grey.colors)
#code spread
plot(som_model, type = "codes")

# Plot the heatmap for a variable at scaled / normalised values
var <- 2
plot(som_model, type = "property", property = som_model$codes[,var], main=names(som_model$data)[var], palette.name=coolBlueHotRed)

# Plot the original scale heatmap for a variable from the training set:
var <- 4 #define the variable to plot
var_unscaled <- aggregate(as.numeric(data_train[,var]), by=list(som_model$unit.classif), FUN=mean, simplify=TRUE)[,2]
plot(som_model, type = "property", property=var_unscaled, main=names(data_train)[var], palette.name=coolBlueHotRed)
rm(var_unscaled, var)

source('~/Downloads/2014-01-SOM-Example-code_release/plotHeatMap.R')
mydata <- som_model$codes
wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 1:6) wss[i] <- sum(kmeans(mydata,
                                     centers=i)$withinss)
par(mar=c(5.1,4.1,4.1,2.1))
plot(1:6, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares", main="Within cluster sum of squares (WCSS)")

# Form clusters on grid
## use hierarchical clustering to cluster the codebook vectors
som_cluster <- cutree(hclust(dist(som_model$codes)), 6)

pretty_palette <- c("#1f77b4", '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2')
# Show the map with different colours for every cluster  					  
plot(som_model, type="mapping", bgcol = pretty_palette[som_cluster], main = "Clusters")
add.cluster.boundaries(som_model, som_cluster)

plot(som_model, type="codes", bgcol = pretty_palette[som_cluster], main = "Clusters")
add.cluster.boundaries(som_model, som_cluster)

cluster_details <- data.frame(data_raw$id,data_raw$NAME,data_raw$REC_DATE2,data_raw$LAT84,data_raw$LNG84,cluster=som_cluster[som_model$unit.classif])
write.csv(cluster_details, file='~/PycharmProjects/Dianping/dataRetr/dpshops/som.csv')

