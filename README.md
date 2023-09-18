# Example YOLO Inference Pipeline on ODH
The `example-flow.ipynb` notebook contains a sample pre + post-processing pipeline to perform
YOLO segmentation on ODH.

# Usage
1) Download the [COCO Dataset](https://cocodataset.org/#download)
2) Build docker image:
`docker build . -t $TAGNAME`
3) Set `$COCO_PATH` to wherever you unzipped the dataset, specifically the folder containing the raw jpg images:
`COCO_PATH=/path/to/your/COCO/directory`
4) Run the docker image:
```bash
docker run -it -p 8888:8889 --mount type=bind,source="$COCO_PATH",target=/home/coco/ $TAGNAME
```
Alternatively, run the pre-built image:
```bash
docker run -it -p 8889:8889 --mount type=bind,source="$COCO_PATH",target=/home/coco/ quay.io/rgeada/yolo-pipeline
```

5) Navigate to the Jupyter notebook server and run the `example-flow.ipynb` notebook.


# CLI
Alternatively, you can run the pipeline from a python script:

`python3 pipeline.py /path/to/uploaded/image`