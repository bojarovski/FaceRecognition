# Automated Attendance System Using Face Recognition

## Problem Definition

Manual attendance tracking (e.g., in lectures, meetings, or events) is inefficient, error-prone, and susceptible to manipulation. This project aims to develop an automated attendance system using **computer vision** and **face recognition**. The system will detect and recognize individuals from images, ensuring an accurate and seamless attendance recording process.

### Keywords

- Face Recognition
- Automated Attendance
- Computer Vision
- Convolutional Neural Networks (CNN)
- Deep Learning

---

## Related Work

Several studies have shaped the evolution of **face recognition technology**. Below are key research contributions that influenced this project:

### **FERET Evaluation Methodology for Face-Recognition Algorithms**

**Phillips et al., IEEE (2000)**

The **FERET (Face Recognition Technology) evaluation methodology** provides a **benchmark for testing face recognition systems**. The **FERET dataset** consists of **around 14,126 images of 1,199 individuals**, enabling researchers to analyze how algorithms perform under different conditions.

The methodology helps in:

- **Assessing the accuracy** of face recognition algorithms.
- **Identifying key research areas** for future improvements.
- **Providing a standardized dataset** for algorithm comparison.

🔗 **[Read the full paper](https://ieeexplore.ieee.org/document/879790)**

---

### **Performance Evaluation of Dlib and OpenCV for Face Recognition**

**Boyko, Basystiuk, Shakhovska, IEEE (2018)**

This study compares the **performance of two widely used face recognition libraries**, **Dlib and OpenCV**. The authors evaluate different **face detection algorithms**, including:

- **HOG + SVM** (Histogram of Oriented Gradients with Support Vector Machines)
- **DCNN (Deep Convolutional Neural Networks)**
- **Face Landmark Estimation** for facial feature detection

The research analyzes execution time, **recognition accuracy**, and computational efficiency, offering insight into which library performs better in various real-world scenarios.

🔗 **[Read the full paper](https://ieeexplore.ieee.org/document/8478556)**

---

### **A New Method for Face Recognition Using Convolutional Neural Networks (CNNs)**

**Kamencay, Benco, Mizdos, Radil (2017)**

This study demonstrates how **Convolutional Neural Networks (CNNs)** significantly improve face recognition **accuracy** compared to traditional methods. Key takeaways from this research include:

- **Feature extraction using deep learning** allows CNNs to identify facial patterns more efficiently.
- **CNNs outperform traditional machine learning methods** in handling real-world face recognition tasks.
- The study highlights CNN architectures suitable for **high-accuracy face recognition models**.

🔗 **[Read the full paper](https://d1wqtxts1xzle7.cloudfront.net/108043938/2389-12960-1-PB-libre.pdf?1701275913=&response-content-disposition=inline%3B+filename%3DA_New_Method_for_Face_Recognition_Using.pdf&Expires=1741893599&Signature=LmBEdzDXjhPUM8Y7UpEIPbGnKGmGslUER1-DkzOcucYe-1y61nbbdio-LvhcSaTSuVwkUGgojoKZkcTICwruOAMWhq5Uj6PCaFekEviAsdnvyADc1WIYI81t9r9cxQTH9Ubp1q9-NoVuBy8qmJAplRH2UxicYU0u8X5wnyyehtrpPJn0T6zfNZWAaRQ5FOqW8RsQdSFK9Swaotrq5GXuhTqHfxCWknlMyNxT10UXmLsSl-g3SZCasifpwQa3rj2V9RPIpnjqwaEuk3i8olq75aJSnGdkz46NJQKBiF7nuH5l2clh7WxAAWNUsxjyLASrgWvAkLF5bDFD2cTQR258vg__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)**

---

## Solution Plan

### Project Team

- **Group**: 1
- **Members**: Viktor Rackov, Mario Bojarovski, Marko Milenovic
- **GitHub Repository**: [FaceRecognition](https://github.com/bojarovski/FaceRecognition)
- **Development Environment**: Python

### Development Iterations

#### **Iteration 1**

- Data collection and analysis.
- Set up the development environment (**Python, OpenCV, face_recognition**).

#### **Iteration 2**

- Face encoding and storage.
- Image capture from a webcam and preprocessing.

#### **Iteration 3**

- Face matching algorithm implementation.
- Real-time performance optimization.
- Command-line interface development.

#### **Iteration 4**

- Graphical user interface (**GUI**) development.
- Accuracy enhancement through parameter tuning.
- System documentation and evaluation.

---

## Solution Description (Workflow Diagram)

![Face Recognition Workflow Diagram](image.png)

---

## Project Repository

[GitHub Project Repository](https://github.com/bojarovski/FaceRecognition)
