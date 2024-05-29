from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

CMC_API_KEY = 'Your CMC_API_KEY' #this should cointain the api key given by coin market cap after registration

@app.route('/coin-listing', methods=['GET'])
def coin(CMC_API_KEY= CMC_API_KEY, limit="choose your limit", convert="specify your currency"):
    
    """_summary_
    This is an api endpoint that makes request and pass jsonified data to the to the html
    page. Note data varies depending on values passed to arguments in the function
    Returns:
        _type_: _description_
        CMC_API_KEY: this is like a password that coin market cap gives a user after joining
                     the platform it allows the view function to fetch data.
        limit: this is an argument that dictates the volume of data being pushed
        convert: well this specifies the currency to display values in
        
        try changing the values for the arguments should be fun 
    """
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    params = {
        'start': 1,
        'limit': limit,
        'convert': convert
    }
    
    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200: # this confirms if the operation was susccessful
        response_data = response.json() #data is now pulled in a json format i.e similar to python dictionary
        coins_data = response_data['data']
        
        # Retrieving necessary data there are more data values in the raw data like percentage change per hour
        # You can try printing the response_data to see the kind of data you have
        
        coins = []
        for coin in coins_data:
            coins.append({
                'symbol': coin['symbol'],
                'name': coin['name'],
                'quote': {
                    'USD': {
                        'price': coin['quote']['USD']['price']
                    }
                }
            })
        
        return jsonify(coins)  # return the coins data as JSON
    else:
        return jsonify({'error': 'Failed to fetch data'}) # error message as json

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
