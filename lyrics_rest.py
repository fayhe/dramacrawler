# coding=utf-8
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, render_template, request
import json

app = Flask(__name__)

def load_data(fname):
    with open(fname, 'r') as f:
        text = f.read()
    
    data = text.split()
    return data

def load_keyword_data(fname):
    with open(fname, 'r') as f:
        text = f.read()
    
    data = text.split(',')
    return data



def get_tensors(loaded_graph):

    inputs = loaded_graph.get_tensor_by_name('inputs:0')
    initial_state = loaded_graph.get_tensor_by_name('initial_state:0')
    final_state = loaded_graph.get_tensor_by_name('final_state:0')
    probs = loaded_graph.get_tensor_by_name('probs:0')
    return inputs, initial_state, final_state, probs

def pick_word(probabilities, int_to_vocab):
    '''
    选择单词进行文本生成，用来以一定的概率生成下一个词
    
    参数
    ---
    probabilities: Probabilites of the next word
    int_to_vocab: 映射表
    '''
    
    result = np.random.choice(len(probabilities), 50, p=probabilities)
    return int_to_vocab[result[0]]    

gen_length = 300
seq_length = 20

text = load_data('raw_data/lyrics.txt')
vocab = set(text)
vocab_to_int = {w: idx for idx, w in enumerate(vocab)}
int_to_vocab = {idx: w for idx, w in enumerate(vocab)}

#print len(text)
#print text[:10]

loaded_graph = tf.Graph()
with tf.Session(graph=loaded_graph) as sess:
	loader = tf.train.import_meta_graph('./model/save' + '.meta')
	loader.restore(sess, './model/save')
	input_text, initial_state, final_state, probs = get_tensors(loaded_graph)


@app.route("/write_lyrics", methods = ['POST'])
def write_lyrics():
	prime_word =  request.json.get('word').encode('utf-8')
	#print prime_word
	loaded_graph = tf.Graph()
	with tf.Session(graph=loaded_graph) as sess:
		loader = tf.train.import_meta_graph('./model/save' + '.meta')
		loader.restore(sess, './model/save')
		input_text, initial_state, final_state, probs = get_tensors(loaded_graph)


		gen_sentences = [prime_word]
		prev_state = sess.run(initial_state, {input_text: np.array([[1]])})

    # 生成句子
		for n in range(gen_length):
			dyn_input = [[vocab_to_int[word] for word in gen_sentences[-seq_length:]]]
			dyn_seq_length = len(dyn_input[0])

        # 预测
			probabilities, prev_state = sess.run(
            [probs, final_state],
            {input_text: dyn_input, initial_state: prev_state})
        
			pred_word = pick_word(probabilities[dyn_seq_length-1], int_to_vocab)

			gen_sentences.append(pred_word)

		#print(gen_sentences);    
		lyrics = ' '.join(gen_sentences)
		lyrics = lyrics.replace(';', '\n')
		lyrics = lyrics.replace('.', ' ')
		lyrics = lyrics.replace(' ', '')
        
		print(lyrics)
       
	return json.dumps({'success':True,'lyrics': lyrics }), 200, {'ContentType':'application/json'} 


@app.route('/')
def main():
    keywords = load_keyword_data('raw_data/lyrics_5000_keywords.txt')
    keywords = [keyword.decode('utf-8') for keyword in keywords]
    print keywords
    return render_template('lyrics_generator.html',toPass=keywords)


if __name__ == '__main__':
    app.run(host='0.0.0.0')