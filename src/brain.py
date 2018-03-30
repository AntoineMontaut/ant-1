import numpy as np
import tensorflow as tf

import keras.models as models
import keras.layers as layers
from keras import backend as K
from src.config_ants import *

class Brain():

    def __init__(self):
        self.train_queue = [[], [], [], []] # s, a, r, s' (terminal mask)
        self.session = tf.Session()
        K.set_session(self.session)
        K.manual_variable_initialization(True)

        self.model = self._build_model()
        self.graph = self._build_graph(self.model)

        self.session.run(tf.global_variables_initializer())
        self.default_graph = tf.get_default_graph()

        self.default_graph.finalize()

    def _build_model(self):
        l_input = layers.Input(batch_shape=(None, NUM_STATE))
        l_dense_1 = layers.Dense(64, activation='relu')(l_input)
        l_dense_2 = layers.Dense(32, activation='relu')(l_dense_1)
        l_dense_3 = layers.Dense(16, activation='relu')(l_dense_2)

        out_actions = layers.Dense(NUM_ACTIONS, activation='softmax')(l_dense_3)
        out_value = layers.Dense(1, activation='linear')(l_dense_3)

        model = models.Model(inputs=[l_input], output=[out_actions, out_value])
        model._make_predict_function()

        return model

    def _build_graph(self, model):
        s_t = tf.placeholder(tf.float32, shape=(None, NUM_STATE))
        a_t = tf.placeholder(tf.float32, shape=(None, NUM_ACTIONS))
        r_t = tf.placeholder(tf.float32, shape=(None, 1))

        p, v = model(s_t)

        log_prob = tf.log(tf.reduce_sum(p * a_t, axis=1, keep_dims=True) + 1e-10)
        advantage = r_t - v

        loss_policy = - log_prob * tf.stop_gradient(advantage)
        loss_value = LOSS_V * tf.square(advantage)
        entropy = LOSS_ENTROPY * tf.reduce_sum(p * tf.log(p + 1e-10), axis=1, keep_dims=True)

        loss_total = tf.reduce_mean(loss_policy + loss_value + entropy)

        optimizer = tf.train.RMSPropOptimizer(LEARNING_RATE, decay=RMS_DECAY)
        minimize = optimizer.minimize(loss_total)

        return s_t, a_t, r_t, minimize

    def optimize(self):
        s, a, r, s_ = self.train_queue
        self.train_queue = [[], [], [], []]

        s = np.vstack(s)
        a = np.vstack(a)
        r = np.vstack(r)
        s_ = np.vstack(s_)

        v = self.predict_v(s_)
        r = r + GAMMA_N * v

        s_t, a_t, r_t, minimize = self.graph
        self.session.run(minimize, feed_dict={s_t: s, a_t: a, r_t: r})

    def train_push(self, s, a, r, s_):
        self.train_queue[0].append(s)
        self.train_queue[1].append(a)
        self.train_queue[2].append(r)
        self.train_queue[3].append(s_)

    def predict(self, s):
        with self.default_graph.as_default():
            p, v = self.model.predict(s)
            return p, v

    def predict_p(self, s):
        with self.default_graph.as_default():
            p, v = self.model.predict(s)
            return p

    def predict_v(self, s):
        with self.default_graph.as_default():
            p, v = self.model.predict(s)
            return v
