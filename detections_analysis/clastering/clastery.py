import os
from typing import Optional, List

import numpy as np
from skimage import draw
from sklearn.cluster import KMeans

from credo_cf import load_json, progress_load_filter, load_image, GRAY, ID, print_log, deserialize_or_run, store_png, deserialize, serialize, FRAME_CONTENT, \
    BaseProcedure, execute_chain, print_run_measurement, make_stack, SortedPreprocess, KMeansClassify

string = "Detections_analysis/clastering/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
OUTPUT_DIR=back_to_main_path+"data_save/detections_analysis/clastering/"

WORKING_SET = '/media/slawekstu/CREDO1/Api/paczki_michala/data_set/17.json'
STORE_GRAY_CLUSTER = False


html_head = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<style>
table, th, td {
  border: 1px black solid;
}
th, td {
  padding: 0.5em;
}
</style>
<body>
<table>
  <tr>
    <th>Cluster</th>
    <th>Count</th>
    <th>Sum</th>
    <th style="white-space: nowrap">Corona-like sums</th>
    <th>Sample images</th>
  </tr>
'''

html_foot = '''
</table>
</body>
</html>'''


def get_working_set_file(stage: int):
    return '%s/loaded-%02d.dat' % (OUTPUT_DIR, stage)


def get_kmeans_file(stage: int):
    return '%s/kmeans-%02d.dat' % (OUTPUT_DIR, stage)


def get_labels_file(stage: int):
    return '%s/labels-%02d.dat' % (OUTPUT_DIR, stage)


def load_data(fn: str):
    """
    Load data from prepared working set in JSON from ``fn`` file.
    For each image:
    1. Load from JSON
    2. Convert to grayscale
    :param fn: JSON file with
    :return: two tables in dict: ``id_array`` with hit ID's and `bitmap_array`` with array of gray bitmaps
    """
    id_array = []
    bitmap_array = []
    stored = {}

    def load_parser(obj: dict, count: int, ret: List[dict]) -> Optional[bool]:
        progress_load_filter(obj, count, ret)
        load_image(obj, False)
        st = '%03d' % ((count - 1) // 1000)
        stored[obj[ID]] = st
        store_png(OUTPUT_DIR, ['images', st], str(obj[ID]), obj[FRAME_CONTENT])

        id_array.append(obj[ID])
        bitmap_array.append([obj[GRAY]])

        return False

    load_json(fn, load_parser)

    return {
        'id_array': id_array,
        'bitmap_array': bitmap_array,
        'stored': stored
    }


def clustering(data: dict, chain: List[BaseProcedure]):
    # Stacking array of 2D bitmaps to 3D stack
    bitmap_array = data['bitmap_array']
    stacked = print_run_measurement('Start vstack', make_stack, bitmap_array)

    return print_run_measurement('Start clustering', execute_chain, chain, stacked)


def save_html_and_pngs_and_labels(stage: int, kmeans: KMeans, data: dict):
    sn = get_labels_file(stage)
    if os.path.exists(sn):
        return

    # Save PNG files in file system
    labels = {}
    images = {}
    for i in range(0, len(kmeans.labels_)):
        label = kmeans.labels_[i]
        _id = data['id_array'][i]
        image = data['bitmap_array'][i][0]

        if STORE_GRAY_CLUSTER:
            store_png(OUTPUT_DIR, ['%02d' % stage, '%03d' % label], str(_id), image)
        in_label = labels.get(label, [])
        in_label.append(_id)
        labels[label] = in_label

        in_image = images.get(label, [])
        in_image.append([image])
        images[label] = in_image

    # make normalized sum and corona sum
    corona_radius = [2, 4, 8, 16]

    for label, in_image in images.items():
        stacked = np.vstack(in_image)
        summed = np.sum(stacked, 0)

        m = np.amax(summed)
        image = summed * 255 / m
        store_png(OUTPUT_DIR, ['%02d' % stage], 'sum_%03d' % label, image.astype(np.uint8))

        # corona:
        for radius in corona_radius:
            rr, cc = draw.disk((30, 30), radius=radius, shape=summed.shape)
            summed[rr, cc] = 0

            m = np.amax(summed)
            image = summed * 255 / m
            store_png(OUTPUT_DIR, ['%02d' % stage], 'sum_corona_%03d_%d' % (label, radius), image.astype(np.uint8))

    # Save HTML for preview clusters
    max_files_per_cluster = 20
    with open('%s/%02d.html' % (OUTPUT_DIR, stage), 'wt') as html:
        html.write(html_head)
        for label in sorted(labels.keys()):
            html.write('  <tr><th>%d</th><th>%d</th>\n' % (label, len(labels[label])))
            html.write('<td><img src="%02d/sum_%03d.png"/></td><td>' % (stage, label))
            for radius in corona_radius:
                html.write('<img src="%02d/sum_corona_%03d_%d.png"/>' % (stage, label, radius))
            html.write('</td><td>')
            used = 0
            for _id in labels[label]:
                html.write('    <img src="images/%s/%s.png"/>\n' % (data['stored'][_id], str(_id)))
                used += 1
                if used >= max_files_per_cluster:
                    break
            html.write('  </td></tr>\n')
        html.write(html_foot)

    serialize(sn, labels)


def exclude_hits(stage: int, excludes: List[int]) -> dict:
    data = deserialize(get_working_set_file(stage - 1))
    labels = deserialize(get_labels_file(stage - 1))

    # prepare excluded working set
    to_exclude = set()
    for ex in excludes:
        to_exclude |= set(labels[ex])

    new_data = {
        'id_array': [],
        'bitmap_array': [],
        'stored': data['stored']
    }

    for i in range(0, len(data['id_array'])):
        _id = data['id_array'][i]
        if _id not in to_exclude:
            image = data['bitmap_array'][i]
            new_data['id_array'].append(_id)
            new_data['bitmap_array'].append(image)
    return new_data


def do_compute(data: dict, stage: int, chain: List[BaseProcedure]):
    # Deserialize or compute clustering ``data`` when serialized file is not exists. See: clustering
    start_time = print_log('Clustering %d stage...' % stage)
    kmeans = deserialize_or_run(get_kmeans_file(stage), clustering, data, chain)
    print_log('  ... finish', start_time)

    save_html_and_pngs_and_labels(stage, kmeans, data)


def do_compute_first_stage(fn: str, chain: List[BaseProcedure]):
    """
    Clustering first stage.
    1. Load full working set.
    2. Compute kmeans for stage 1.
    3. Save to PNG and html for human preview.
    :param fn: input working set in JSON
    """
    stage = 1

    # Deserialize or load from ``fn`` JSON file when serialized file is not exists. See: load_data
    start_time = print_log('Load from JSON...')
    data = deserialize_or_run(get_working_set_file(stage), load_data, fn)
    print_log('  ... finish', start_time)

    do_compute(data, stage, chain)


def do_compute_nth_stage(stage: int, chain: List[BaseProcedure], excludes: List[int]):
    """
    Clustering nth stage.
    1. Load working set and labels from previous stage.
    2. Exclude hits from excluded labels.
    3. Save working set for current stage.
    4. Compute kmeans for current stage.
    :param stage: current stage of classification
    :param excludes: cut off hits from these clusters from previous stage
    """

    # Deserialize or load working set and labels from previous stage and Exclude hits from excluded labels when serialized file is not exists. See: exclude_hits
    start_time = print_log('Exclude hits...')
    data = deserialize_or_run(get_working_set_file(stage), exclude_hits, stage, excludes)
    print_log('  ... finish', start_time)

    do_compute(data, stage, chain)


def main():
    chain = [
        SortedPreprocess(),
        KMeansClassify()
    ]

    do_compute_first_stage(WORKING_SET, chain)
    do_compute_nth_stage(2, chain, [2, 3, 5, 12, 13, 15, 18])  # this is sample of clusters to eliminate
    do_compute_nth_stage(3, chain, [4, 8, 10, 14, 18])
    do_compute_nth_stage(4, chain, [6, 11, 12, 16, 17, 19])
    do_compute_nth_stage(5, chain, [2, 4, 15, 18])


if __name__ == '__main__':
    main()