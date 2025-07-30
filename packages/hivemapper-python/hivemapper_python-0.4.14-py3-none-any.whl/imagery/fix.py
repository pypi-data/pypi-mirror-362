import argparse
import concurrent.futures
import json
import os

from exiftool import ExifToolHelper

def update_exif(local_path, metadata):
  tags = {}

  if 'camera' in metadata:
    cam = metadata.get('camera', {})
    focal = cam.get('focal', 0.0)
    k1 = cam.get('k1', 0.0)
    k2 = cam.get('k2', 0.0)
    tags['FocalLength'] = focal
    tags['Lens'] = f'{k1} {k2}'

  if len(tags) == 0:
    return

  print(f'Writing {len(tags)} tags to {local_path}:')
  # pirnt(tags)
  with ExifToolHelper() as et:
    et.set_tags(
      [local_path],
      tags=tags,
      params=['-overwrite_original']
    )

def main(dir_):
  executor = concurrent.futures.ThreadPoolExecutor(max_workers=25)
  futures = []

  contents = os.listdir(dir_)
  folders = [x for x in contents if x.startswith('out')]
  for folder in folders:
    colls = os.listdir(os.path.join(dir_, folder))
    for coll in colls:
      if '.geojson' in coll:
        continue
      metapath = os.path.join(dir_, folder, coll, 'meta.json')
      with open(metapath, 'r') as f:
        meta = json.load(f)
        for k, v in meta.items():
          local_path = os.path.join(dir_, folder, coll, k)
          futures.append(executor.submit(update_exif, local_path, v))

  for future in concurrent.futures.as_completed(futures):
    try:
      results = future.result()
    except Exception as e:
      print(e)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', type=str, required=True)

  args = parser.parse_args()

  main(args.input_file)
