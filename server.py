from flask import Flask

app = Flask(__name__)

@app.route('/')
def overall_app():
    return f'Cluster {cluster_number} is running!'


# @app.route('/cluster1')
# def cluster1_app():
#     return 'Cluster 1 is running successfully !'

# @app.route('/cluster2')
# def cluster2_app():
#     return 'Cluster 2 is running successfully !'

if __name__=="__main__":
    app.run(host='0.0.0.0', port=80)
