from django.shortcuts import render
from django.http import JsonResponse
import language_tool_python
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import word_tokenize, pos_tag, RegexpParser

# Function to check sentiment using NLTK SentimentIntensityAnalyzer
def check_sentiment(text):

    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(text)
    return sentiment_score


def count_grammar_mistakes(sentence):
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')

    tokens = word_tokenize(sentence)
    tagged_tokens = pos_tag(tokens)

    grammar_pattern = r"""
        NP: {<DT|JJ|NN.*>+}
        PP: {<IN><NP>}
        VP: {<MD>?<VB.*><NP|PP>*}
    """
    chunk_parser = RegexpParser(grammar_pattern)
    parsed_tree = chunk_parser.parse(tagged_tokens)

    num_mistakes = len([subtree for subtree in parsed_tree.subtrees() if subtree.label() != 'S'])

    return num_mistakes
# Create your views here.
def index(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')  
        sentiment_score = check_sentiment(text)
        num_mistakes = count_grammar_mistakes(text)

        # Sentiment Analysis
        sentiment_result = {
            'Positive': sentiment_score['pos'],
            'Neutral': sentiment_score['neu'],
            'Negative': sentiment_score['neg']
        }

        # Grammar Analysis
        total_words = len(word_tokenize(text))
        accuracy = ((total_words - num_mistakes) / total_words) * 100

        response_data = {
            'sentiment_result': sentiment_result,
            'total_words': total_words,
            'grammar_accuracy': accuracy
        }

        # Print statements
        print("\nSentiment Analysis:")
        for sentiment, score in sentiment_result.items():
            print(f"{sentiment}: {score:.2f}")
        
        print(f"Total words: {total_words}")
        print(f"Grammar accuracy: {accuracy:.2f}%")

        return JsonResponse(response_data)

    return render(request, 'index.html')
