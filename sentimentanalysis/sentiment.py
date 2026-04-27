from flask import Flask, request, jsonify

app = Flask(__name__)

def analyze_sentiment(text):
    positive_words = ['fantastic', 'great', 'excellent', 'amazing', 'wonderful', 
                      'good', 'best', 'awesome', 'outstanding', 'superb', 'happy',
                      'love', 'perfect', 'brilliant', 'satisfied']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'worst', 'poor', 
                      'disappointed', 'unhappy', 'dissatisfied', 'rude', 'slow']
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

@app.route('/analyze', methods=['GET'])
def analyze():
    text = request.args.get('text', '')
    sentiment = analyze_sentiment(text)
    return jsonify({"sentiment": sentiment, "text": text})

if __name__ == '__main__':
    app.run(port=5000)