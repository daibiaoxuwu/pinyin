import tensorflow as tf
import numpy as np

PAD = 0
EOS = 1
vocab_size = 672
output_size= 114
input_embedding_size = 1000
encoder_hidden_units = 20
decoder_hidden_units = 20
batch_size = 1



from pyreadertest import reader
model=reader()


train_graph = tf.Graph()
with train_graph.as_default():
    encoder_inputs = tf.placeholder(shape=(None, None), dtype=tf.int32, name='encoder_inputs')

    embeddings = tf.Variable(tf.random_uniform([vocab_size, input_embedding_size], -1.0, 1.0), dtype=tf.float32)
    encoder_inputs_embedded = tf.nn.embedding_lookup(embeddings, encoder_inputs)

    encoder_cell = tf.contrib.rnn.LSTMCell(encoder_hidden_units)
    encoder_outputs, encoder_final_state = tf.nn.dynamic_rnn(
        encoder_cell, encoder_inputs_embedded,
        dtype=tf.float32, time_major=False,
    )
     decoder_outputs, decoder_final_state=tf.contrib.seq2seq(encoder_inputs=encoder_inputs, #[T， batch_size]
                                decoder_inputs=decoder_inputs, #[out_T， batch_size]
                                cell,
                                num_encoder_symbols,
                                num_decoder_symbols,
                                embedding_size,
                                num_heads=1, #只采用一个read head
                                output_projection=None,
                                feed_previous=False,
                                dtype=None,
                                scope=None,
                                initial_state_attention=False):
    decoder_cell = tf.contrib.rnn.LSTMCell(decoder_hidden_units)
    decoder_outputs, decoder_final_state = tf.nn.dynamic_rnn(
        decoder_cell, 
        initial_state=encoder_final_state,
        dtype=tf.float32, time_major=False, scope="plain_decoder",
    )

    decoder_logits = tf.contrib.layers.linear(decoder_outputs, vocab_size)
    decoder_prediction = tf.argmax(decoder_logits, 2)
    saver=tf.train.Saver()

loss_track = []
epochs = 3001


voicedict={}
rvdict={}
with open('../拼音汉字表.txt',encoding='gbk') as f:
    a=f.readline()#.encode('gbk')
    while(a!=''):
        b=a.split()
        rvdict[b[0]]=b[1:]
        for c in b[1:]:
            voicedict[c]=b[0]
        a=f.readline()
with open('../input.txt') as f:
    sentence=f.readline()[:-1]
with tf.Session(graph=train_graph) as sess:
    sess.run(tf.global_variables_initializer())
    ckpt = tf.train.get_checkpoint_state('tense/py')
    saver.restore(sess, ckpt.model_checkpoint_path)
    answers,pads,inputs = model.list_tags(sentence)
    sentence=sentence.split()

    decoder_targets_ = [(sequence) + [EOS] for sequence in answers]
    decoder_inputs_ = [[EOS] + (sequence) for sequence in answers]
    feed_dict = {encoder_inputs: inputs}
    predict_ = sess.run(decoder_prediction, feed_dict)
    for i, (inp, pred) in enumerate(zip(np.array(feed_dict[encoder_inputs]).T, predict_.T)):
        areal=[]
        for num in range(len(pred)):
            if pred[num]<2:
                break
            areal.append(rvdict[sentence[num]][pred[num]-2])
        print('predicted > {}'.format(areal))

