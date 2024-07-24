from sklearn.cluster import KMeans

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}


    def get_clustering_model(self, image):
        # reshape image into 2D array
        image_2d = image.reshape(-1, 3) 

        # perform k-means clustering with two clusters
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(image_2d)

        return kmeans


    def get_player_color(self, frame, bbox):
        # crop bbox from frame
        image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        top_half_image = image[0: int(image.shape[0]/2), :]

        # get clustering model
        kmeans = self.get_clustering_model(top_half_image)

        # get cluster labels
        labels = kmeans.labels_

        # reshape labels into original image shape
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])

        # get clusters from coners, custer that apear the most is background
        corner_clusters = [clustered_image[0,0], clustered_image[0,-1], clustered_image[-1,0], clustered_image[-1,-1]]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)

        # get player cluster
        player_cluster = 1 - non_player_cluster   

        # get player color
        player_color = kmeans.cluster_centers_[player_cluster]  

        return player_color   


    def assign_team_color(self, frame, player_detections):
        # get player colors
        player_colors = []
        for _, player_detection in player_detections.items():
            bbox = player_detection['bbox']
            player_color = self.get_player_color(frame, bbox)
            player_colors.append(player_color)

        # divide colors into white and green
        kmeans = KMeans(n_clusters=2, init="k-means++", n_init=1)
        kmeans.fit(player_colors)

        self.kmeans = kmeans

        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]


    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id] 
        
        player_color = self.get_player_color(frame, player_bbox)

        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        team_id += 1

        self.player_team_dict[player_id] = team_id

        return team_id 