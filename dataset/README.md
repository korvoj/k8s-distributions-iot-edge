# `s3-download-speed`

The S3 download speed benchmarks requires a large binary file to be downloaded from a remote S3 repository.

A binary file of an arbitrary size can be created with:

```bash
fallocate -l 100M /path/to/file.img
```

# `video-processing`

The source video file is based on the [Big Buck Bunny film](https://peach.blender.org/about/) (*(c) copyright 2008, Blender Foundation / www.bigbuckbunny.org*) and is available in the `video-processing` directory. 

# `model-training`

The model training benchmark reuses the `reviews10mb.csv` dataset available in the original [kmu-bigdata/serverless-faas-workbench](https://github.com/kmu-bigdata/serverless-faas-workbench/blob/master/dataset/amzn_fine_food_reviews/reviews10mb.csv) repository.

# `image-processing`

The image processing enchmark reuses the `image.jpg` file available in the original [kmu-bigdata/serverless-faas-workbench](https://github.com/kmu-bigdata/serverless-faas-workbench/blob/master/dataset/image/image.jpg) repository.