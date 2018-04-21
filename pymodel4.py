
import numpy as np
import tensorflow as tf
import os
from pyreader4 import reader
model=reader()
os.environ["CUDA_VISIBLE_DEVICES"]=""#环境变量：使用第一块gpu


tf.reset_default_graph()


PAD = 0
EOS = 1
# UNK = 2
# GO  = 3

vocab_size = 672
input_embedding_size = 20

encoder_hidden_units = 20
decoder_hidden_units = encoder_hidden_units * 2

encoder_inputs = tf.placeholder(shape=(None, None), dtype=tf.int32, name='encoder_inputs')

encoder_inputs_length = tf.placeholder(shape=(None,), dtype=tf.int32, name='encoder_inputs_length')

decoder_targets = tf.placeholder(shape=(None, None), dtype=tf.int32, name='decoder_targets')

embeddings = tf.Variable(tf.truncated_normal([vocab_size, input_embedding_size], mean=0.0, stddev=0.1), dtype=tf.float32)

encoder_inputs_embedded = tf.nn.embedding_lookup(embeddings, encoder_inputs)


from tensorflow.contrib.rnn import LSTMCell, LSTMStateTuple

encoder_cell = LSTMCell(encoder_hidden_units)






((encoder_fw_outputs,
  encoder_bw_outputs),
 (encoder_fw_final_state,
  encoder_bw_final_state)) = (
    tf.nn.bidirectional_dynamic_rnn(cell_fw=encoder_cell,
                                    cell_bw=encoder_cell,
                                    inputs=encoder_inputs_embedded,
                                    sequence_length=encoder_inputs_length,
                                    dtype=tf.float32, time_major=True)
    )


encoder_outputs = tf.concat((encoder_fw_outputs, encoder_bw_outputs), 2)

encoder_final_state_c = tf.concat(
    (encoder_fw_final_state.c, encoder_bw_final_state.c), 1)

encoder_final_state_h = tf.concat(
    (encoder_fw_final_state.h, encoder_bw_final_state.h), 1)

encoder_final_state = LSTMStateTuple(
    c=encoder_final_state_c,
    h=encoder_final_state_h
)


decoder_cell = LSTMCell(decoder_hidden_units)

#encoder_max_time, batch_size = tf.unstack(tf.shape(encoder_inputs))
batch_size=100


decoder_lengths = encoder_inputs_length + 3


W = tf.Variable(tf.truncated_normal([decoder_hidden_units, vocab_size], 0, 0.1), dtype=tf.float32)
b = tf.Variable(tf.zeros([vocab_size]), dtype=tf.float32)

assert EOS == 1 and PAD == 0

eos_time_slice = tf.ones([batch_size], dtype=tf.int32, name='EOS')
pad_time_slice = tf.zeros([batch_size], dtype=tf.int32, name='PAD')

eos_step_embedded = tf.nn.embedding_lookup(embeddings, eos_time_slice)
pad_step_embedded = tf.nn.embedding_lookup(embeddings, pad_time_slice)


def loop_fn_initial():
    initial_elements_finished = (0 >= decoder_lengths)  # all False at the initial step
    initial_input = eos_step_embedded
    initial_cell_state = encoder_final_state
    initial_cell_output = None
    initial_loop_state = None  # we don't need to pass any additional information
    return (initial_elements_finished,
            initial_input,
            initial_cell_state,
            initial_cell_output,
            initial_loop_state)

# (time, previous_cell_output, previous_cell_state, previous_loop_state) -> 
#     (elements_finished, input, cell_state, output, loop_state).
def loop_fn_transition(time, previous_output, previous_state, previous_loop_state):

    def get_next_input():
        output_logits = tf.add(tf.matmul(previous_output, W), b) # projection layer
        # [batch_size, vocab_size]
        prediction = tf.argmax(output_logits, axis=1)
        next_input = tf.nn.embedding_lookup(embeddings, prediction)
        # [batch_size, input_embedding_size]
        return next_input
    
    elements_finished = (time >= decoder_lengths) # this operation produces boolean tensor of [batch_size]
                                                  # defining if corresponding sequence has ended

    finished = tf.reduce_all(elements_finished) # -> boolean scalar
    inputs = tf.cond(finished, lambda: pad_step_embedded, get_next_input)
    # input shape [batch_size,input_embedding_size]
    state = previous_state
    output = previous_output
    loop_state = None

    return (elements_finished, 
            inputs,
            state,
            output,
            loop_state)


def loop_fn(time, previous_output, previous_state, previous_loop_state):
    if previous_state is None:    # time == 0
        assert previous_output is None and previous_state is None
        return loop_fn_initial()
    else:
        return loop_fn_transition(time, previous_output, previous_state, previous_loop_state)

decoder_outputs_ta, decoder_final_state, _ = tf.nn.raw_rnn(decoder_cell, loop_fn)
decoder_outputs = decoder_outputs_ta.stack()

print('1')


decoder_max_steps, decoder_batch_size, decoder_dim = tf.unstack(tf.shape(decoder_outputs))
decoder_outputs_flat = tf.reshape(decoder_outputs, (-1, decoder_dim))
decoder_logits_flat = tf.add(tf.matmul(decoder_outputs_flat, W), b)
decoder_logits = tf.reshape(decoder_logits_flat, (decoder_max_steps, decoder_batch_size, vocab_size))

decoder_prediction = tf.argmax(decoder_logits, 2)


stepwise_cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
    labels=tf.one_hot(decoder_targets, depth=vocab_size, dtype=tf.float32),
    logits=decoder_logits,
)

loss = tf.reduce_mean(stepwise_cross_entropy)
train_op = tf.train.AdamOptimizer().minimize(loss)

def random_sequences(length_from, length_to, vocab_lower, vocab_upper, batch_size):
    def random_length():
        if length_from == length_to:
            return length_from
        return np.random.randint(length_from, length_to + 1)

    while True:
        yield [
            np.random.randint(low=vocab_lower, high=vocab_upper, size=random_length()).tolist()
            for _ in range(batch_size)
        ]
batches = random_sequences(length_from=3, length_to=8,
                                   vocab_lower=2, vocab_upper=10,
                                   batch_size=batch_size)
def make_batch(inputs, max_sequence_length=None):
    sequence_lengths = [len(seq) for seq in inputs]
    batch_size = len(inputs)
    if max_sequence_length is None:
        max_sequence_length = max(sequence_lengths)
    inputs_batch_major = np.zeros(shape=[batch_size, max_sequence_length], dtype=np.int32)
    for i, seq in enumerate(inputs):
        for j, element in enumerate(seq):
            inputs_batch_major[i, j] = element
    inputs_time_major = inputs_batch_major.swapaxes(0, 1)
    return inputs_time_major, sequence_lengths


def next_feed():
    answers,inputs = model.list_tags(batch_size=batch_size)
    encoder_inputs_, encoder_input_lengths_ = make_batch(inputs)
    decoder_targets_, _ = make_batch(
        [(sequence) + [EOS] + [PAD] * 2 for sequence in answers]
    )
  #  print('a',encoder_inputs_.shape)
  #  print('b',np.array(encoder_input_lengths_).shape)
  #  print('c',np.array(decoder_targets_).shape)
    return {
        encoder_inputs: encoder_inputs_,
        encoder_inputs_length: encoder_input_lengths_,
        decoder_targets: decoder_targets_,
    }
    '''
def next_feed():
    answers,inputs = model.list_tags(batch_size=batch_size)
    answers=np.array(answers).T.tolist()
    pads=np.array(pads).T.tolist()
    inputs=np.array(inputs).T.tolist()
    print('a',np.array(answers).shape)
    print('b',np.array(pads).shape)
    print('c',np.array(inputs).shape)
    print('a',type(answers[0]))
    print('b',type(pads[0]))
    print('c',type(inputs[0]))
    return {
        encoder_inputs: inputs,
        encoder_inputs_length: pads,
        decoder_targets: answers
    }
'''
saver=tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    #ckpt = tf.train.get_checkpoint_state('tense/py4')
    #saver.restore(sess, ckpt.model_checkpoint_path)


    print('head of the batch:')
    for seq in next(batches)[:10]:
        print(seq)


    loss_track = []
    max_batches = 300000001
    batches_in_epoch = 1000

    try:
        for batch in range(max_batches):
            fd = next_feed()
            _, l = sess.run([train_op, loss], fd)
            loss_track.append(l)

            if batch == 0 or batch % batches_in_epoch == 0:
                print('saved to: ', saver.save(sess,'tense/py4/py4.ckpt',global_step=batch))
                print('batch {}'.format(batch)+'  minibatch loss: {}'.format(sess.run(loss, fd)))
                predict_ = sess.run(decoder_prediction, fd)
                for i, (inp,ans, pred) in enumerate(zip(fd[encoder_inputs].T,fd[decoder_targets].T, predict_.T)):
                    print('  sample {}:'.format(i + 1))
                    print('    input     > {}'.format(inp))
                    print('    answer    > {}'.format(ans))
                    print('    predicted > {}'.format(pred))
                    if i >= 2:
                        break
                print()

    except KeyboardInterrupt:
        print('training interrupted')

    '''
    import matplotlib.pyplot as plt
    plt.plot(loss_track)
    print('loss {:.4f} after {} examples (batch_size={})'.format(loss_track[-1], len(loss_track)*batch_size, batch_size))
'''
