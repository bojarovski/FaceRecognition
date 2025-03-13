# **Automated Attendance System Using Face Recognition**

## **Problem Definition**

Manual attendance tracking (e.g., in lectures, meetings, or events) is time-consuming, often inaccurate, and prone to fraud. The goal of this project is to develop an automated system that utilizes computer vision and face recognition to enable fast and reliable attendance tracking. Mathematically, the problem is defined as a classification task.

### **Keywords:**

- Face Recognition
- Automated Attendance
- Computer Vision
- Convolutional Neural Networks (CNN)
- Deep Learning

---

## **Review of Related Work and Evaluation Methods**

### **FERET Evaluation Methodology for Face-Recognition Algorithms**

The **FERET (Face Recognition Technology) evaluation methodology**, as described by **P. Jonathon Phillips et al.**, provides a standardized testing framework for assessing the performance of face recognition algorithms. The FERET database consists of over **14,126 images from 1,199 individuals**, divided into development and sequestered portions. This methodology evaluates face recognition systems based on three primary objectives:

1. Assessing the state-of-the-art performance of face recognition technology.
2. Identifying key areas for further research and improvement.
3. Providing a controlled and repeatable test environment for algorithm benchmarking.

The FERET methodology is widely referenced in face recognition research as it offers a consistent benchmark for comparing different algorithms under identical testing conditions. More details can be found in the **IEEE paper**:  
[Phillips, P. Jonathon, et al. "The FERET Evaluation Methodology for Face-Recognition Algorithms."](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=879790)

### **Performance Evaluation of Dlib and OpenCV for Face Recognition**

The study by **N. Boyko, O. Basystiuk, and N. Shakhovska**, titled _"Performance Evaluation and Comparison of Software for Face Recognition, Based on Dlib and OpenCV Library"_, compares the effectiveness of **OpenCV** and **dlib** for face recognition tasks. The research highlights:

- A comparative analysis of **face detection algorithms**, including **HOG + SVM, Deep Convolutional Neural Networks (DCNN), and face landmark estimation**.
- Advantages and disadvantages of OpenCV and dlib in **real-world facial recognition scenarios**.
- Performance evaluation based on execution time, number of iterations, and computational efficiency.

This work provides valuable insights into the strengths and weaknesses of OpenCV and dlib in various facial recognition applications. More details can be found in the **IEEE paper**:  
[Boyko, Basystiuk, Shakhovska - "Performance Evaluation and Comparison of Software for Face Recognition, based on Dlib and OpenCV Library"](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8478556)

### **A New Method for Face Recognition Using Convolutional Neural Networks (CNNs)**

The research by **Patrik Kamencay, Miroslav Benco, Tomas Mizdos, and Roman Radil**, titled _"A New Method for Face Recognition Using Convolutional Neural Network"_, explores the use of **CNN-based architectures** for facial recognition. The study presents:

- A comparison between traditional **machine learning approaches** and deep-learning-based CNN models.
- The efficiency of **feature extraction and classification using CNNs**.
- The potential of **CNNs to outperform classical face recognition methods** in terms of accuracy and robustness.

This paper provides important insights into how CNNs can enhance face recognition systems by improving accuracy while maintaining computational efficiency. More details can be found in the **full paper**:  
[Kamencay et al. - "A New Method for Face Recognition Using Convolutional Neural Network"](https://d1wqtxts1xzle7.cloudfront.net/108043938/2389-12960-1-PB-libre.pdf?1701275913=&response-content-disposition=inline%3B+filename%3DA_New_Method_for_Face_Recognition_Using.pdf&Expires=1741893599&Signature=LmBEdzDXjhPUM8Y7UpEIPbGnKGmGslUER1-DkzOcucYe-1y61nbbdio-LvhcSaTSuVwkUGgojoKZkcTICwruOAMWhq5Uj6PCaFekEviAsdnvyADc1WIYI81t9r9cxQTH9Ubp1q9-NoVuBy8qmJAplRH2UxicYU0u8X5wnyyehtrpPJn0T6zfNZWAaRQ5FOqW8RsQdSFK9Swaotrq5GXuhTqHfxCWknlMyNxT10UXmLsSl-g3SZCasifpwQa3rj2V9RPIpnjqwaEuk3i8olq75aJSnGdkz46NJQKBiF7nuH5l2clh7WxAAWNUsxjyLASrgWvAkLF5bDFD2cTQR258vg__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)

---

## **Solution Plan**

### **Project Team**

- **Group:** 1
- **Team Members:** Viktor Rackov, Mario Bojarovski, Marko Milenovic
- **GitHub Repository:** [FaceRecognition](https://github.com/bojarovski/FaceRecognition)
- **Development Environment:** Python

### **Development Iterations**

#### **Iteration 1**

- Collect and analyze suitable datasets of facial images.
- Set up the development environment (_Python, OpenCV, Face Recognition_).

#### **Iteration 2**

- Implement face encoding and storage using the **face_recognition** library.
- Develop a module to capture images from a webcam and preprocess them.
- Implement the **preprocessing pipeline** (resizing, lighting adjustment).

#### **Iteration 3**

- Implement the **face matching algorithm** that compares new faces to stored encodings.
- Optimize performance for real-time processing.
- Develop a simple **command-line interface** for user interaction.

#### **Iteration 4**

- Implement a **graphical user interface (GUI)** for better user experience.
- Improve the accuracy of face recognition using parameter tuning.
- Document the project and evaluate system performance.

---

## **Solution Description (UML Diagram)**

![Training and Recognition phase](image.png)

## **Project Repository**

[GitHub Project Repository](https://github.com/bojarovski/FaceRecognition)
