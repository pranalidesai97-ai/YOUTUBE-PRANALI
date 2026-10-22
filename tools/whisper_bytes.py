#!/usr/bin/env python3
"""Greedy Whisper decoding of sherpa-onnx exported models with correct UTF-8.

sherpa-onnx decodes every byte-level BPE token separately, which drops the
partial UTF-8 bytes of Devanagari characters. This decoder joins the raw token
bytes first, so Hindi comes out intact.

Usage: whisper_bytes.py MODEL_DIR PREFIX LANG AUDIO_16K_S16LE START END [START END ...]
Prints one line per span: start, end, mean token log-prob, text.
"""
import base64
import sys

import kaldi_native_fbank as knf
import numpy as np
import onnxruntime as ort


class Whisper:
    def __init__(self, model_dir, prefix):
        so = ort.SessionOptions()
        so.intra_op_num_threads = 4
        self.enc = ort.InferenceSession(f"{model_dir}/{prefix}-encoder.int8.onnx", so)
        self.dec = ort.InferenceSession(f"{model_dir}/{prefix}-decoder.int8.onnx", so)
        m = self.enc.get_modelmeta().custom_metadata_map
        self.n_mels = int(m["n_mels"])
        self.n_layer = int(m["n_text_layer"])
        self.n_ctx = int(m["n_text_ctx"])
        self.n_state = int(m["n_text_state"])
        self.sot_seq = [int(x) for x in m["sot_sequence"].split(",")]
        self.eot = int(m["eot"])
        self.blank = int(m["blank_id"])
        self.no_ts = int(m["no_timestamps"])
        self.lang = dict(zip(m["all_language_codes"].split(","),
                             [int(x) for x in m["all_language_tokens"].split(",")]))
        self.table = {}
        for line in open(f"{model_dir}/{prefix}-tokens.txt"):
            tok, idx = line.split()
            self.table[int(idx)] = base64.b64decode(tok)

    def mel(self, audio):
        opts = knf.WhisperFeatureOptions()
        opts.dim = self.n_mels
        fb = knf.OnlineWhisperFbank(opts)
        fb.accept_waveform(16000, audio)
        fb.input_finished()
        f = np.stack([fb.get_frame(i) for i in range(fb.num_frames_ready)])
        f = np.log10(np.clip(f, 1e-10, None))
        f = np.maximum(f, f.max() - 8.0)
        f = (f + 4.0) / 4.0
        f = np.pad(f, ((0, 1500), (0, 0)))
        if f.shape[0] > 3000:
            f = np.pad(f[:2950], ((0, 50), (0, 0)))
        return f.T[None].astype(np.float32)

    def suppress(self, logits, initial):
        logits[self.eot + 1:] = -np.inf
        if initial:
            logits[self.eot] = -np.inf
            logits[self.blank] = -np.inf
        return logits

    def transcribe(self, audio, lang):
        ck, cv = self.enc.run(None, {"mel": self.mel(audio)})
        seq = list(self.sot_seq)
        seq[1] = self.lang[lang]
        seq.append(self.no_ts)
        sk = np.zeros((self.n_layer, 1, self.n_ctx, self.n_state), np.float32)
        sv = np.zeros_like(sk)
        offset = np.zeros(1, np.int64)
        tokens = np.array([seq], np.int64)
        out, lps, initial = [], [], True
        # speech rarely exceeds ~8 tokens/s; cap it and stop on repetition loops
        max_tokens = min(self.n_ctx - len(seq), int(len(audio) / 16000 * 8) + 10)
        for _ in range(max_tokens):
            if len(out) >= 12 and out[-6:] == out[-12:-6]:
                out, lps = out[:-6], lps[:-6]
                break
            logits, sk, sv = self.dec.run(None, {"tokens": tokens, "in_n_layer_self_k_cache": sk,
                                                 "in_n_layer_self_v_cache": sv, "n_layer_cross_k": ck,
                                                 "n_layer_cross_v": cv, "offset": offset})
            offset += tokens.shape[1]
            lg = self.suppress(logits[0, -1].astype(np.float64), initial)
            initial = False
            t = int(np.argmax(lg))
            if t == self.eot:
                break
            lp = lg - (np.log(np.sum(np.exp(lg[np.isfinite(lg)] - lg[t]))) + lg[t])
            lps.append(float(lp[t]))
            out.append(t)
            tokens = np.array([[t]], np.int64)
        text = b"".join(self.table.get(t, b"") for t in out).decode("utf-8", errors="replace").strip()
        return text, (float(np.mean(lps)) if lps else 0.0)


def main():
    model_dir, prefix, lang, raw = sys.argv[1:5]
    spans = [float(x) for x in sys.argv[5:]]
    x = np.fromfile(raw, np.int16).astype(np.float32) / 32768
    w = Whisper(model_dir, prefix)
    for a, b in zip(spans[::2], spans[1::2]):
        text, lp = w.transcribe(x[int(a * 16000):int(b * 16000)], lang)
        print(f"{a:.2f}\t{b:.2f}\t{lp:.2f}\t{text}", flush=True)


if __name__ == "__main__":
    main()
