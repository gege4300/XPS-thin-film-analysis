XPSquanti is for XPS quantification when one needs to calculate the atomic ratios and film thickness. It is written in Python. 
To run this script,
1. download all the files
2. run xpsquanti.py with Python
3. makesure that the reuired cross section in the cs folder is included in the cs folder. if not, add it manually.

the following is an example of calculating the atomic ratio of C1s and N1s peaks. the IMFP is based on the simplified TPP-2M formua. one needs to 
pay attention to the binding energy (BE1 and BE2 correspond to the binding energy of ele1 and ele2) of the elements. if the sample is a thin film, one also need to include the thickness of the thin film. Generally, one just need to follow the steps 1-4 and insert the values and models. then click calculate.
here two methods are included, one (the calculate button) is the general method with the CS and IMFP considered. Another one is based on the sensitivity facor (SF). Two of them show similar results.

![image](https://user-images.githubusercontent.com/42301914/183249864-24e82ddc-f07b-4f38-950e-f1c5235c2f45.png)


the following is an example of calculating the film thickness based on the model: the thin film is on the bulk surface

![image](https://user-images.githubusercontent.com/42301914/183249882-4217dd3b-3939-4b6a-b97a-bc81308506eb.png)




current questions:
1. XPS setup transmission function is not included. the current script only considers the cross section and the inelastic mean free path.
2. angle dependent crosssection changes has not been included yet. current version is useful for magic angle experiment. 
