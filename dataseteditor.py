import os
import shutil

#python mask_the_face.py --path 'data/celeba_hq_256/10k' --mask_type 'surgical' --verbose

def splitceleba():
    # directory of images
    directory= 'CELEBAHQ'
    # paths for images to go based on their number
    train_path = os.path.join("./256/", "train/")
    test_path = os.path.join(directory, "test/")
    val_path = os.path.join(directory, "val/")
    # make directories
    # each is in their own try, catch block to prevent the
    # scenario where one exists, but the others dont, as this 
    # would skip the remaining directories.
    try:
        os.mkdir(train_path)
    except OSError as err:
        print("Train Dir exists, skipping creation")    
        
    try:
        os.mkdir(test_path)
    except OSError as err:
        print("Test Dir exists, skipping creation")    

    try:
        os.mkdir(val_path)
    except OSError as err:
        print("Validation Dir exists, skipping creation")    
    
    #loop through files
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        #check if file exists
        if os.path.isfile(f):
            # f[23:28] corrosponds to the section of the filepath that contains
            # the number ie 00000 in 00000.jpg
            fd = int(f[23:28])
            # if within the first 20k
            if (fd < 20000):
                # add filepath of image to directory eg ./256/train/00000.jpg
                destination = os.path.join(train_path, f[23:])
                # copy the file to the specified filepath
                dest = shutil.copyfile(f, (destination))
            # repeat for test and val
            elif (fd < 25000 and fd >= 20000):
                destination = os.path.join(test_path, f[23:])
                dest = shutil.copyfile(f, (destination))
            elif (fd <= 30000 and fd >= 25000):
                destination = os.path.join(path30k, f[23:])
                dest = shutil.copyfile(f, (destination))
            # remove file from directory
            os.remove(f)


def deletemissingmasked():
    #directory of images
    directory= 'Datasets/LFW/Images_masked'
    directory2= 'Datasets/LFW/Images'

    #empty list
    maskedlist = []
    #append each id of the image in the masked dir to the array
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            maskedlist.append(f[27:32])

    c=0
    #loop through files and remove any that are not in the masked dir
    for filename in os.listdir(directory2):
        f = os.path.join(directory2,filename)
        if os.path.isfile(f):
            if not (f[20:25] in maskedlist):
                os.remove(f)
                c+=1
    print(c,"files removed")

def removestringfromname():
    directory= './bb/celeba_hq_256_split/10k_masked'
    #directory= './bb/celeba_hq_256_split/20k_masked'
    #directory= './bb/celeba_hq_256_split/30k_masked'

    #loop through files
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            os.rename(f, f[:41]+".jpg")

def renamefiles():
    directory= 'Datasets/LFW/Images_masked'
    #directory= './bb/celeba_hq_256_split/20k_masked'
    #directory= './bb/celeba_hq_256_split/30k_masked'

    #loop through files
    c=0
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            os.rename(f, directory+"/"+str(c).zfill(5)+".jpg")
            c+=1


def shiftfiles():
        #directory of images
    directory2= './bb/celeba_hq_256_split/10k'
    directory= './bb/celeba_hq_256_split/20k'
    #paths for images to go based on their number
 
    #loop through files
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            destination = os.path.join(directory2, f[29:])
            dest = shutil.copyfile(f, (destination))
            os.remove(f)



def delifover(level):
    #directory of images
    directory= '256/train/data256x256_masked'

    #loop through files
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            #if in first 10k
            fd = int(f[29:34])
            # fd = int(f[36:41])
            if (fd < level):
                os.remove(f)

def stringfinder():
    directory= 'Datasets/LFW/Images_masked'
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        if os.path.isfile(f):
            print(f[27:32])
            break
