"""Implementation of WaveNet."""
from ..bases import DynEmbedBase, ModelMeta
from ..layers import conv_nn, embedding_lookup, max_pool, normalize_embeds, tf_dense
from ..tfops import dropout_config, reg_config, tf
from ..utils.misc import count_params


class WaveNet(DynEmbedBase, metaclass=ModelMeta, backend="tensorflow"):
    """*WaveNet* algorithm.

    Parameters
    ----------
    task : {'rating', 'ranking'}
        Recommendation task. See :ref:`Task`.
    data_info : :class:`~libreco.data.DataInfo` object
        Object that contains useful information for training and inference.
    loss_type : {'cross_entropy', 'focal'}, default: 'cross_entropy'
        Loss for model training.
    embed_size: int, default: 16
        Vector size of embeddings.
    norm_embed : bool, default: False
        Whether to l2 normalize output embeddings.
    n_epochs: int, default: 10
        Number of epochs for training.
    lr : float, default 0.001
        Learning rate for training.
    lr_decay : bool, default: False
        Whether to use learning rate decay.
    epsilon : float, default: 1e-5
        A small constant added to the denominator to improve numerical stability in
        Adam optimizer.
        According to the `official comment <https://github.com/tensorflow/tensorflow/blob/v1.15.0/tensorflow/python/training/adam.py#L64>`_,
        default value of `1e-8` for `epsilon` is generally not good, so here we choose `1e-5`.
        Users can try tuning this hyperparameter if the training is unstable.
    reg : float or None, default: None
        Regularization parameter, must be non-negative or None.
    batch_size : int, default: 256
        Batch size for training.
    sampler : {'random', 'unconsumed', 'popular'}, default: 'random'
        Negative sampling strategy.

        - ``'random'`` means random sampling.
        - ``'unconsumed'`` samples items that the target user did not consume before.
        - ``'popular'`` has a higher probability to sample popular items as negative samples.

        .. versionadded:: 1.1.0

    num_neg : int, default: 1
        Number of negative samples for each positive sample, only used in `ranking` task.
    use_bn : bool, default: True
        Whether to use batch normalization.
    dropout_rate : float or None, default: None
        Probability of an element to be zeroed. If it is None, dropout is not used.
    n_filters : int, default: 16
        Number of output filters in each CNN layer.
    n_blocks : int, default: 1
        Number of CNN blocks.
    n_layers_per_block : int, default: 4
        Number of CNN layers in each block.
    recent_num : int or None, default: 10
        Number of recent items to use in user behavior sequence.
    random_num : int or None, default: None
        Number of random sampled items to use in user behavior sequence.
        If `recent_num` is not None, `random_num` is not considered.
    seed : int, default: 42
        Random seed.
    lower_upper_bound : tuple or None, default: None
        Lower and upper score bound for `rating` task.
    tf_sess_config : dict or None, default: None
        Optional TensorFlow session config, see `ConfigProto options
        <https://github.com/tensorflow/tensorflow/blob/v2.10.0/tensorflow/core/protobuf/config.proto#L431>`_.

    References
    ----------
    *Aaron van den Oord et al.* `WaveNet: A Generative Model for Raw Audio
    <https://arxiv.org/pdf/1609.03499.pdf>`_.
    """

    user_variables = ("embedding/user_embeds_var",)
    item_variables = (
        "embedding/item_embeds_var",
        "embedding/item_bias_var",
        "embedding/seq_embeds_var",
    )

    def __init__(
        self,
        task,
        data_info=None,
        loss_type="cross_entropy",
        embed_size=16,
        norm_embed=False,
        n_epochs=20,
        lr=0.001,
        lr_decay=False,
        epsilon=1e-5,
        reg=None,
        batch_size=256,
        sampler="random",
        num_neg=1,
        dropout_rate=None,
        use_bn=False,
        n_filters=16,
        n_blocks=1,
        n_layers_per_block=4,
        recent_num=10,
        random_num=None,
        seed=42,
        lower_upper_bound=None,
        tf_sess_config=None,
    ):
        super().__init__(
            task,
            data_info,
            embed_size,
            norm_embed,
            recent_num,
            random_num,
            lower_upper_bound,
            tf_sess_config,
        )
        self.all_args = locals()
        self.loss_type = loss_type
        self.n_epochs = n_epochs
        self.lr = lr
        self.lr_decay = lr_decay
        self.epsilon = epsilon
        self.reg = reg_config(reg)
        self.batch_size = batch_size
        self.sampler = sampler
        self.num_neg = num_neg
        self.dropout_rate = dropout_config(dropout_rate)
        self.use_bn = use_bn
        self.n_filters = n_filters
        self.n_blocks = n_blocks
        self.n_layers_per_block = n_layers_per_block
        self.seed = seed

    def build_model(self):
        tf.set_random_seed(self.seed)
        self._build_placeholders()
        self._build_variables()
        self.user_embeds = self._build_user_embeddings()

        user_embeds = self.user_embeds
        item_embeds = tf.nn.embedding_lookup(self.item_embeds, self.item_indices)
        item_biases = tf.nn.embedding_lookup(self.item_biases, self.item_indices)
        if self.norm_embed:
            user_embeds, item_embeds = normalize_embeds(
                user_embeds, item_embeds, backend="tf"
            )
        self.output = tf.reduce_sum(user_embeds * item_embeds, axis=1) + item_biases
        self.serving_topk = self.build_topk()
        count_params()

    def _build_placeholders(self):
        self.user_indices = tf.placeholder(tf.int32, shape=[None])
        self.item_indices = tf.placeholder(tf.int32, shape=[None])
        self.user_interacted_seq = tf.placeholder(
            tf.int32, shape=[None, self.max_seq_len]
        )
        self.user_interacted_len = tf.placeholder(tf.int32, shape=[None])
        self.labels = tf.placeholder(tf.float32, shape=[None])
        self.is_training = tf.placeholder_with_default(False, shape=[])

    def _build_variables(self):
        with tf.variable_scope("embedding"):
            # weight and bias parameters for last fc_layer
            self.item_embeds = tf.get_variable(
                name="item_embeds_var",
                shape=(self.n_items, self.embed_size * 2),
                initializer=tf.glorot_uniform_initializer(),
                regularizer=self.reg,
            )
            self.item_biases = tf.get_variable(
                name="item_bias_var",
                shape=[self.n_items],
                initializer=tf.zeros_initializer(),
            )

    def _build_user_embeddings(self):
        user_repr = embedding_lookup(
            indices=self.user_indices,
            var_name="user_embeds_var",
            var_shape=(self.n_users + 1, self.embed_size),
            initializer=tf.glorot_uniform_initializer(),
            regularizer=self.reg,
        )
        # B * seq * K
        seq_item_embed = embedding_lookup(
            indices=self.user_interacted_seq,
            var_name="seq_embeds_var",
            var_shape=(self.n_items + 1, self.embed_size),
            initializer=tf.glorot_uniform_initializer(),
            regularizer=self.reg,
        )

        convs_out = seq_item_embed
        for _ in range(self.n_blocks):
            for i in range(self.n_layers_per_block):
                convs_out = conv_nn(
                    filters=self.n_filters,
                    kernel_size=2,
                    strides=1,
                    padding="causal",
                    activation=tf.nn.relu,
                    dilation_rate=2**i,
                )(inputs=convs_out)

        convs_out = conv_nn(
            filters=self.n_filters,
            kernel_size=1,
            strides=1,
            padding="valid",
            activation=tf.nn.relu,
        )(inputs=convs_out)

        p_size = convs_out.get_shape().as_list()[1]
        convs_out = max_pool(pool_size=p_size, strides=1, padding="valid")(convs_out)
        convs_out = tf.squeeze(convs_out, axis=1)
        convs_out = tf_dense(units=self.embed_size, activation=None)(convs_out)
        return tf.concat([user_repr, convs_out], axis=1)
