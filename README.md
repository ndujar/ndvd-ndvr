# ndvd-ndvr: Near Duplicate Video Detection / Video Based Fraud Detector

This is a sandbox repository for the [Livepeer grant #92](https://github.com/livepeer/Grant-Program/issues/92) 

Near-Duplicate Video Detection (NDVD) and Near-Duplicate Video Retrieval are hot research topics of increasing interest in recent years due to the exponential growth of online video creation. It is considered essential in a variety of applications that involve copy detection, copyright protection, video retrieval, indexing and management and video recommendation and search.

The aim of this proposal is to research the specific application of copyright protection and to explore the potential integration within the Livepeer ecosystem.

**Describe the problem you are solving.** 

Recent developments in the Livepeer Protocol include the possibility of accessing an [MPEG-7 perceptual hashed](https://ieeexplore.ieee.org/document/6164253) version of the transcoded videos.

This basically opens the door to several applications which are worth exploring.

These include [[SHEN et al. 2020](https://journal.hep.com.cn/fcs/EN/article/downloadArticleFile.do?attachType=PDF&id=25507)]:

- Copyright Protection: Digital products are highly sensitive to different forms of fraud, like unauthorized copying, editing and / or redistribution (see copy minting of NFTs, for example). Besides, this usually results in a huge risk for Livepeer platform to become liable for these behaviors.
- Video Monitoring: Being able to monitor the ways in which a video asset is used permits Livepeer creators and their sponsors measure the impact of it and, for instance, evaluate the repercussion of embedded commercials.
- Topic Tracking: Broadcast video, especially news video, contains a broad range of real-world events that could be of critical value for the affected or interested persons. The semantic organzation of the event-related videos from different sources is essential to track and extract the most relevant of them, while maintaining an adequate degree of diversity.
- Video Recommender: This kind of systems aim at retrieving users’ preference based on their past interactions, and recommend videos that can be of value for the Livepeer user. Therefore, NDVR techniques are necessary for service subjects to efficiently search out the videos that Livepeer users may want to browse in large-scale data.
- Data mining: The purpose of data preprocessing is to reduce the impact of the existing near-duplicate contents on data mining results. When searching for videos on the Internet, one may get a list of videos flooded with near-duplicates. These near-duplicates are assumed to be removed from the list for better mining.

**Describe the solution you are proposing and how it will have a positive impact on the Livepeer developer ecosystem.** 

Even though there is a large corpus of work and research on the topic of NDVR / NDVD, the scope of this research would initially focus only on the application of the recent developments included in Livepeer's protocol (see [MPEG-7 perceptual hashing](https://forum.livepeer.org/t/transcoding-verification-improvements-fast-full-verification/1499)).

Essentially, this makes it possible to access a perceptual hashed version of any video broadcasted through the Livepeer Network.

More specifically, we would be dealing with the particular application of Near Duplicate Video Detection.

According to the literature, the extraction speed of the Video Signature descriptor from uncompressed video is ~900 frames/sec on a standard PC (Intel Xeon X5460 (single core implementation), running at 3.16GHz and with 8GB of RAM). With this performance, researchers also claim that duplicate detection by means of the MPEG-7 Video Signature achieved an average success rate of 95.49% with a false alarm rate no more that 5ppm, i.e. with a precision≈1 [S. Paschalakis et al, 2012](https://static1.squarespace.com/static/5c96595ca5682794a1eb2fa8/t/5cb6170cf9619acd0cf644b4/1555437327308/MPEG-7_Video_Signature_Author_Version.pdf).

When it comes to integration into Livepeer ecosystem, it is important to remark the following considerations:

- Some of the big concerns today around media scanning include the hash DB being a black box that is controlled by a single entity. This means that the rules for allowable media can change at any time, leading to potential data poisoning of the training subset (i.e. how do we know that the DB contains fingerprints of only a specific type of content that should be restricted?).
- Such concerns have been manifested in complaints around YouTube ContentID (i.e. even legitimate creators end up playing a game against ContentID to figure out how to edit their videos to not get flagged by ContentID).

The approach that we will be evaluating for the Livepeer use case necessarily involves using an open dataset. This makes the fingerprinting algorithm mentioned above public, which implies that once the dataset and algorithm are known it is much easier to construct media variants that circumvent scanning.
For this reason, historically, perceptual hash algorithm developers have been more secretive about how things actually work under the hood (see PhotoDNA, Cloudflare CSAM scanning, Apple NeuralHash).

Moreover, there is the need to account for assets extracted from other platforms where the access to their perceptual hash might not be possible, hence rendering them "invisible" to the detector.

**Describe why you are the right team with the capability to build this.**

I can apply my past expertise in the field of Machine Learning and Computer Vision applied to video streaming, once this problem is well understood.
Besides, I have some previous experience with Livepeer as one of the contributors of the [transcoding verifier] (https://github.com/livepeer/verification-classifier).

**Describe the scope of the project including a 3 month timeline and milestones.** 

Milestone 1: MPEG-7 Video Signature descriptor evaluation (expected completion: Nov 22)

- Test, improve and iterate with LivePeer video transcoding and Fast verification using MPEG-7 signature comparator (20h)
- Prepare / recover a suitable test dataset similar to the one described in the literature (footage of various types, ~70,000 30-second queries, and 1,900 3-minute original, non-matching clips, unrelated to each other) (20h)
- Document, illustrate and publish results in Livepeer channels for feedback collection (20h)

Milestone 2: MPEG-7 Video Signature vulnerability analysis (expected completion: Mid Nov 22)

- Find and define different tampering techniques for which the MPEG-7 perceptual hashing descriptor becomes insensitive (20h)
- Extend the test dataset with new forged assets (20h)
- Document, illustrate and publish results in Livepeer channels for feedback collection (20h)

Milestone 3: MPEG-7 Video Signature descriptor alternatives (expected completion: Dec 22)

- Find, define and choose alternative / complementary techniques for duplicate detection (20h)
- Implement a POC with the chosen alternative (20h)
- Document, illustrate and publish results in Livepeer channels for feedback collection (20h)

Milestone 4: Livepeer's Video Copy detector integration (expected completion: Jan 23)

- Once a suitable detector has been chosen, define the architecture and mechanisms for retrofitting the open source database and its access (20h)
- Implement and integrate needed APIs (40h)

NOTE: Milestones are approximate and to be reviewed and adjusted accordingly with updated time, costs and scope at the end of the previous. 
Computational costs for creation of the test / train dataset need to be considered apart.

**Please estimate hours spent on project based on the above and how much funding you will need.** 

Assuming researchers work part time (4 hours per day) the research and divulging content creation should be completed within 9 weeks (180h in total). 
Implementation and integration is expected to take 3 weeks (60h).

- Researcher Hourly Wage: $55/hr USD* Up for discussion
- Cloud computing costs: TBD

Funding needed: USD13200 + Cloud costs
