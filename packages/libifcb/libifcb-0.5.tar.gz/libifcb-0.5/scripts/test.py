from libifcb import ROIReader
import json

sample1 = ROIReader("testdata/D20140117T003426_IFCB014.hdr", "testdata/D20140117T003426_IFCB014.adc", "testdata/D20140117T003426_IFCB014.roi")
#print(json.dumps(sample1.header, indent=4))
#for trigger in sample1.triggers:
    #print(json.dumps(trigger.raw, indent=4))
print(str(len(sample1.rois)) + " ROIs")
sample1.rois[1899].image.save("testout/D20140117T003426_IFCB014_02177.png") # This list only contains valid ROIs - indexes will not match with other software!
sample1.rows[2176].image.save("testout/D20140117T003426_IFCB014_02177.tiff") # ADC row indexes start from one, but we start from zero to be pythonic
sample1.triggers[2102].rois[0].image.save("testout/D20140117T003426_IFCB014_02177.jpeg") # As do trigger indexes, this is trigger #2103
# Both should match https://ifcb-data.whoi.edu/image?image=02177&bin=D20140117T003426_IFCB014
