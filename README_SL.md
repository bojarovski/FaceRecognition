# Avtomatiziran sistem beleženja prisotnosti z uporabo prepoznavanja obrazov

## Opredelitev problema

Ročno beleženje prisotnosti (npr. na predavanjih, sestankih ali dogodkih) je neučinkovito, nagnjeno k napakam in dovzetno za zlorabe. Ta projekt je namenjen razvoju avtomatiziranega sistema za beleženje prisotnosti z uporabo **računalniškega vida** in **prepoznavanja obrazov**. Sistem bo zaznal in prepoznal posameznike s slik ter tako omogočil natančno in brezhibno evidentiranje prisotnosti.

### Ključne besede

- Prepoznavanje obrazov
- Avtomatsko beleženje prisotnosti
- Računalniški vid
- Konvolucijske nevronske mreže (CNN)
- Globoko učenje

---

## Pregled sorodnih del

Več raziskav je oblikovalo razvoj **tehnologije prepoznavanja obrazov**. Spodaj so ključne študije, ki so vplivale na ta projekt:

### **Metodologija FERET za ocenjevanje algoritmov prepoznavanja obrazov**

**Phillips et al., IEEE (2000)**

**Metodologija FERET (Face Recognition Technology)** zagotavlja **standardizirano testno okolje za preizkušanje sistemov za prepoznavanje obrazov**. **FERET baza podatkov** vsebuje približno **14.126 slik 1.199 posameznikov**, kar raziskovalcem omogoča analizo, kako algoritmi delujejo v različnih pogojih.

Metodologija omogoča:

- **Ocenjevanje natančnosti** algoritmov za prepoznavanje obrazov.
- **Določanje ključnih področij za nadaljnje raziskave** in izboljšave.
- **Omogočanje standardizirane primerjave algoritmov** v enakih testnih pogojih.

🔗 **[Celoten članek](https://ieeexplore.ieee.org/document/879790)**

---

### **Primerjava učinkovitosti Dlib in OpenCV za prepoznavanje obrazov**

**Boyko, Basystiuk, Shakhovska, IEEE (2018)**

Ta raziskava primerja **učinkovitost dveh priljubljenih knjižnic za prepoznavanje obrazov**, **Dlib in OpenCV**. Avtorji ocenjujejo različne **algoritme za zaznavo obrazov**, vključno z:

- **HOG + SVM** (Histogram usmerjenih gradientov s podpornimi vektorskimi stroji)
- **DCNN (Globoke konvolucijske nevronske mreže)**
- **Ocena ključnih točk obraza** za zaznavo obraznih značilnosti

Raziskava analizira **čas obdelave, natančnost prepoznavanja in računalniško učinkovitost**, s čimer ponuja vpogled v to, katera knjižnica je boljša v različnih realnih scenarijih.

🔗 **[Celoten članek](https://ieeexplore.ieee.org/document/8478556)**

---

### **Nova metoda za prepoznavanje obrazov z uporabo konvolucijskih nevronskih mrež (CNN)**

**Kamencay, Benco, Mizdos, Radil (2017)**

Ta študija prikazuje, kako **konvolucijske nevronske mreže (CNN)** bistveno izboljšajo **natančnost prepoznavanja obrazov** v primerjavi s tradicionalnimi metodami. Ključni poudarki raziskave vključujejo:

- **Izvleček značilnosti s pomočjo globokega učenja** omogoča učinkovitejšo identifikacijo obraznih vzorcev.
- **CNN prekašajo tradicionalne metode strojnega učenja** pri obdelavi obraznih slik v realnem okolju.
- Študija izpostavlja **CNN arhitekture, primerne za modele visoke natančnosti**.

🔗 **[Celoten članek](https://d1wqtxts1xzle7.cloudfront.net/108043938/2389-12960-1-PB-libre.pdf?1701275913=&response-content-disposition=inline%3B+filename%3DA_New_Method_for_Face_Recognition_Using.pdf&Expires=1741893599&Signature=LmBEdzDXjhPUM8Y7UpEIPbGnKGmGslUER1-DkzOcucYe-1y61nbbdio-LvhcSaTSuVwkUGgojoKZkcTICwruOAMWhq5Uj6PCaFekEviAsdnvyADc1WIYI81t9r9cxQTH9Ubp1q9-NoVuBy8qmJAplRH2UxicYU0u8X5wnyyehtrpPJn0T6zfNZWAaRQ5FOqW8RsQdSFK9Swaotrq5GXuhTqHfxCWknlMyNxT10UXmLsSl-g3SZCasifpwQa3rj2V9RPIpnjqwaEuk3i8olq75aJSnGdkz46NJQKBiF7nuH5l2clh7WxAAWNUsxjyLASrgWvAkLF5bDFD2cTQR258vg__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA)**

---

## Načrt rešitve

### Projektna skupina

- **Skupina**: 1
- **Člani**: Viktor Rackov, Mario Bojarovski, Marko Milenovic
- **GitHub repozitorij**: [FaceRecognition](https://github.com/bojarovski/FaceRecognition)
- **Razvojno okolje**: Python

### Razvojne iteracije

#### **Iteracija 1**

- Zbiranje in analiza podatkov.
- Nastavitev razvojnega okolja (**Python, OpenCV, face_recognition**).

#### **Iteracija 2**

- Kodiranje in shranjevanje obraznih značilnosti.
- Zajem slik iz spletne kamere in predobdelava.

#### **Iteracija 3**

- Implementacija algoritma za primerjavo obrazov.
- Optimizacija sistema za obdelavo v realnem času.
- Razvoj ukazne vrstice za upravljanje sistema.

#### **Iteracija 4**

- Razvoj grafičnega uporabniškega vmesnika (**GUI**).
- Izboljšanje natančnosti s prilagajanjem parametrov.
- Dokumentacija in končna evalvacija sistema.

---

## Opis rešitve (Diagram poteka sistema)

![Diagram poteka prepoznavanja obrazov](image.png)

---

## Repozitorij projekta

[GitHub repozitorij projekta](https://github.com/bojarovski/FaceRecognition)
