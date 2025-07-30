import json
import os

from util import stitching

def read_seqs(root, manifest, verbose):
  contents = os.listdir(root)
  for content in contents:
    p = os.path.join(root, content)
    if os.path.isfile(p):
      continue

    seq_contents = os.listdir(p)
    jpgs = set([f for f in seq_contents if f.endswith('.jpg')])
    meta_path = os.path.join(p, 'meta.json')

    with open(meta_path, 'r') as f:
      meta = json.load(f)
      for img in meta.keys():
        if img in jpgs:
          d = meta[img]
          sid = f"{d['sequence']}/{d['idx']}.jpg"
          manifest[sid] = d
          manifest[sid]['loc'] = os.path.join(p, img)

def main(root, max_dist, max_lag, max_angle, verbose):
  manifest = {}
  read_seqs(root, manifest)

  frames = manifest.values()
  stitched = stitching.stitch(frames, max_dist, max_lag, max_angle, verbose)

  print(len(stitched))
