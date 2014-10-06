# This is just a quick script for reading .ser movie files.

%pylab
import struct

# Change this filename to suit your needs...
filename = './uranus20141002-1511.ser'

with open(filename,'rb') as f:
    FileID = f.read(14) #str
    # Do an incredibly naive sanity check on the data
    if not FileID == 'LUCAM-RECORDER':
        print 'This is not a .ser formatted file.'
    LuID = struct.unpack('<I',f.read(4))[0] #int32
    ColorID = struct.unpack('<I',f.read(4))[0] #int32
    LittleEndian = struct.unpack('<I',f.read(4))[0] #int32
    ImageWidth = struct.unpack('<I',f.read(4))[0] #int32
    ImageHeight = struct.unpack('<I',f.read(4))[0] #int32
    PixelDepth = struct.unpack('<I',f.read(4))[0] #int32
    BytePerPixel = 1 if PixelDepth<=8 else 2
    FrameCount = struct.unpack('<I',f.read(4))[0] #int32
    Observer = struct.unpack('<40s',f.read(40))[0] #str
    Instrume = struct.unpack('<40s',f.read(40))[0] #str
    Telescope = struct.unpack('<40s',f.read(40))[0] #str
    DateTime = struct.unpack('<8s',f.read(8))[0] #"Date"
    DateTime_UTC = struct.unpack('<8s',f.read(8))[0] #"Date"

print 'Image size is: '+str(ImageWidth)+'x'+str(ImageHeight)
print 'Frame count: '+str(FrameCount)

HeaderBytes = 178
WhichFrame = 150
ImagePixels = ImageWidth*ImageHeight
ImageBytes = ImagePixels*BytePerPixel
with open(filename,'rb') as f:
    f.seek(HeaderBytes+ImageBytes*WhichFrame)
    f.read(ImageBytes)
    fmt = '<'+str(ImagePixels)+('H' if BytePerPixel==2 else 'B')
    img = np.array(struct.unpack(fmt,f.read(ImageBytes))).reshape(ImageHeight,ImageWidth)

plt.imshow(img)

