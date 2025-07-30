from sklearn.decomposition import PCA
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def plotPCA(mat,labels):
    # columns are samples and rows are genes
    pca = PCA(n_components=3)
    pca.fit(mat)
    ax = scatter3(pca.components_.T,labels)
    ax.set_xlabel('PC1 ('+format(pca.explained_variance_ratio_[0],'.2')+')')
    ax.set_ylabel('PC2 ('+format(pca.explained_variance_ratio_[1],'.2')+')')
    ax.set_zlabel('PC3 ('+format(pca.explained_variance_ratio_[2],'.2')+')')

    
def plotMDS(distMat,groups=None,labels=None):
	# input should be distance matrix
	mds = MDS(dissimilarity="precomputed",
	max_iter=10000,eps=1e-6)
	mds.fit(distMat)
	coordinates = mds.embedding_
	fig = plt.figure()
	ax = fig.add_subplot(111)
	if groups:
		colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
		uniqGroups = list(set(groups))
		groupColors = []
		for group in groups:
			idx = uniqGroups.index(group)
			groupColors.append(colors[idx])
		ax.scatter(coordinates[:,0],coordinates[:,1],c=groupColors)
	else:
		ax.scatter(coordinates[:,0],coordinates[:,1])
	if labels:
		for i,label in enumerate(labels):
			ax.annotate(label,xy=(coordinates[i,0],coordinates[i,1]),
			xytext=(coordinates[i,0],coordinates[i,1]+0.05))
	return ax

def scatter3(mat,labels):
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    # colors = ['r','b','g','c','m','y',]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plottedLabels = []
    for i, label in enumerate(set(labels)):
        plottedLabels.append(label)
        idx = np.array([True if item==label else False for item in labels])
        print(label,colors[i])
        subMat = mat[idx,:]
        xs = subMat[:,0]
        ys = subMat[:,1]
        zs = subMat[:,2]
        ax.scatter(xs, ys, zs, c=colors[i], marker='o')
#     plt.show()
    plt.legend(plottedLabels)
    return ax