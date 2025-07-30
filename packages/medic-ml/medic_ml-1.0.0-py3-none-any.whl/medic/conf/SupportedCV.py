from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

CV_ALGORITHMS = {
    "GridSearchCV": {
        "constructor": GridSearchCV,
        "params": []
    }, 
    "RandomizedSearchCV": {
        "constructor": RandomizedSearchCV,
        "params": [{
            "name": "n_iter", 
            "value": 10, 
            "type": "int", 
            "constant": False
        }]
    }
}
