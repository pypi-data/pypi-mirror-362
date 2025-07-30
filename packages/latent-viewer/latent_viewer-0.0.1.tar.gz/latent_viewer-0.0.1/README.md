# LatentViewer

LatentViewer is a visualisation tool to inspect image embeddings.
It uses principal component analysis to display the embedding vectors as a point
cloud.
Individual points can be selected to display an image, as well as its nine
closest neighbours.

Additionally, there is the possibility to train an SVM classifier through an
active learning method.
This is particularly useful when dealing with embeddings of an unlabeled data set.

## Installation

Install the latent viewer with pip:
```bash
pip install latent-viewer
```

## Usage

After installation, the `latent-viewer` can be invoked with `lv`.
For using, it is important to specify both a file with the embeddings, as well as an HDF5 image archive.

```bash
lv -e embeddings.csv -a image_archive.hdf5
```
