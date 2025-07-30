import inspect
import json
import os

import numpy as np
import torch

from ..tfops import tf


def save_params(model, path, model_name):
    hparams = dict()
    arg_names = list(inspect.signature(model.__init__).parameters.keys())
    if "data_info" in arg_names:
        arg_names.remove("data_info")
    if "device" in arg_names:
        arg_names.remove("device")
    for p in arg_names:
        hparams[p] = model.all_args[p]

    param_path = os.path.join(path, f"{model_name}_hyper_parameters.json")
    with open(param_path, "w") as f:
        json.dump(hparams, f, separators=(",", ":"), indent=4)


def load_params(path, data_info, model_name):
    if not os.path.exists(path):
        raise OSError(f"file folder {path} doesn't exists...")

    param_path = os.path.join(path, f"{model_name}_hyper_parameters.json")
    with open(param_path, "r") as f:
        hparams = json.load(f)
    hparams["data_info"] = data_info
    # if "with_training" in inspect.signature(model_class.__init__).parameters.keys():
    #    hparams.update({"with_training": False})
    return hparams


def save_default_recs(model, path, model_name):
    rec_path = os.path.join(path, f"{model_name}_default_recs")
    if model.default_recs is not None:
        np.savez_compressed(rec_path, default_recs=model.default_recs)


def load_default_recs(path, model_name):
    rec_path = os.path.join(path, f"{model_name}_default_recs.npz")
    if os.path.exists(rec_path):
        return np.load(rec_path)["default_recs"]


def save_tf_model(sess, path, model_name):
    model_path = os.path.join(path, f"{model_name}_tf")
    saver = tf.train.Saver()
    saver.save(sess, model_path, write_meta_graph=True)


def load_tf_model(model_class, path, model_name, data_info):
    model_path = os.path.join(path, f"{model_name}_tf")
    hparams = load_params(path, data_info, model_name)
    model = model_class(**hparams)  # model_class.__class__(**hparams)
    model.build_model()
    model.loaded = True
    model.default_recs = load_default_recs(path, model_name)
    # saver = tf.train.import_meta_graph(os.path.join(path, model_name + ".meta"))
    saver = tf.train.Saver()
    saver.restore(model.sess, model_path)
    return model


def save_tf_variables(sess, path, model_name, inference_only):
    variable_path = os.path.join(path, f"{model_name}_tf_variables")
    variables = dict()
    for v in tf.global_variables():
        if inference_only:
            # also save moving_mean and moving_var for batch_normalization
            if v in tf.trainable_variables() or "moving" in v.name:
                variables[v.name] = sess.run(v)
        else:
            variables[v.name] = sess.run(v)
    np.savez_compressed(variable_path, **variables)


def load_tf_variables(model_class, path, model_name, data_info):
    variable_path = os.path.join(path, f"{model_name}_tf_variables.npz")
    variables = np.load(variable_path)
    hparams = load_params(path, data_info, model_name)
    model = model_class(**hparams)
    model.build_model()
    model.loaded = True
    model.default_recs = load_default_recs(path, model_name)
    update_ops = []
    for v in tf.global_variables():
        # also load moving_mean and moving_var for batch_normalization
        if v in tf.trainable_variables() or "moving" in v.name:
            update_ops.append(v.assign(variables[v.name]))
        # v.load(variables[v.name], session=model.sess)
    model.sess.run(update_ops)
    return model


def save_torch_state_dict(model, path, model_name):
    save_path = os.path.join(path, f"{model_name}_torch.pt")
    torch.save(
        {
            "model_state_dict": model.torch_model.state_dict(),
            "optimizer_state_dict": model.trainer.optimizer.state_dict(),
        },
        save_path,
    )


def load_torch_state_dict(path, model_name, device):
    load_path = os.path.join(path, f"{model_name}_torch.pt")
    state = torch.load(load_path, map_location=device)
    return state["model_state_dict"], state["optimizer_state_dict"]
