from flask import Flask, render_template, jsonify, Response, request, redirect, url_for
import os
import sqlite3
import shutil
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

# Function to copy history file
def copy_history_file(source_path, dest_path):
    shutil.copy2(source_path, dest_path)

def read_chrome_history():
    history_file_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    temp_history_file_path = 'temp_history_chrome'
    copy_history_file(history_file_path, temp_history_file_path)

    connection = sqlite3.connect(temp_history_file_path)
    cursor = connection.cursor()
    cursor.execute("SELECT url, visit_count FROM urls")
    history = cursor.fetchall()
    connection.close()

    # Remove the temporary history file after use
    os.remove(temp_history_file_path)

    return history

def read_ie_history():
    # Temporarily unavailable yet
    pass

def read_firefox_history():
    # ATemporarily unavailable yet
    pass

def generate_browser_history_graph(history_data):
    sorted_history = sorted(history_data, key=lambda x: x[1], reverse=True)
    top_10_history = sorted_history[:10]
    
    urls = [row[0] for row in top_10_history]
    visit_counts = [row[1] for row in top_10_history]

    plt.figure(figsize=(10, 6))
    plt.barh(urls, visit_counts, color='skyblue')
    plt.xlabel('Visit Counts')
    plt.ylabel('URL')
    plt.title('Top 10 Visited URLs')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/graph_html', methods=['GET', 'POST']) 
def graph_html():
    return render_template('browser_history_graph.html')

@app.route('/get_browser_history', methods=['POST'])
def get_browser_history():
    browser = request.form['browser']
    if browser == 'chrome':
        history_data = read_chrome_history()
    elif browser == 'ie':
        history_data = read_ie_history()
    elif browser == 'firefox':
        history_data = read_firefox_history()
    else:
        return jsonify({'error': 'Invalid browser selection'})

    browser_history = [{'url': row[0], 'visits': row[1]} for row in history_data]
    return jsonify(browser_history)

@app.route('/browser_history_graph', methods=['GET', 'POST'])
def browser_history_graph():
    if request.method == 'POST':
        browser = request.form['browser']
    elif request.method == 'GET':
        browser = request.args.get('browser')
    else:
        return jsonify({'error': 'Unsupported HTTP method'})

    if browser == 'chrome':
        history_data = read_chrome_history()
    elif browser == 'ie':
        history_data = read_ie_history()
    elif browser == 'firefox':
        history_data = read_firefox_history()
    else:
        return jsonify({'error': 'Invalid browser selection'})

    if not history_data:
        return jsonify({'error': 'No history data found'})

    try:
        buffer = generate_browser_history_graph(history_data)
        return Response(buffer, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/return_to_main')
def return_to_main():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
