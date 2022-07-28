XPSquanti is for XPS quantification when one needs to calculate the atomic ratios. It is written in Python. 
To run this script,
1. download all the files
2. run xpsquanti.py with Python
3. makesure that the reuired cross section is included in the cs folder. if not, add it manually.

the following is a example of calculating the atomic ratio of C1s and N1s peaks. the IMFP is based on the simplified TPP-2M formua. one needs to 
pay attention to the binding energy (BE1 and BE2 correspond to the binding energy of ele1 and ele2) of the elements. if the sample is a thin film, one also need to include the thickness of the thin film. Generally, one just need to follow the steps 1-4 and insert the values and models. then click calculate.

![image](https://user-images.githubusercontent.com/42301914/181450516-be4ab76d-5842-4f9f-98b1-957354ea3e68.png)



current questions:
1. XPS setup transmission function is not included. the current script only considers the cross section and the inelastic mean free path.
2. angle dependent crosssection changes has not been included yet. current version is useful for magic angle experiment. 
