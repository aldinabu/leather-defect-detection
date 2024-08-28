# Leather Defect Detection

## About
This is the basic Flask application to experiment with leather defect detection. Application has few functionalities:
- small image defect classification
- extracting patches
- big image defects detection

### Small image defect classification
upload image and click on 'Detektuj'. On the bottom of the page prediction class will be shown:
![https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-1.png](https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-1.png)

### Extracting patches
On the same screen as image classification is, upload image, click on the button 'Podijeli slike'. After the process is done, popup window with message where it is saved will be shown. 

![https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-2.png](https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-2.png)

### Image Defect Detection
On the menu tab, click on the second option. Upload the image. Click on the button 'Detektuj'. After proccess of detection is done, on the right side of the window image with marked defects will be shown. Defects are colored with the same color as legend on the right side shows. 

![https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-3.png](https://github.com/LEATHER-SEE/Leather-Defect-Detection/blob/main/images/aplikacija-3.png)

>[!IMPORTANT]
>Add model state dict used for prediction. Change 'model_net_state_dict' value in [config](config.ini) file.



## Installation
Run this command to install all packages required in the project:

```bash
pip install -r requirements.txt
```

## Run locally
To run the application run this command:
```bash
flask run --host=0.0.0.0
```

Application is now hosted [here](http://localhost:5000/).


>[!INFO]
>This project contains also Jupyter notebooks for training Inception-V3 CNN with our created dataset.
>Notebooks can be found [here](jupyter-notebooks/) .
>Dataset can be downloaded from .....
