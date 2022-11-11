# Context

Near-Duplicate Video Detection (NDVD) and Near-Duplicate Video Retrieval are hot research topics of increasing interest in recent years due to the exponential growth of online video creation. It is considered essential in a variety of applications that involve copy detection, copyright protection, video retrieval, indexing and management and video recommendation and search.

Recent developments included in the Livepeer Protocol (see [MPEG-7 perceptual hashing](https://forum.livepeer.org/t/transcoding-verification-improvements-fast-full-verification/1499)) include the possibility of accessing an [MPEG-7 perceptual hashed](https://ieeexplore.ieee.org/document/6164253) version of the transcoded videos. This basically opens the door to several applications which are worth exploring.

Such applications include [[SHEN et al. 2020](https://journal.hep.com.cn/fcs/EN/article/downloadArticleFile.do?attachType=PDF&id=25507)]:

* Copyright Protection: Digital products are highly sensitive to different forms of fraud, like unauthorized copying, editing and / or redistribution (see copy minting of NFTs, for example). Besides, this usually results in a huge risk for Livepeer platform to become liable for these behaviors.
* Video Monitoring: Being able to monitor the ways in which a video asset is used permits Livepeer creators and their sponsors measure the impact of it and, for instance, evaluate the repercussion of embedded commercials.
* Topic Tracking: Broadcast video, especially news video, contains a broad range of real-world events that could be of critical value for the affected or interested persons. The semantic organzation of the event-related videos from different sources is essential to track and extract the most relevant of them, while maintaining an adequate degree of diversity.
* Video Recommender: This kind of systems aim at retrieving users’ preference based on their past interactions, and recommend videos that can be of value for the Livepeer user. Therefore, NDVR techniques are necessary for service subjects to efficiently search out the videos that Livepeer users may want to browse in large-scale data.
* Data mining: The purpose of data preprocessing is to reduce the impact of the existing near-duplicate contents on data mining results. When searching for videos on the Internet, one may get a list of videos flooded with near-duplicates. These near-duplicates are assumed to be removed from the list for better mining.

In this research, we are only focusing on the Copyright Protection applications, given the growing impact copy-minting is having in the crypto community.

# Methodology

The study has been split into four stages, namely:
- MPEG-7 Video Signature descriptor evaluation
- MPEG-7 Video Signature vulnerability analysis 
- MPEG-7 Video Signature descriptor alternatives
- Livepeer's Video Copy detector integration

Each stage corresponds to one of the proposed milestones described in the [Livepeer Grant Program Issue #92](https://github.com/livepeer/Grant-Program/issues/92)

# The dataset
For the first part, in order to properly assess the functionality described in the Livepeer Protocol in [this same forum](https://forum.livepeer.org/t/transcoding-verification-improvements-fast-full-verification/1499), a suitable dataset has been selected from the available literature.
Specifically, the VCDB (Video Copy DataBase) was chosen, given its comprehension, the ease of use and the existence of a list of annotations that would greatly enable the statistical analysis. It is further presented [here](https://fvl.fudan.edu.cn/dataset/vcdb/list.htm). 
The main corpus of the dataset consists of 528 video sequences of different length (72.77s on average) and is publicly available [here](https://drive.google.com/drive/folders/0B-b0CY525pH8NjdxbFNGY0JJdGs?resourcekey=0-RFJPDV0q40sND2xADRA1Dw). The sequences correspond to 28 specific popular culture scenes stored in Youtube and MetaCafe (Roberto Baggio missing a penalty in 1994 World Final Cup of Soccer, Angelina Jolie and Brad Pitt in the tango scene of Mr&Mrs Smith Holliwood movie, etc)
Further details can be found in the article [VCDB: A Large-Scale Database for Partial Copy Detection in Videos](https://fvl.fudan.edu.cn/_upload/article/files/7b/c4/190424104d2192e8e83cb9dfa6fc/5a8d85f7-5738-450c-b957-3de71d8d7e72.pdf), and includes major transformations between the copies such as "insertion of patterns", "camcording", "scale change", "picture in picture", among others. A secondary "background dataset" is further described there but not considered in our research at this point.

As a comparison to other datasets, the table and figures below were obtained from the publication [A Large-Scale Short Video Dataset for Near-Duplicate Video Retrieval](https://svdbase.github.io/files/ICCV19_SVD.pdf).
![image|690x403](https://github.com/ndujar/ndvd-ndvr/blob/main/research/images/datasets_comparison.png)

# Evaluation of the MPEG-7 Video Signature for Near Duplicate Detections
In order to assess the ability of the MPEG-7 perceptual hashing to identify copied sub-segments of video within another, we used the [signature filter](https://ffmpeg.org/ffmpeg-filters.html#signature-1) provided by ffmpeg. To do that, a few python scripts (available [here](https://github.com/ndujar/ndvd-ndvr)) were produced for convenience.
The process of duplicate detection carries two main steps:
- Extraction and compression of the signature for each sample
- Localization of matches between signatures

These steps are evaluated in more detail in order to properly understand their practical application in the context of the Livepeer ecosystem. 

## Signature extraction and compression
The process of extracting a signature according to the MPEG-7 Standard (ISO/IEC 15938) is described in depth at the document https://ieeexplore.ieee.org/document/6164253.
In summary, it consists of aggregations of "fine signatures" from each frame of the given video sequence into bags-of-words (histograms) that comprise what is referred to as "coarse signatures", taken form every 90 frames, then shifted 45 frames.
![frame-MPEG-7|627x289](https://github.com/ndujar/ndvd-ndvr/blob/main/research/images/fine-signatures.png)

![bags-MPEG-7|690x441](https://github.com/ndujar/ndvd-ndvr/blob/main/research/images/coarse_signatures.png)

In the context of the Livepeer ecosystem, this procedure implies an extra computational cost that needs to be evaluated. 
According to the aforementioned document, the speed of extraction is ~900 fps in a standard PC. It was found, however, a much higher speed in our profiling experiments, carried away in a Lenovo ThinkPad T480 running Ubuntu 22.04.1 with Intel Core i7-8550U (8 cores) and 16GB of RAM.
The scatter plot below shows the results of our experiments, ran over the 528 samples of the VCDB dataset. Each point represents a single sample's signature extraction time against the total number of pixels (as frames x fps x height x width). The color serves as a reference to observe the influence of the spatial resolution (which is nonexistent).
It is possible to conclude that neither the number of pixels nor the duration nor the resolution affected significantly to the speed of computation, which fluctuates around the 40ms - 80ms per sample, regardless of the sample's characteristics.
![image|690x388](https://github.com/ndujar/ndvd-ndvr/blob/main/research/images/results_scatterplot.png)

Another relevant parameter to take in consideration is that of the extra bytes required by the signatures file.
According to the specification:

> The compactness requirement was that the Video Signature shall not exceed 30,720 bits/sec of content at 30 frames/sec, i.e. 1,024 bits per frame on average.

It is also mentioned that:

> In its uncompressed form, the fine frame-level signature is quite compact, requiring only 656 bits of storage. The coarse segment-level signature is also very compact, requiring only 1215 bits of storage. Thus the complete uncompressed Video Signature storage cost is 683 bits/frame, or 20,490 bits/sec at 30 frames/sec, i.e. ~9MB per hour of video at 30 frames/sec. In its compressed form, the complete Video Signature storage cost is, on average, 184 bits/frame, or 5,532 bits/sec at 30 frames/sec, i.e. ~2.5MB per hour of video at 30 frames/sec.

In our case, none of the generated binary files was larger than 2.65MB, as can be observed in the chart below. However, there is a very evident linear relationship between the number of frames (hence the amount of stored fine and coarse signatures) and the size of the binary file. This line is defined by the equation:
`File Size = 90 * #Frames`
 
![image|690x387](https://github.com/ndujar/ndvd-ndvr/blob/main/research/images/storage_scatterplot.png)

Finally, although the option of using other formats for storing exists (.xml), it is strongly discouraged, given the fact that it is not compressed, resulting in much larger signature files.

## Match localization
In order to assess the feasibility of the matching between pairs from a purely functional standpoint, another set of experiments was conducted using the tools provided with the VCDB dataset.
As it is described in the MPEG-7 specification document, the robustness tests conducted therein only contemplate a very specific set of "synthetic" modifications:
- (TLO) Text/logo overlay
- (CIF) Compression at CIF resolution
- (RR) Resolution reduction from SD
- (FR) Frame-rate reduction from 25/30fps
- (CAM) Camera capture at SD resolution
- (VCR) Analog VCR recording/recapture
- (MON) Color to monochrome
- (BR) Brightness change (additive)
- (IP) Interlaced/progressive conversion

It is pointed out, in the VCDB paper, that this kind of modifications lead inevitably to partial solutions with near perfect results (as is the case of the MPEG-7 specification), but of dubious validity for real life scenarios, often too complex to be simulated. 
The VCDB authors explain about their dataset the following:
> Major transformations between the copies include "insertion of patterns", "camcording", "scale change", "picture in picture", etc.

Which is expected to be more aligned with the scenarios one may find in Livepeer.
For our experiments, we have used the provided videos together with the set of manual annotations giving the actual pair matches.
The script used in this case is available in the [research repository](https://github.com/ndujar/ndvd-ndvr) as multiple_match.py. It basically automates the process of pairing videos from the dataset, given a list of known matching pairs, and computing the found / not found match by means of ffmpeg signature filter.
As explained in the VCDB doumentation,

> For each row in the annotation file, there are six fields: video A, video B, A start time, A end time, B start time, B end time.
> 
> For example:
> 
> 	127dab55025984673f65d3a23b1fea99ecc79b15.mp4,12e5b295f88e0c387a4326c73613b1c7a05f2eda.flv,00:01:19,00:01:49,00:00:21,00:00:51
> 
> means 00:01:19-00:01:49 of video 127dab55025984673f65d3a23b1fea99ecc79b15.mp4 and 00:00:21-00:00:51 of video 12e5b295f88e0c387a4326c73613b1c7a05f2eda.flv are partial copies.

We ran the script over 3479 pairs, extracted from 18 of the 29 available pairs lists (queries) provided by the VCDB.
We got the following results:
- 129 pairs led to ffmpeg failure
- 960 pairs did not find any match
- 3350 pairs found at least one match

Considering that the possibility of having unmatched pairs in those annotations is low, given their manual nature done by specialized technicians, we can conclude that those 960 pairs with no match come from the inability of the signature system to detect such cases.
This represents a False Negative rate of 28.6% (or a True Positive rate of 71.4%), which is quite far from the results obtained in the robustness tests presented in Table V of the [MPEG-7 paper](https://ieeexplore.ieee.org/document/6164253) for Light intensity modification levels. Nevertheless, this success rate is still aligned with the High intensity modification levels presented there.
Timing considerations have been left aside for now as in real life the prior knowledge of the pairs does not exist and a different pairing strategy needs to be defined. 
Further estimates on the matching speed can be obtained from Table VII of the same document, where they claim an average of over 2000 matches per second when searching 10s segments within 3-minute clips. Our results however are much worse (an average 15s per match) so they will be considered inconclusive until further research is done.

# Conclusions and further work

In this first milestone of the research into Near Duplicate Video Detection, some capabilities and technical viability of the MPEG-7 video signature were explored.
We researched and selected a publicly available, annotated dataset with over 500 video segments. Those segments correspond to 28 specific popular culture scenes and come with manual annotations of matching pairs of clips within other clips at a given start and end time.
We also computed the binary video signature of each of the 528 assets. The computation of these binary compressed signatures was proven a fairly inexpensive and fast process, in the range of 40 - 80 ms each, regardless of the clip size, resolution or duration. 
In terms of storage requirements, we found a linear ratio between the number of frames and the file size in bytes (90x), which means a storage cost of 2.7kB/s at 30FPS, or 9.72MB/h, in line with the MPEG-7 description.
For now, we find the actual match search much more computationally expensive with the used tools (ffmpeg's signature filter), even in a directed one-to-one search. Nevertheless, success rate is in the range of the (otherwise worst) results presented by the MPEG-7, for the High modification level, and lies in the 71.4%.

Further work aims at analyzing the specific sources of failure for those 28.6% undetected videos and start outlining the database indexing algorithm that might allow for fast retrieval with high accuracy.

Stay tuned!