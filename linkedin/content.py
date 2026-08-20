HEADLINE = "Principal Machine Learning Engineer at Snapp! | MLOps, Computer Vision & Agentic LLM Systems | Python, Go, Kubernetes | Real-time ML at 3,000 RPS and ~1M events/sec"

ABOUT = """I build machine learning systems that have to answer in milliseconds, and keep answering when a million events a second are coming in.

For nine years I have worked on the production end of ML: the part where a model meets real traffic, a real latency budget, and real users. Today I am Principal Machine Learning Engineer at Snapp!, where I own the ML roadmap across Safety, Driver Signup, Support Automation and ETA, and set quarterly technical direction with the Director of Engineering.

What I do best:

- Put models into production and keep them there. Nvidia Triton and Kubernetes serving 3,000 RPS under 10ms.
- Build the MLOps underneath. Apache Airflow, MLflow, DVC and ArgoCD, with model monitoring and drift detection, which cut our retraining and deployment cycle from quarterly to weekly.
- Fit models where there is no room. A 1MB on-device computer vision pipeline running on iOS, Android and Web; knowledge distillation inside a 2GB budget on Jetson Nano.
- Design agentic LLM systems. A graph-based state machine agent in Go that now resolves 85% of support tickets.
- Lead the people who do it. Teams of 6 to 12, the hiring and interview pipeline behind them, and mentoring.

Before Snapp! I led a 12-person cross-functional team at Galliot shipping real-time computer vision products to edge devices, built multi-camera ReID tracking at Neoxi, and designed multimodal property valuation models at IREEN. I started out applying system identification to structural health monitoring, which is where I learned that a model nobody trusts is a model nobody uses.

Core skills: Machine Learning, Deep Learning, MLOps, Computer Vision, NLP, Large Language Models, Agentic AI, RAG, Python, Go, SQL, C++, PyTorch, TensorFlow, TensorRT, Nvidia Triton, ONNX, Kubernetes, Apache Kafka, Apache Spark, Apache Airflow, MLflow, AWS, GCP, Distributed Systems, Edge AI, A/B Testing, Technical Leadership.

Open to Staff and Principal machine learning roles, remote or relocating. Reach me at soheil.koohi@gmail.com."""

ROLES = [
    ("Principal Machine Learning Engineer", "Snapp! | Mar 2026 - Present | Tehran, Iran",
     "Own the machine learning roadmap across four product areas at Iran's largest ride-hailing platform, and the hiring pipeline that staffs them.",
     [
      "Own the ML roadmap across Safety, Driver Signup, Support Automation and ETA, setting quarterly technical direction with the Director of Engineering; designed the ML hiring and interview pipeline and made the final technical call on 3-5 engineering hires.",
      "Architected a graph-based state machine support LLM agent in Go, orchestrating language model workflows across specialized nodes: toxicity safeguards, intent-based triage and external tool-calling.",
      "Scaled the Go agentic architecture on Kubernetes with Helm, integrating Redis and ClickHouse as memory layers, automating 85% of all support tickets.",
      "Developed an unsupervised clustering pipeline segmenting drivers into three safety tiers from ban records, trip ratings and NLP analysis of passenger comments, now a core upstream feature for cross-functional intervention workflows.",
      "Engineered a real-time trip safety scoring engine using a Gaussian Mixture Model over live route deviations, time-of-day and geographic isolation; A/B tests showed a 10x increase in unsafe ride recall at only a 2x increase in back-office alarms.",
      "Shipped a compressed 1MB on-device computer vision pipeline across iOS, Android and Web for real-time object detection and image quality assessment on sign-up documents, cutting wrong submissions by 50% and driver sign-up time by 30%.",
     ]),
    ("ML Technical Lead", "Snapp! | Dec 2023 - Mar 2026 | Tehran, Iran",
     "Led the data team behind Snapp!'s ETA and traffic-speed products, and built the serving and MLOps platform the rest of the ML org runs on.",
     [
      "Led and mentored a 6-person cross-functional data team to rebuild the core ETA product, architecting a deep learning residual model adapting Uber's DeeprETA on top of the routing engine, improving driver ETA accuracy by 5%.",
      "Deployed resilient model serving pipelines on Nvidia Triton and Kubernetes, handling 3,000 RPS at under 10ms latency.",
      "Architected a fully automated MLOps pipeline with Apache Airflow, MLflow and DVC, adding model monitoring and drift detection to cut the distributed retraining and deployment cycle from quarterly to weekly with full reproducibility.",
      "Engineered a high-throughput real-time speed generation pipeline using Apache Kafka and Kafka Streams, ingesting ~1 million spatial-temporal location messages per second.",
      "Designed historical speed imputation algorithms using Alternating Least Squares, Kalman filters and graph-based methods, increasing speed coverage across unobserved street segments by 60%.",
     ]),
    ("Senior Machine Learning Engineer", "Neoxi | Sep 2022 - Dec 2023 | Remote, USA",
     "Built the multi-camera person re-identification system: embeddings on the edge, matching in the cloud.",
     [
      "Architected a multi-camera ReID tracking system, extracting high-dimensional feature embeddings on edge devices and streaming them to centralized servers via Apache Kafka.",
      "Optimized on-device inference with Nvidia DeepStream, detecting and tracking pedestrians and tiny objects in real-time edge environments, improving tracking mAP by 17% over 6 months.",
      "Rebuilt the server-side cross-camera matching logic, upgrading the embedding vector database from Redis to Milvus, scaling to hundreds of concurrent camera feeds and millions of active embeddings.",
      "Managed end-to-end training and deployment infrastructure on AWS SageMaker and ECS, cutting development time by 70% with 100% deployment automation.",
     ]),
    ("ML Team Lead", "Galliot | Jan 2020 - Sep 2022 | Remote, USA",
     "Led a 12-person cross-functional team building real-time computer vision products for edge hardware, from research through production release.",
     [
      "Led a 12-person cross-functional team across ML, Backend, Frontend and Design, owning the technical roadmap and mentoring the ML engineers; promoted into the role from within the team.",
      "Led end-to-end development of a COVID-19 back-to-work SaaS product for real-time social distancing and face mask detection, integrating low-cost edge clusters with enterprise CCTV networks to process 20+ concurrent camera feeds.",
      "Engineered an Adaptive Learning pipeline using knowledge distillation to compress large-scale object detection models into efficient label-free architectures, optimizing gradient calculations to run within a strict 2GB RAM budget on Jetson Nano.",
      "Integrated PyTorch models with TensorRT and TFLite for high-speed edge inference, achieving up to 130% reduction in inference time and over 90% accuracy across 100+ edge devices.",
     ]),
    ("Computer Vision Engineer", "IREEN | Dec 2018 - Jan 2020 | Remote, Austria",
     "Built the multimodal model behind an automated residential property valuation product.",
     [
      "Designed a multimodal real-estate valuation system in TensorFlow 2, fusing structured property data with aerial, street-level and interior imagery via multi-branch Convolutional Neural Networks, achieving 6% prediction error.",
      "Derived location features from the Google Places API, mapping neighborhood amenities into grid representations and improving baseline model accuracy by 4%.",
      "Deployed Dockerized inference services on GCP GPU virtual machines with FastAPI, serving real-time predictions to the product frontend.",
     ]),
    ("Data Scientist", "ISENSE | Oct 2017 - Nov 2018 | Tehran, Iran",
     "First technical ML hire at an 8-person structural engineering startup, applying system identification to infrastructure safety.",
     [
      "Built data-driven Structural Health Monitoring models for critical infrastructure using System Identification and subspace methods in Python and MATLAB, increasing prediction precision by 30%.",
      "Led data science as the sole ML expert in an 8-person startup, building MATLAB visualization tools that translated dynamic system models into safety insights for non-technical stakeholders, and mentoring civil engineers in data science workflows.",
     ]),
]

SKILLS = [
 "Machine Learning","Deep Learning","MLOps","Computer Vision","Natural Language Processing (NLP)",
 "Large Language Models (LLM)","Agentic AI","Retrieval-Augmented Generation (RAG)","Model Deployment",
 "Model Monitoring","Distributed Systems","Edge Computing","A/B Testing","Technical Leadership",
 "Engineering Management","Mentoring","Technical Recruiting","Product Roadmapping","Cross-functional Team Leadership",
 "Python","Go (Programming Language)","SQL","C++","MATLAB",
 "PyTorch","TensorFlow","Keras","TensorRT","NVIDIA Triton Inference Server","ONNX","NVIDIA DeepStream",
 "TensorFlow Lite","OpenCV","Hugging Face Transformers","Knowledge Distillation","MLX",
 "Kubernetes","Helm","Argo CD","Docker","Terraform","CI/CD",
 "Apache Kafka","Apache Spark","Apache Airflow","MLflow","DVC",
 "Amazon Web Services (AWS)","Google Cloud Platform (GCP)","PostgreSQL",
]

TOP3 = ["Machine Learning", "MLOps", "Technical Leadership"]

LIMITS = {"headline": 220, "about": 2600, "role": 2000}
