```vbsoundinference``` is based of an algorithm i invented called VSI for wake work detection on CPUs.

To use ```vbsoundinference```, first collect your custom wake word data using ```vsi.recorder```.

``` python
from vsi.recorder import Recorder # import the Recorder class

recorder = Recorder() # create the Recorder object

recorder.record_class(n_recordings=10, class_number=0, duration=1, num_samples=512, # record class 0
                      dataset_file="test_dataset.txt", append=False)
```

```vbsoundinference``` will store all the training data in one file. e.g-dataset.txt.

The ```append``` argument will append the recorded data to the dataset instead of deleting the previous data.

To train the model, use ```vsi.trainer```.

``` python
from vsi.trainer import Trainer # import the Trainer class

trainer = Trainer(dataset_file_path="test_dataset.txt") # create the Trainer object

trainer.load_dataset() # load the dataset
trainer.train(epochs=100, save_path="model.pth") # train and save the model
```

To use the model, use ```vsi.vsi```.

``` python
from vsi.vsi import VSI # import the VSI class
from vsi.recorder import Recorder # import the Recorder class

vsi = VSI() # create the VSI object
recorder = Recorder() # create the Recorder object

while True: # infinite loop
    recording = recorder.record_sample() # record a sample
    
    prediction = vsi.predict(recording.recording) # get the model's prediction
    
    print(prediction)
```
