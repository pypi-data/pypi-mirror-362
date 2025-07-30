from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Cluster_statistics:
    """
    Class to that holds statistics on the clusters.
    """

    def __init__(self, num_clusters: int, silhouette_score: float, centroids: list, radius: list[float], labels_percetages: list[float]):
        """
        Initialize the Cluster_statistics object with the number of clusters, inertia, and silhouette score.
        """
        self.num_clusters = num_clusters
        self.silhouette_score = silhouette_score
        self.centroids = centroids
        self.radius = radius
        self.labels_percetages = labels_percetages

    def __repr__(self):
        """
        String representation of the Cluster_statistics object.
        """

        radius_str = ', '.join(f'{r:.4f}' for r in self.radius)
        centroids_str = ', '.join(f'[{", ".join(f"{c:.4f}" for c in centroid)}]' for centroid in self.centroids)

        return (f"Cluster_statistics(num_clusters={self.num_clusters},\n"
                f"silhouette_score={self.silhouette_score:.4f},\n"
                f"centroids={centroids_str},\n"
                f"radius={radius_str},\n"
                f"labels_percentages={self.labels_percetages})")

class ClusterChanges:
    """
    A class to represent the changes in clustering between two datasets.
    """

    def __init__(self, original: Cluster_statistics, new_data: Cluster_statistics, delta: float = 0.1):
        """
        Initializes the ClusterChanges with statistics from two clustering results.
        """
        self.original = original
        self.new_data = new_data
        self.delta = delta

        self.changed = dict()
        self.unchanged = dict()

        if original.num_clusters != new_data.num_clusters:
            self.changed['num_clusters'] = 100 * abs(original.num_clusters - new_data.num_clusters) / original.num_clusters
        else:
            self.unchanged['num_clusters'] = 100 * abs(original.num_clusters - new_data.num_clusters) / original.num_clusters

        metrics = [
            ("silhouette_score", original.silhouette_score, new_data.silhouette_score, delta * original.silhouette_score),
        ]

        if original.num_clusters == new_data.num_clusters:
            new_data = ClusterChanges.reorder_changes(original, new_data)

            # Compare centroids and radius
            for i, (orig_centroid, new_centroid, orig_radius) in enumerate(zip(original.centroids, new_data.centroids, original.radius)):
                metrics.append(
                    (f'centroid_{i}', np.linalg.norm(orig_centroid), np.linalg.norm(new_centroid), delta * orig_radius)
                )

            for i, (orig_radius, new_radius) in enumerate(zip(original.radius, new_data.radius)):
                metrics.append(
                    (f'radius_{i}', orig_radius, new_radius, delta * orig_radius)
                )

            for i, (orig_label_percentage, new_label_percentage) in enumerate(zip(original.labels_percetages, new_data.labels_percetages)):
                metrics.append(
                    (f'label_percentage_{i}', orig_label_percentage, new_label_percentage, delta * orig_label_percentage)
                )

        for name, orig_val, new_val, threshold in metrics:
            if type(orig_val) is np.ndarray and type(new_val) is np.ndarray:
                diff = np.linalg.norm(orig_val - new_val)
            else:
                diff = abs(orig_val - new_val)
            # Avoid division by zero
            if threshold == 0:
                percentage_diff = 0
            else:
                percentage_diff = diff / abs(threshold)
                if diff > abs(threshold):
                    self.changed[name] = int(percentage_diff * 100)
                else:
                    self.unchanged[name] = int(percentage_diff * 100)

    def __repr__(self):
        """
        Returns a string representation of the ClusterChanges.
        """
        change_str = ', '.join([f"{k}: {v}%" for k, v in self.changed.items()])
        unchanged_str = ', '.join([f"{k}: {v}%" for k, v in self.unchanged.items()])

        return (f"Change: {change_str}, Unchanged: {unchanged_str}, delta: {self.delta}")
    
    def reorder_changes(original, new_data):
        """
        Reorder the changes to match the order of another ClusterChanges object.
        """
        new_centroid_positions = []
        for i in range(original.num_clusters):
            min_distance = float('inf')
            for j in range(new_data.num_clusters):
                distance = np.linalg.norm(original.centroids[i] - new_data.centroids[j])
                if distance < min_distance:
                    min_distance = distance
            new_centroid_positions.append(min_distance)       
        
        # Order centroids and related statistics by closest new centroid positions
        order = np.argsort(new_centroid_positions)
        new_data.centroids = [new_data.centroids[i] for i in order]
        new_data.radius = [new_data.radius[i] for i in order]
        new_data.labels_percetages = [new_data.labels_percetages[i] for i in order]

        return new_data

def _calculate_radius(X, kmeans):
    """
    Calculate the radius of each cluster based on the distance of points to their respective centroids.
    """

    X = np.array(X, dtype=float)
    radius = [0]*len(kmeans.cluster_centers_)
    for data_point, label in zip(X, kmeans.labels_):
        radius[label] = max(radius[label], np.linalg.norm(data_point-kmeans.cluster_centers_))

    return radius

def plot_clusters(X, kmeans, best_cluster):
    """
    Plot the clusters and their centroids.
    """
    if len(X.columns) == 2:
        plt.figure(figsize=(8, 4))
        plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=kmeans.labels_, cmap='viridis', marker='o')
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x', s=100, label='Centroids')
        plt.title(f'KMeans Clustering with {best_cluster} clusters')
        plt.xlabel(X.columns[0])
        plt.ylabel(X.columns[1])
        plt.legend()
        plt.grid(True)
        plt.show()
    elif len(X.columns) == 3:
        fig = plt.figure(figsize=(8, 4))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(X.iloc[:, 0], X.iloc[:, 1], X.iloc[:, 2], c=kmeans.labels_, cmap='viridis', marker='o')
        ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], c='red', marker='x', s=100, label='Centroids')
        ax.set_title(f'KMeans Clustering with {best_cluster} clusters')
        ax.set_xlabel(X.columns[0])
        ax.set_ylabel(X.columns[1])
        ax.set_zlabel(X.columns[2])
        ax.legend()
        plt.grid(True)
        plt.show()

def get_best_clusters(X):
    """
    Perform clustering on the dataset X and plot silhouette scores for different cluster counts.
    """

    max_silhouette = -1
    silhouette_scores = []
    best_cluster = 0
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        score = silhouette_score(X, kmeans.labels_)
        silhouette_scores.append(score)
        if score > max_silhouette:
            max_silhouette = score
            best_cluster = k

    # Plot silhouette scores for each k
    plt.figure(figsize=(8, 4))
    plt.plot(range(2, 11), silhouette_scores, marker='o')
    plt.title('Silhouette Scores for Different k')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.xticks(range(2, 11))
    plt.grid(True)
    plt.show()

    # Fit KMeans with the best number of clusters
    kmeans = KMeans(n_clusters=best_cluster, random_state=42)
    kmeans.fit(X)

    radius = _calculate_radius(X, kmeans)

    labels_percetages = np.bincount(kmeans.labels_) / len(kmeans.labels_) * 100

    plot_clusters(X, kmeans, best_cluster)

    return Cluster_statistics(
        num_clusters=best_cluster,
        silhouette_score=max_silhouette,
        centroids=kmeans.cluster_centers_,
        radius=radius,
        labels_percetages=labels_percetages.tolist()
    )

def get_cluster_defined_number(X, num_clusters: int):
    """
    Perform clustering on the dataset X with a defined number of clusters.
    """

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)
    score = silhouette_score(X, kmeans.labels_)

    radius = _calculate_radius(X, kmeans)

    labels_percetages = np.bincount(kmeans.labels_) / len(kmeans.labels_) * 100

    plot_clusters(X, kmeans, num_clusters)

    return Cluster_statistics(
        num_clusters=num_clusters,
        silhouette_score=score,
        centroids=kmeans.cluster_centers_,
        radius=radius,
        labels_percetages=labels_percetages
    )

def compare_clusters(cluster_stats1: Cluster_statistics, cluster_stats2: Cluster_statistics, delta: float = 0.1):
    """
    Compare two cluster statistics objects and visualize the differences.
    """

    return ClusterChanges(original=cluster_stats1, new_data=cluster_stats2, delta=delta)

def clustering_evolution(dfs: list[pd.DataFrame], num_clusters: int):
    """
    Compares the evolution of clustering across multiple DataFrames.
    """

    cluster_stats = []
    for i, df in enumerate(dfs):
        stats = get_cluster_defined_number(df, num_clusters)
        if i!=0:
            stats = ClusterChanges.reorder_changes(cluster_stats[0], stats)
        cluster_stats.append(stats)

    plt.figure(figsize=(10, 6* (1 + num_clusters)))
    plt.suptitle("Evolution of Clustering")

    for i, (title, values, ylabel) in enumerate([
        ('Silhouette Score Evolution', [cs.silhouette_score for cs in cluster_stats], 'Silhouette Score')
    ]):
        plt.subplot(2*(1+num_clusters), 2, i+1)
        plt.plot(values, marker='o', linestyle='-', label=title)
        plt.title(title)
        plt.xlabel('Index')
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.tight_layout(pad=2.0)

    for cluster_idx in range(num_clusters):
        ax = plt.subplot(2*(1+num_clusters), 2, cluster_idx + 3)
        ax.set_title(f"Cluster {cluster_idx + 1}")
        # Gather radius and label percentage values for this cluster across all time steps
        radius_evolution = [cs.radius[cluster_idx] for cs in cluster_stats]
        percentage_evolution = [cs.labels_percetages[cluster_idx] for cs in cluster_stats]
        ax.plot(range(len(cluster_stats)), radius_evolution, marker='o', label='Radius')
        ax.set_xlabel("Index")
        ax.set_ylabel("Radius")
        ax.legend(loc='upper left')
        ax.grid(True)
        ax2 = ax.twinx()
        ax2.plot(range(len(cluster_stats)), percentage_evolution, marker='x', color='red', linestyle='--', label='Label %')
        ax2.set_ylabel("Label Percentage")
        ax2.legend(loc='upper right')

    plt.tight_layout(pad=2.0)
    plt.show()

    # Visualize the evolution of clustering
    for i in range(1, len(cluster_stats)):
        compare_clusters(cluster_stats[i - 1], cluster_stats[i])