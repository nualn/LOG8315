from flask import Flask

app = Flask(__name__)

@app.route('/overall_app')
def overall_app():
    return 'Overall app !'


@app.route('/cluster1')
def cluster1_app():
    return 'Cluster 1 is running successfully !'

@app.route('/cluster2')
def cluster2_app():
    return 'Cluster 2 is running successfully !'

if __name__=="__main__":
    app.run(debug=True)
