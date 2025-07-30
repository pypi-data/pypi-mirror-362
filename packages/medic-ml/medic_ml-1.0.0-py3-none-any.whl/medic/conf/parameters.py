# Number of features to compute PCA, UMAP and Strip charts
features = [5, 10, 40, 100]

# Default marks for sliders
default_marks = {str(k): str(v) for k, v in enumerate(features)}

# Mark for the all value
all_mark = {str(len(features)): "All"}

# Offset when showing the used value
custom_mark_offset = 0.3

# Limit of used features to plot (used for strip charts)
max_used_features_to_show = 200